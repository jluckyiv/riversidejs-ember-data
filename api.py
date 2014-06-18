#!/usr/bin/env python
import os
import json
import argparse
import psycopg2
from psycopg2.extras import DictCursor
from bottle import (Bottle,
                    request,
                    response,
                    run,
                    get,
                    post,
                    static_file)


DSN = os.getenv('DATABASE_URL', 'dbname=moviedb')
SITE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
ASSETS_ROOT = os.path.join(SITE_ROOT, 'assets')

app = Bottle()

def init_db():
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()

    # create tables
    cur.execute('CREATE TABLE IF NOT EXISTS movie '
                '(id serial primary key, data json)')

    cur.execute('CREATE TABLE IF NOT EXISTS goof '
                '(id serial primary key, '
                'movie integer references movie (id), data json)')

    conn.commit()


def record_to_dict(record):
    tmp = record.copy()
    data = tmp.pop('data')
    return dict(tmp.items() + data.items())


@app.hook('before_request')
def db_conn():
    if request.path.startswith('/assets/'):
        return

    conn = psycopg2.connect(DSN, cursor_factory=DictCursor)
    request.db = conn


@app.hook('after_request')
def db_close():
    if request.path.startswith('/assets/'):
        return

    request.db.close()


@app.hook('after_request')
def json_content_type():
    response.content_type = 'application/json'


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept, X-Requested-With'
    response.headers['Access-Control-Max-Age'] = '1000'


@app.route('/api/movies', method=['GET', 'OPTIONS'])
def movies():
    cur = request.db.cursor()
    cur.execute('WITH goofs AS (SELECT array_agg(id) as ids, movie '
                'FROM goof GROUP BY movie) '
                'SELECT movie.id, movie.data, '
                '(SELECT array_to_json(coalesce(array_agg(a), \'{}\')) FROM unnest(goofs.ids) a '
                'WHERE a IS NOT NULL) goofs '
                'FROM movie LEFT JOIN goofs ON movie.id = goofs.movie')
    results = cur.fetchall()
    return {
        'movie': [record_to_dict(r) for r in results]
    }


@app.get('/api/movies/<id:int>')
def get_movie(id):
    cur = request.db.cursor()
    # i'm too lazy to write a different query
    cur.execute('WITH goofs AS (SELECT array_agg(id) as ids, movie '
                'FROM goof GROUP BY movie) '
                'SELECT movie.id, movie.data, '
                '(SELECT array_to_json(coalesce(array_agg(a), \'{}\')) FROM unnest(goofs.ids) a '
                'WHERE a IS NOT NULL) goofs '
                'FROM movie LEFT JOIN goofs ON movie.id = goofs.movie '
                'WHERE movie.id = %s', [id])
    result = cur.fetchone()
    return {
        'movie': record_to_dict(result)
    }


@app.post('/api/movies')
def new_movie():
    movie = request.json['movie']
    cur = request.db.cursor()
    cur.execute('INSERT INTO movie (data) VALUES (%s) '
                'RETURNING id, data', [json.dumps(movie)])
    result = cur.fetchone()
    request.db.commit()
    return {
        'movie': record_to_dict(result)
    }


@app.route('/api/goofs', method=['GET', 'OPTIONS'])
def goofs():
    ids = request.query.getall('ids[]')
    cur = request.db.cursor()

    if ids:
        cur.execute('SELECT id, movie, data FROM goof WHERE id in %s', [tuple(ids)])
    else:
        cur.execute('SELECT id, movie, data FROM goof')

    results = cur.fetchall()
    return {
        'goof': [record_to_dict(r) for r in results]
    }


@app.get('/api/goofs/<id:int>')
def get_goof(id):
    cur = request.db.cursor()
    cur.execute('SELECT id, movie, data FROM goof WHERE id = %s', [id])
    result = cur.fetchone()
    request.db.commit()
    return {
        'goof': record_to_dict(result)
    }


@app.post('/api/goofs')
def new_goof():
    goof = request.json['goof']
    cur = request.db.cursor()
    movie_id = goof.pop('movie')

    cur.execute('INSERT INTO goof (movie, data) VALUES '
                '(%s, %s) RETURNING id, movie, data', [movie_id, json.dumps(goof)])
    result = cur.fetchone()
    request.db.commit()

    return {
        'goof': record_to_dict(result)
    }


@app.get('/')
def index():
    return static_file('index.html', SITE_ROOT)


@app.get('/assets/<path:path>')
def static(path):
    return static_file(path, ASSETS_ROOT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Movie DB API')
    parser.add_argument('--init-db',
                        dest='init_db',
                        action='store_true',
                        help='Initialize database tables')

    args = parser.parse_args()
    if args.init_db:
        init_db()
    else:
        run(app, host='0.0.0.0', debug=True, port=os.getenv('PORT', 8080))
