import os

from boardwatch_models import Platform
from dotenv import find_dotenv, load_dotenv
import psycopg2 as db


load_dotenv(dotenv_path=find_dotenv())
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')


def get_db_connection():
    return db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)


def get_all_platforms():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT p.id as id, p.name as name, p.is_brand_missing as is_brand_missing, pf.id as platform_family_id, pf.name as platform_family_name, p.model_no as model_no, p.storage_capacity as storage_capacity, p.description as description, p.disambiguation as disambiguation, p.relevance as relevance FROM platforms as p JOIN platform_families as pf ON pf.id = p.platform_family_id;')
    platforms = cur.fetchall()

    all_platforms = []

    for p in platforms:
        current = Platform(id=p[0], name=p[1], is_brand_missing_from_name=p[2], platform_family_id=p[3], platform_family_name=p[4], model_no=p[5], storage_capacity=p[6], description=p[7], disambiguation=p[8], relevance=p[9])

        all_platforms.append(current)

    return all_platforms


def get_platform_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT p.id as id, p.name as name, p.is_brand_missing as is_brand_missing, pf.id as platform_family_id, pf.name as platform_family_name, p.model_no as model_no, p.storage_capacity as storage_capacity, p.description as description, p.disambiguation as disambiguation, p.relevance as relevance FROM platforms as p JOIN platform_families as pf ON pf.id = p.platform_family_id WHERE p.id=%s LIMIT 1;', (id,))
    p = cur.fetchone()

    if p == None:
        return None

    return Platform(id=p[0], name=p[1], is_brand_missing_from_name=p[2], platform_family_id=p[3], platform_family_name=p[4], model_no=p[5], storage_capacity=p[6], description=p[7], disambiguation=p[8], relevance=p[9])
