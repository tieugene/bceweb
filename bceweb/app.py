import os.path

import psycopg2
from flask import Flask

from . import routes, vars


def init_db(app):
    vars.CONN = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASS'])


def create_app():
    # utils.init_cfg()
    cfg_file = '/etc/bceweb.cfg' if os.path.isfile('/etc/bceweb.cfg') else 'bceweb.cfg'
    app = Flask(__name__)
    app.config.from_pyfile(cfg_file)
    app.register_blueprint(routes.bp)
    init_db(app)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
