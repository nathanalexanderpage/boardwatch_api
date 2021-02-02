import os

from boardwatch_models import Game, Platform, PlatformEdition
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

    cur.close()
    conn.close()

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

    cur.close()
    conn.close()

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

    cur.close()
    conn.close()
        
    return all_platforms


def get_editions_by_platform_id(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            pe.id AS id,
            pe.name AS name,
            pe.official_color AS official_color,
            pe.has_matte AS has_matte,
            pe.has_transparency AS has_transparency,
            pe.has_gloss AS has_gloss,
            pe.note AS note,
            pe.image_url AS image_url,
            x.colors,
            p.id AS platform_id
            -- p.name AS platform_name
            FROM platforms AS p
            JOIN platform_editions AS pe ON pe.platform_id = p.id
            JOIN
                (SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors
                FROM platform_editions AS pe
                JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id
                JOIN colors AS c ON c.id = cpe.color_id
                GROUP BY pe.id
                ORDER BY pe.id)
            AS x ON x.id = pe.id
            WHERE p.id = %s
            ORDER BY p.id, name, official_color, colors;
    """, (id,))

    editions = cur.fetchall()

    all_platform_editions = []

    for e in editions:
        current = PlatformEdition(id=e[0], name=e[1], official_color=e[2], has_matte=e[3], has_transparency=e[4], has_gloss=e[5], note=e[6], image_url=e[7])
        current.colors = e[8].split(', ')

        all_platform_editions.append(current)

    cur.close()
    conn.close()
    
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

    cur.close()
    conn.close()

    if e == None:
        return None

    return PlatformEdition(id=e[0], name=e[1], official_color=e[3], has_matte=e[4], has_transparency=e[5], has_gloss=e[6], note=e[7], image_url=e[8])


def get_searched_editions(q):
    conn = get_db_connection()
    cur = conn.cursor()

    like_q = '%' + q + '%'
    data_dict = {
        'q': q,
        'like_q': like_q,
    }

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
        WHERE e.name ILIKE %(like_q)s OR e.official_color ILIKE %(like_q)s
        ORDER BY e.name, e.official_color;
        """, data_dict)

    editions = cur.fetchall()

    all_editions = []

    for e in editions:
        current = PlatformEdition(id=e[0], name=e[1], official_color=e[3], has_matte=e[4], has_transparency=e[5], has_gloss=e[6], note=e[7], image_url=e[8])

        all_editions.append(current)
        
    cur.close()
    conn.close()
        
    return all_editions


def get_all_games():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        g.id,
        g.name,
        g.year_first_release,
        g.is_bootleg
        FROM games as g
        ORDER BY g.name, g.year_first_release;
        """)
    games = cur.fetchall()

    all_games = []

    for g in games:
        current = Game(id=g[0], name=g[1], year_first_release=g[2], is_bootleg=g[3])

        all_games.append(current)

    cur.close()
    conn.close()

    return all_games


def get_game_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        g.id,
        g.name,
        g.year_first_release,
        g.is_bootleg
        FROM games as g
        WHERE g.id=%s LIMIT 1;
        """, (id,))
    g = cur.fetchone()

    cur.close()
    conn.close()

    if g == None:
        return None

    return Game(id=g[0], name=g[1], year_first_release=g[2], is_bootleg=g[3])

def get_searched_games(q):
    conn = get_db_connection()
    cur = conn.cursor()

    like_q = '%' + q + '%'
    data_dict = {
        'q': q,
        'like_q': like_q,
    }

    cur.execute("""
        SELECT
        g.id,
        g.name,
        g.year_first_release,
        g.is_bootleg
        FROM games as g
        WHERE g.name ILIKE %(like_q)s
        ORDER BY g.name, g.year_first_release DESC;
        """, data_dict)

    games = cur.fetchall()

    all_games = []

    for g in games:
        current = Game(id=g[0], name=g[1], year_first_release=g[2], is_bootleg=g[3])

        all_games.append(current)

    cur.close()
    conn.close()
        
    return all_games
