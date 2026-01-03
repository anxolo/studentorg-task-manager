from flask import Flask, redirect, url_for
from sqlalchemy import create_engine
import os

def create_app():
    app = Flask(__name__)

    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SESSION_COOKIE_PATH='/',
        SESSION_COOKIE_NAME='app_session',
        SESSION_COOKIE_SECURE=False, 
        SESSION_COOKIE_HTTPONLY=True,
        PERMANENT_SESSION_LIFETIME=3600
    )

    db_host = os.environ.get('DB_HOST')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')
    
    app.config['SQLALCHEMY_ENGINE'] = create_engine(
        f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}",
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=10,
        max_overflow=20
    )

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.route('/')
    def root():
        return redirect(url_for('main.login'))

    return app

app = create_app()