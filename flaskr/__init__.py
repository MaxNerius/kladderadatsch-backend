import os
from flask import Flask

from . import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # close the database connection on app teardown
    app.teardown_appcontext(db.close_db)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        return 'Henlo!'

    @app.route('/notes')
    def notes():
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * from notes;')
        results = cursor.fetchall()
        cursor.close()

        return f"got {results} from the db!"

    return app
