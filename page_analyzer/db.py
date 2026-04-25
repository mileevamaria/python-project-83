import psycopg2
import os

DATABASE_URL = os.getenv('DATABASE_URL')


def connect():
    return psycopg2.connect(DATABASE_URL)
