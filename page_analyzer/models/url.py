import psycopg2
from psycopg2.extras import RealDictCursor
from validators.url import url as url_validation_func
from urllib.parse import urlparse

from page_analyzer import db

MAX_URL_LENGTH = 255
DATE_FORMAT = '%Y-%m-%d'


def create(name: str) -> tuple[int | None, str]:
    conn = db.connect()
    cur = conn.cursor()
    url_id, message = None, None
    try:
        cur.execute('''
                INSERT INTO urls (name) 
                VALUES (%s) RETURNING id;
            ''',
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


def find(id: int) -> dict:
    conn = db.connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
            SELECT 
                id, name, date(created_at) AS created_at
            FROM urls 
            WHERE id = %s;
        ''',
        (id,),
    )
    data = cur.fetchone()
    if not data:
        return {}
    
    cur.execute('''
            SELECT 
                id, 
                status_code, 
                h1, 
                title, 
                description, 
                date(created_at) AS checked_at
            FROM url_checks 
            WHERE url_id = %s
            ORDER BY checked_at DESC;
        ''',
        (id,),   
    )
    checks = cur.fetchall()
    cur.close()
    conn.close()
    data['checks'] = checks
    return data


def all() -> list:
    conn = db.connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
            SELECT DISTINCT ON (u.id)
                u.id,
                u.name,
                uc.status_code AS last_status_code,
                date(uc.created_at) AS last_created_at
            FROM urls u
            LEFT JOIN url_checks uc ON uc.url_id = u.id
            ORDER BY u.id, last_created_at DESC;
        '''
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


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


def add_check(id: int) -> None:
    conn = db.connect()
    cur = conn.cursor()
    cur.execute('''
            INSERT INTO url_checks (url_id)
            VALUES (%s);
        ''',
        (id,),
    )
    conn.commit()
    cur.close()
    conn.close()
