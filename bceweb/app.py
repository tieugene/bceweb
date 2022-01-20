from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wertyuiop'
    from bceweb.routes import bp
    app.register_blueprint(bp)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
