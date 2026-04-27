import os

from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for

from .models import url as url_model


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/',  methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    # POST: create
    if request.method == 'POST':
        data = request.form.to_dict()
        url = data['url']
        url_id, status, message = url_model.create(url)
        flash(message, status)
        if status == url_model.STATUS_ERR:
            return render_template('index.html'), 422
        return redirect(url_for('get_url', id=url_id))

    # GET: list
    else:
        return render_template('list.html', urls=url_model.all())


@app.route('/urls/<int:id>', methods=['GET'])
def get_url(id):
    url = url_model.find(id)
    print(f'url: {url}')
    return render_template('detail.html', url=url)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url = url_model.find(id)
    if not url:
        return redirect(url_for('get_url', id=id)), 404
    status, message = url_model.add_check(id, url['name'])
    flash(message, status)
    return redirect(url_for('get_url', id=id))
