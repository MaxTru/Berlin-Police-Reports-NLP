"""Defines the URIs which can called in the Flask Webapp and the logic behind."""

from flask import render_template, request, session
from webui.webapp import app
from webui.webapp.forms import SearchForm, FilterForm
from webui.database.models import Report
from sqlalchemy import and_, desc, asc
from webui.flaskconfig import Config
import subprocess
import re

@app.route('/', methods=['GET'])
@app.route('/search', methods=['GET'])
def searchPage():
    """On the search page the user may enter a query.
    Returns
    -------
    Returns the SearchPage.html with the initialized query form."""
    form = SearchForm(request.form)
    return render_template('SearchPage.html', form=form)

@app.route('/search', methods=['POST'])
def searchPageResults():
    """After having searched, the user receives a result page with the search results.
    Returns
    -------
    Returns ResultPage.html with the query results (docs)."""
    form = SearchForm(request.form)
    if form.validate_on_submit():
        # This is a hack, but when running metapy directly in Flask is runs forever. This is why I run it as \
        # a separate process
        proc = subprocess.Popen(["python", "search/searcher.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        proc.stdin.write(form.query.data.encode("utf-8").strip() + "\n")
        proc.stdin.close()
        while proc.returncode is None:
            proc.poll()
        results = proc.stdout.read()
        print("Retrieved reports and ranking: " + results.splitlines()[0])
        relevantIDs = re.findall("\d+L", results.splitlines()[0])
        relevantReport = Report.query
        result = []
        for x in relevantIDs:
            result.append(relevantReport.filter(Report.id == int(long(x))).first())
        labelCaptions = Config.LABEL_CAPTIONS
        return render_template('ResultPage.html', reports=result, labelCaptions=labelCaptions)
    else:
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