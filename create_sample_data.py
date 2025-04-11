from app import app, db
from models import User, Post
from werkzeug.security import generate_password_hash
import datetime

def create_sample_data():
    # Создаем системного пользователя для тестовых постов
    system_user = User.query.filter_by(username='system').first()
    if not system_user:
        system_user = User(
            username='system',
            email='system@example.com',
            password_hash=generate_password_hash('systempass123')
        )
        db.session.add(system_user)
        db.session.commit()

    # Список городов и их описаний
    posts_data = [
        {
            'title': 'Париж - город любви',
            'content': 'Париж - столица Франции, известная своей романтической атмосферой, искусством и архитектурой. Эйфелева башня, Лувр, Нотр-Дам - лишь малая часть достопримечательностей.',
            'city': 'Париж',
            'image_path': 'uploads/paris.jpg'
        },
        {
            'title': 'Токио - город будущего',
            'content': 'Токио - столица Японии, сочетающая в себе современные технологии и древние традиции. Район Сибуя, храм Сэнсо-дзи, Tokyo Skytree.',
            'city': 'Токио',
            'image_path': 'uploads/tokyo.jpg'
        },
        {
            'title': 'Нью-Йорк - город, который никогда не спит',
            'content': 'Нью-Йорк - самый населенный город США, центр культуры, финансов и развлечений. Статуя Свободы, Центральный парк, Таймс-сквер.',
            'city': 'Нью-Йорк',
            'image_path': 'uploads/newyork.jpg'
        },
        {
            'title': 'Рим - вечный город',
            'content': 'Рим - столица Италии, город с богатейшей историей. Колизей, Пантеон, фонтан Треви - символы великой цивилизации.',
            'city': 'Рим',
            'image_path': 'uploads/rome.jpg'
        },
        {
            'title': 'Барселона - жемчужина Каталонии',
            'content': 'Барселона - город Гауди, футбола и пляжей. Саграда Фамилия, Парк Гуэль, Ла Рамбла.',
            'city': 'Барселона',
            'image_path': 'uploads/barcelona.jpg'
        },
        {
            'title': 'Дубай - город будущего в пустыне',
            'content': 'Дубай - современный мегаполис в ОАЭ. Бурдж-Халифа, Palm Jumeirah, Dubai Mall.',
            'city': 'Дубай',
            'image_path': 'uploads/dubai.jpg'
        },
        {
            'title': 'Лондон - город королевской семьи',
            'content': 'Лондон - столица Великобритании. Биг-Бен, Тауэрский мост, Букингемский дворец.',
            'city': 'Лондон',
            'image_path': 'uploads/london.jpg'
        },
        {
            'title': 'Сидней - город у океана',
            'content': 'Сидней - крупнейший город Австралии. Оперный театр, мост Харбор-Бридж, пляж Бонди.',
            'city': 'Сидней',
            'image_path': 'uploads/sydney.jpg'
        },
        {
            'title': 'Амстердам - город каналов',
            'content': 'Амстердам - столица Нидерландов. Музей Ван Гога, Королевский дворец, каналы.',
            'city': 'Амстердам',
            'image_path': 'uploads/amsterdam.jpg'
        },
        {
            'title': 'Стамбул - город двух континентов',
            'content': 'Стамбул - крупнейший город Турции. Айя-София, Голубая мечеть, Гранд-базар.',
            'city': 'Стамбул',
            'image_path': 'uploads/istanbul.jpg'
        }
    ]

    # Создаем посты
    for post_data in posts_data:
        existing_post = Post.query.filter_by(title=post_data['title']).first()
        if not existing_post:
            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                city=post_data['city'],
                image_path=post_data['image_path'],
                author=system_user,
                date_posted=datetime.datetime.now()
            )
            db.session.add(post)

    db.session.commit()
    print("Тестовые данные успешно добавлены!")

if __name__ == '__main__':
    with app.app_context():
        create_sample_data() 