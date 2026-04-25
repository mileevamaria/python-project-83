import os

from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for

from .models import url as url_model


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/urls/', methods=['GET', 'POST'])
def urls():
    # Создание url
    if request.method == 'POST':
        data = request.form.to_dict()
        url = data['url']
        errors = url_model.validate(url)
        status = 'error'
        if errors:
            flash(errors['url'], status)
            return render_template('index.html'), 422

        url_id, message = url_model.create(url)
        if url_id is None:
            flash(message, status)
            return redirect('/')
        status = 'success'
        flash(message, status)
        return redirect(url_for('get_url', id=url_id))

    # Список urls
    else:
        urls = url_model.all()
        return render_template('list.html', urls=urls)


@app.route('/urls/<int:id>/', methods=['GET'])
def get_url(id):
    url = url_model.find(id)
    return render_template('detail.html', url=url)

