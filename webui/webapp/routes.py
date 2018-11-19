"""Defines the URIs which can called in the Flask Webapp and the logic behind."""

from flask import render_template, request, session, make_response
from webui.webapp import app
from webui.webapp.forms import SearchForm, FilterForm
import sys
from webui.flaskconfig import Config
from webui.database.models import Report
from sqlalchemy import and_, desc, asc

@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def searchPage():
    """On the search page the user may enter a query and get a list of matching police reports returned.
    Returns
    -------
    Returns either a ResultPage.html or a SearchPage.html depending on whether the user call the link with or
    without having submitted the query entry form."""
    form = SearchForm(request.form)
    if form.validate_on_submit(): # Is only called when the form is submitted
        if "metapy" in sys.modules:
         #   # reload(metapy) doenst work
         #   reload("metapy") doestn work
            # metapy = sys.modules("metapy") doenst work
            #del sys.modules["metapy"]
            #import metapy doesnt work
            metapy = sys.modules["metapy"]
        else:
            import metapy
            metapy.log_to_stderr()
        # TODO: this code block only runs ONCE. Once the user clicks twice on search the ranker.score(...) runs forever. figuring out why...
        print("1")
        idx = metapy.index.make_inverted_index(Config.CONFIG_TOML)
        print(idx.avg_doc_length())
        print("2")
        ranker = metapy.index.OkapiBM25()
        print("3")
        query = metapy.index.Document()
        print("4")
        query.content("auto")
        print("5")
        top = ranker.score(idx, query, num_results=5)
        print("6")
        print(top)
        #displayedPages = toID - fromID
        # Transform from 1-indexed to 0-indexed
        #fromID = fromID - 1
        #results =[]
        retrievedReports = Report.query
        for (d_id,_) in top:
            results = retrievedReports.filter(Report.id == d_id)
            print (d_id)

        return render_template('ResultPage.html', reports=results)
    return render_template('SearchPage.html', form=form)

@app.route('/browse/<int:fromID>/<int:toID>', methods=['GET', 'POST'])
def browsePage(fromID, toID):
    """A user may browse the police reports."""
    # Initialize forms:
    # 1. Initilaize with default as defiend in class
    # 2. If the page is loaded without a submit, fill it with the value stored in the session
    filterForm = FilterForm(request.form)
    if (not filterForm.validate_on_submit()) and "ordering" in session:
        filterForm.order.data = session["ordering"]
    if (not filterForm.validate_on_submit()) and "classes" in session:
        filterForm.classes.data = session["classes"]

    # TODO: implement error handling (e.g. not too many results at once
    displayedPages = toID - fromID
    # Transform from 1-indexed to 0-indexed
    fromID = fromID - 1
    retrievedReports = Report.query

    # Handle Ordering Filter
    if filterForm.order.data == 'asc':
        session["ordering"]=filterForm.order.data
        retrievedReports = retrievedReports.order_by(asc(Report.date))
    elif filterForm.order.data == 'desc':
        session["ordering"] = filterForm.order.data
        retrievedReports = retrievedReports.order_by(desc(Report.date))
    else:
        session["ordering"] = filterForm.order.data
        retrievedReports = retrievedReports

    # Handle Classes Filter
    if filterForm.classes.data == 'none':
        session["classes"]=filterForm.classes.data
        retrievedReports = retrievedReports
    else:
        session["classes"] = filterForm.classes.data
        retrievedReports = retrievedReports.filter(Report.label==filterForm.classes.data)

    retrievedReports = retrievedReports.limit(toID - fromID) \
        .offset(fromID) \
        .all()
    return render_template('BrowsePage.html', reports=retrievedReports, displayedPages=displayedPages, toID=toID,
                           filterForm=filterForm)

@app.route('/classes', methods=['GET'])
def classes():
    """A user may browse the police reports by a set of categories."""
    # TODO here we need to render pre-classified police reports
    return render_template('Classes.html')

@app.route('/view/<int:id>', methods=['GET'])
def viewPage(id):
    """A user may display an individual report.
    GET Requests expects to get the ID of the report passed in the field 'ID'."""
    retrievedReport = Report.query.filter(Report.id == id).first()
    if not bool(retrievedReport):
        return render_template('ViewPage.html', empty="TRUE")
    else:
        return render_template('ViewPage.html',
                               result="TRUE",
                               title=retrievedReport.title,
                               location=retrievedReport.location,
                               date=retrievedReport.date,
                               event=retrievedReport.event,
                               link=retrievedReport.link)