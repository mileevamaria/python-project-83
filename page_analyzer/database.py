import os

import psycopg2
import requests
from psycopg2.extras import RealDictCursor

from page_analyzer.parser import parse
from page_analyzer.validator import normalize_url, validate_url


def _db_connect():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


class UrlModel:

    STATUS_ERR = 'danger'
    STATUS_SUC = 'success'
    STATUS_INFO = 'info'

    CREATE_MSG_INFO = 'Страница уже существует'
    CREATE_MSG_SUC = 'Страница успешно добавлена'
    SEO_MSG_ERR = 'Произошла ошибка при проверке'
    SEO_MSG_SUC = 'Страница успешно проверена'

    @staticmethod
    def create(url: str) -> tuple[int | None, str, str]:
        url_id = None

        # validation
        error = validate_url(url)
        if error:
            return url_id, UrlModel.STATUS_ERR, error

        conn = _db_connect()
        cur = conn.cursor()
        url = normalize_url(url)
        try:
            cur.execute('''
                    INSERT INTO urls (name) 
                    VALUES (%s) RETURNING id;
                ''',
                (url,)
            )
            url_id = cur.fetchone()[0]
            status, message = UrlModel.STATUS_SUC, UrlModel.CREATE_MSG_SUC
            conn.commit()

        # unique violated
        except psycopg2.errors.UniqueViolation:
            status, message = UrlModel.STATUS_INFO, UrlModel.CREATE_MSG_INFO
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

    @staticmethod
    def find(id: int) -> dict:
        with _db_connect() as conn:
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


    @staticmethod
    def all() -> list:
        # select url and results of its last check
        with _db_connect() as conn:
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
        
    @staticmethod
    def add_check(id: int, url: str) -> tuple[str, str]:
        status, message = UrlModel.STATUS_ERR, UrlModel.SEO_MSG_ERR

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
        
        status, message = UrlModel.STATUS_SUC, UrlModel.SEO_MSG_SUC
        result = parse(response.text)
        with _db_connect() as conn:
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
