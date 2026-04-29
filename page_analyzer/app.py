import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.database import UrlModel

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    # POST: create
    if request.method == 'POST':
        data = request.form.to_dict()
        url = data['url']
        url_id, status, message = UrlModel.create(url)
        flash(message, status)
        if status == UrlModel.STATUS_ERR:
            return render_template('index.html'), 422
        return redirect(url_for('get_url', id=url_id))

    # GET: list
    return render_template('list.html', urls=UrlModel.all())


@app.route('/urls/<int:id>', methods=['GET'])
def get_url(id):
    url = UrlModel.find(id)
    return render_template('detail.html', url=url)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url = UrlModel.find(id)
    status, message = UrlModel.add_check(id, url['name'])
    flash(message, status)
    return redirect(url_for('get_url', id=id))
