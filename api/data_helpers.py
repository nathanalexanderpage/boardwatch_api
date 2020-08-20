import os

from boardwatch_models import Platform, PlatformEdition
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

    cur.execute("""
        SELECT
        p.id as id,
        p.name as name,
        p.is_brand_missing as is_brand_missing,
        pf.id as platform_family_id,
        pf.name as platform_family_name,
        p.model_no as model_no,
        p.storage_capacity as storage_capacity,
        p.description as description,
        p.disambiguation as disambiguation,
        p.relevance as relevance
        FROM platforms as p
        JOIN platform_families as pf ON pf.id = p.platform_family_id
        ORDER BY p.relevance DESC;
        """)
    platforms = cur.fetchall()

    all_platforms = []

    for p in platforms:
        current = Platform(id=p[0], name=p[1], is_brand_missing_from_name=p[2], platform_family_id=p[3], platform_family_name=p[4], model_no=p[5], storage_capacity=p[6], description=p[7], disambiguation=p[8], relevance=p[9])

        all_platforms.append(current)

    return all_platforms


def get_platform_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        p.id as id,
        p.name as name,
        p.is_brand_missing as is_brand_missing,
        pf.id as platform_family_id,
        pf.name as platform_family_name,
        p.model_no as model_no,
        p.storage_capacity as storage_capacity,
        p.description as description,
        p.disambiguation as disambiguation,
        p.relevance as relevance
        FROM platforms as p JOIN platform_families as pf ON pf.id = p.platform_family_id
        WHERE p.id=%s LIMIT 1;
        """, (id,))
    p = cur.fetchone()

    if p == None:
        return None

    return Platform(id=p[0], name=p[1], is_brand_missing_from_name=p[2], platform_family_id=p[3], platform_family_name=p[4], model_no=p[5], storage_capacity=p[6], description=p[7], disambiguation=p[8], relevance=p[9])

def get_searched_platforms(q=''):
    conn = get_db_connection()
    cur = conn.cursor()

    like_q = '%' + q + '%'
    data_dict = {
        'q': q,
        'like_q': like_q,
    }

    cur.execute("""
        SELECT
        p.id as id,
        p.name as name,
        p.is_brand_missing as is_brand_missing,
        pf.id as platform_family_id,
        pf.name as platform_family_name, 
        p.model_no as model_no,
        p.storage_capacity as storage_capacity,
        p.description as description,
        p.disambiguation as disambiguation,
        p.relevance as relevance
        FROM platforms as p JOIN platform_families as pf ON pf.id = p.platform_family_id
        WHERE p.name ILIKE %(like_q)s OR p.model_no ILIKE %(like_q)s
        ORDER BY p.relevance DESC;
        """, data_dict)

    platforms = cur.fetchall()

    all_platforms = []

    for p in platforms:
        current = Platform(id=p[0], name=p[1], is_brand_missing_from_name=p[2], platform_family_id=p[3], platform_family_name=p[4], model_no=p[5], storage_capacity=p[6], description=p[7], disambiguation=p[8], relevance=p[9])

        all_platforms.append(current)
        
    return all_platforms

def get_editions_by_platform_id(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        pe.id,
        pe.name,
        pe.platform_id,
        pe.official_color,
        pe.has_matte,
        pe.has_transparency,
        pe.has_gloss,
        pe.note,
        pe.image_url
        FROM platform_editions as pe
        JOIN platforms as p ON pe.platform_id = p.id
        WHERE pe.platform_id = %s;
        """, (id,))

    editions = cur.fetchall()

    all_platform_editions = []

    for e in editions:
        current = PlatformEdition(id=e[0], name=e[1], official_color=e[3], has_matte=e[4], has_transparency=e[5], has_gloss=e[6], note=e[7], image_url=e[8])

        all_platform_editions.append(current)
    
    return all_platform_editions


def get_edition_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        e.id,
        e.name,
        e.platform_id,
        e.official_color,
        e.has_matte,
        e.has_transparency,
        e.has_gloss,
        e.note,
        e.image_url
        FROM platform_editions as e
        WHERE e.id=%s LIMIT 1;
        """, (id,))
    e = cur.fetchone()

    if e == None:
        return None

    return PlatformEdition(id=e[0], name=e[1], official_color=e[3], has_matte=e[4], has_transparency=e[5], has_gloss=e[6], note=e[7], image_url=e[8])
