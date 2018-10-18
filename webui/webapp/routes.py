"""Defines the URIs which can called in the Flask Webapp and the logic behind."""

from flask import render_template, request
from webui.webapp import app
from webui.webapp.forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/Search', methods=['GET', 'POST'])
def searchPage():
    """On the search page the user may enter a query and get a list of matching police reports returned.

    Returns
    -------
    Returns either a ResultPage.html or a SearchPage.html depending on whether the user call the link with or
    without having submitted the query entry form."""
    form = SearchForm(request.form)
    if form.validate_on_submit(): # Is only called when the form is submitted
        # TODO: here we need to implement the IR functionality
        # ResultPage will parse the items in results and output them.
        return render_template('ResultPage.html', results=[form.query.data, "Result2"])
    return render_template('SearchPage.html', form=form)


@app.route('/Classes')
def classes():
    """A user may browse the police reports by a set of categories."""
    # TODO here we need to render pre-classified police reports
    return render_template('Classes.html')
