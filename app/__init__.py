from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_basicauth import BasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
basic_auth = BasicAuth()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ---------------------------------------------------------
    # Basic認証の設定 (クラウド等での覗き見・不正アクセス防止)
    # .env ファイルに USERNAME と PASSWORD を設定して使います。
    # 設定されていない場合は、デフォルトで admin / secret になります。
    # ---------------------------------------------------------
    app.config['BASIC_AUTH_USERNAME'] = os.environ.get('AUTH_USERNAME', 'admin')
    app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('AUTH_PASSWORD', 'secret')
    # すべてのページに強制的にパスワードをかける
    app.config['BASIC_AUTH_FORCE'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    basic_auth.init_app(app)

    # 開発環境でHTTPSが使えない場合やテスト用の設定（必要な場合）
    # @app.before_request
    # def require_basic_auth():
    #    pass

    from app.models import Client

    from app.routes.main import main_bp
    from app.routes.clients import clients_bp
    from app.routes.settings import settings_bp
    from app.routes.mail import mail_bp
    from app.routes.appointments import appointments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(mail_bp)
    app.register_blueprint(appointments_bp)

    return app
