from flask import Flask
import os

from extensions import db, login_manager, migrate
from models import User
from routes import bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['AVATAR_FOLDER'] = os.path.join('static', 'avatars')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Создаем директории для загрузки файлов
    for folder in [app.config['UPLOAD_FOLDER'], app.config['AVATAR_FOLDER']]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Регистрация Blueprint
    app.register_blueprint(bp)

    # Создаем базу данных, если она не существует
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 