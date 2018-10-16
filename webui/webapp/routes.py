from flask import render_template, request
from webui.webapp import app
from webui.webapp.forms import SearchForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/Search', methods=['GET', 'POST'])
def searchPage():
    form = SearchForm(request.form)
    if form.validate_on_submit(): # Is only called when the form is submitted
        # TODO: here we need to implement the IR functionality
        return render_template('ResultPage.html', results=[form.query.data, "Result2"])
    return render_template('SearchPage.html', form=form)


@app.route('/Classes')
def classes():
    # TODO here we need to render pre-classified police reports
    return render_template('Classes.html')
