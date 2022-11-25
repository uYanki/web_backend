import os
import sqlite3

from flask import current_app, g


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        if not os.path.exists(current_app.config['DATABASE']):
            init_db()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # 获取数据库路径
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e):
    db = g.pop('db', None)
    # print('db.py - close_db')
    if db is not None:
        db.close()
