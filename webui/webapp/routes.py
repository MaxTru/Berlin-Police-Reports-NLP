"""Defines the URIs which can called in the Flask Webapp and the logic behind."""

from flask import render_template, request, session
from webui.webapp import app
from webui.webapp.forms import SearchForm, OrderingForm, ClassesForm
from utils import policeReportUtils as utils
from webui import flaskconfig
from webui.database.models import Report
from sqlalchemy import and_, desc, asc
import os
import metapy

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
        # TODO: here we need to implement the IR functionality
        # TODO this should be configurd in the config file flaskconfig.oy and not directly in code
        cfg = os.path.abspath("./search/config.toml")
        # TODO: the indexation should not be performed at runtime (the user would wait forever in this case). I think we should do this when the Flask Server starts up.
        idx = metapy.index.make_inverted_index(cfg)
        print("Index was built....")
        query = metapy.index.Document()
        print("Query initilaized...")
        ranker = metapy.index.OkapiBM25(k1=2,b=0.65,k3=500)
        #TODO: next two lines run forever. I dont know why.
        print("Ranker initilaized...")
        query.content(form.query.data)
        print("Query content filled...")
        results = ranker.score(idx, query, 10)
        print("Results created...")
        # ResultPage will parse the items in results and output them.
        return render_template('ResultPage.html', results=[form.query.data, "Result2"])
    return render_template('SearchPage.html', form=form)

@app.route('/browse/<int:fromID>/<int:toID>', methods=['GET', 'POST'])
def browsePage(fromID, toID):
    """A user may browse the police reports."""
    # Initialize forms:
    # 1. Initilaize with default as defiend in class
    # 2. If the page is loaded without a submit, fill it with the value stored in the session
    orderingForm = OrderingForm(request.form)
    if (not orderingForm.validate_on_submit()) and "ordering" in session:
        orderingForm.order.data = session["ordering"]
    classesForm = ClassesForm(request.form)
    if (not classesForm.validate_on_submit()) and "classes" in session:
        classesForm.classes.data = session["classes"]

    # TODO: implement error handling (e.g. not too many results at once
    displayedPages = toID - fromID
    # Transform from 1-indexed to 0-indexed
    fromID = fromID - 1
    retrievedReports = Report.query

    # Handle Ordering Filter
    if orderingForm.order.data == 'asc':
        session["ordering"]=orderingForm.order.data
        retrievedReports = retrievedReports.order_by(asc(Report.date))
    elif orderingForm.order.data == 'desc':
        session["ordering"] = orderingForm.order.data
        retrievedReports = retrievedReports.order_by(desc(Report.date))
    else:
        session["ordering"] = orderingForm.order.data
        retrievedReports = retrievedReports

    # Handle Classes Filter
    if classesForm.classes.data == 'none':
        session["classes"]=classesForm.classes.data
        retrievedReports = retrievedReports
    else:
        session["classes"] = classesForm.classes.data
        retrievedReports = retrievedReports.filter(Report.label==classesForm.classes.data)

    retrievedReports = retrievedReports.limit(toID - fromID) \
        .offset(fromID) \
        .all()
    return render_template('BrowsePage.html', reports=retrievedReports, displayedPages=displayedPages, toID=toID,
                           orderingForm=orderingForm, classesForm=classesForm)

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