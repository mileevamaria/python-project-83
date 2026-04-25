import psycopg2
from datetime import datetime
from validators.url import url as url_validation_func
from urllib.parse import urlparse

from page_analyzer import db

MAX_URL_LENGTH = 255
DATE_FORMAT = '%Y-%m-%d'


def create(name):
    conn = db.connect()
    cur = conn.cursor()
    url_id, message = None, None
    try:
        cur.execute(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id;",
            (normalize(name),)
        )
        url_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        message = 'Страница уже существует'
        conn.rollback()
    finally:
        message = 'Страница успешно добавлена'
        cur.close()
        conn.close()
    return url_id, message


def find(id: int):
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, created_at FROM urls WHERE id = %s;",
        (id,)
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    return serialize(result)


def all():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, created_at FROM urls ORDER BY id DESC;"
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [serialize(item) for item in results]

def normalize(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def validate(url: str) -> dict:
    errors = {}
    validated_url = url_validation_func(url)
    if validated_url is not True:
        errors['url'] = 'Некорректный url'
    if len(url) > MAX_URL_LENGTH:
        errors['url'] = f'Длина url не может превышать {MAX_URL_LENGTH} символов'
    return errors

def serialize(data: tuple) -> dict:
    (id, name, created_at) = data
    return {
        'id': id,
        'name': name,
        'created_at': datetime.strftime(created_at, DATE_FORMAT),
    }
