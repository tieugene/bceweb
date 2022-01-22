# 1. std
import os.path
# 2. 3rd
from flask import Flask
# 3. local
from . import routes


def create_app():
    # utils.init_cfg()
    cfg_file = '/etc/bceweb.cfg' if os.path.isfile('/etc/bceweb.cfg') else 'bceweb.cfg'
    app = Flask(__name__)
    app.config.from_pyfile(cfg_file)
    app.register_blueprint(routes.bp)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
