import psycopg2
import requests

from bs4 import BeautifulSoup
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
from validators.url import url as url_validation_func

from page_analyzer import db

DATE_FORMAT = '%Y-%m-%d'

# validate & create
MAX_URL_LENGTH = 255
VAL_INCORRECT_MSG = 'Некорректный URL'
VAL_INCORRECT_LEN_MSG = (
    f'Длина url не может превышать {MAX_URL_LENGTH} символов')
CREATE_MSG_INFO = 'Страница уже существует'
CREATE_MSG_SUC = 'Страница успешно добавлена'
STATUS_ERR = 'danger'
STATUS_SUC = 'success'
STATUS_INFO = 'info'

# seo
SEO_MSG_ERR = 'Произошла ошибка при проверке'
SEO_MSG_SUC = 'Страница успешно проверена'


def _normalize(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _validate(url: str) -> str:
    error = ''
    validated_url = url_validation_func(url)
    if validated_url is not True:
        return VAL_INCORRECT_MSG
    if len(url) > MAX_URL_LENGTH:
        return VAL_INCORRECT_LEN_MSG
    return error


def _seo(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    result = {}

    # h1
    h1_tag = soup.find('h1')
    result['h1'] = h1_tag.get_text(strip=True) if h1_tag else None

    # title
    title_tag = soup.find('title')
    result['title'] = title_tag.get_text(strip=True) if title_tag else None

    # meta description
    description_tag = soup.find('meta', attrs={'name': 'description'})
    result['description'] = (
        description_tag.get('content').strip()
        if description_tag and description_tag.get('content')
        else None
    )
    return result


def create(url: str) -> tuple[int | None, str, str]:
    url_id = None

    # validation
    error = _validate(url)
    if error:
        return url_id, STATUS_ERR, error

    conn = db.connect()
    cur = conn.cursor()
    url = _normalize(url)
    try:
        cur.execute('''
                INSERT INTO urls (name) 
                VALUES (%s) RETURNING id;
            ''',
            (url,)
        )
        url_id = cur.fetchone()[0]
        status, message = STATUS_SUC, CREATE_MSG_SUC
        conn.commit()

    # unique violated
    except psycopg2.errors.UniqueViolation:
        status, message = STATUS_INFO, CREATE_MSG_INFO
        conn.rollback()
        cur.execute('''
                SELECT id FROM urls WHERE name = %s;
            ''',
            (url,),
        )
        url_id = cur.fetchone()[0]
    
    # close db
    finally:
        cur.close()
        conn.close()
        
    return url_id, status, message


def find(id: int) -> dict:
    with db.connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # get url
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
    
            # checks list for url
            cur.execute('''
                    SELECT 
                        id, 
                        status_code, 
                        h1, 
                        title, 
                        description, 
                        date(created_at) AS created_at
                    FROM url_checks 
                    WHERE url_id = %s
                    ORDER BY id DESC;
                ''',
                (id,),
            )
            data['checks'] = cur.fetchall()
            return data


def all() -> list:
    # select url and results of its last check
    with db.connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                    SELECT DISTINCT ON (u.id)
                        u.id,
                        u.name,
                        uc.status_code AS last_status_code,
                        date(uc.created_at) AS last_created_at
                    FROM urls u
                    LEFT JOIN url_checks uc ON uc.url_id = u.id
                    ORDER BY u.id DESC;
                '''
            )
            results = cur.fetchall()
    return results
    

def add_check(id: int, url: str) -> tuple[str, str]:
    status, message = STATUS_ERR, SEO_MSG_ERR

    try:
        response = requests.get(url)
        status_code = response.status_code
    # other exceptions
    except requests.exceptions.RequestException:
        return status, message

    # 2xx
    try:
        response.raise_for_status()
    # 4xx, 5xx
    except requests.HTTPError:
        return status, message
    
    status, message = STATUS_SUC, SEO_MSG_SUC
    result = _seo(response.text)
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    INSERT INTO url_checks 
                        (url_id, status_code, h1, title, description)
                    VALUES (%s, %s, %s, %s, %s);
                ''',
                (
                    id, status_code, result['h1'], 
                    result['title'], result['description'],
                ),
            )
    return status, message
