from app import app, db
from models import Place
import os

def create_places():
    # Создаем директорию для изображений мест, если она не существует
    places_images_dir = os.path.join('static', 'uploads', 'places')
    os.makedirs(places_images_dir, exist_ok=True)

    places_data = [
        {
            'name': 'Красная площадь',
            'city': 'Москва',
            'image_path': 'uploads/places/red_square.jpg',
            'description': 'Главная площадь Москвы, исторический центр города'
        },
        {
            'name': 'Эрмитаж',
            'city': 'Санкт-Петербург',
            'image_path': 'uploads/places/hermitage.jpg',
            'description': 'Один из крупнейших музеев мира'
        },
        {
            'name': 'Озеро Байкал',
            'city': 'Иркутск',
            'image_path': 'uploads/places/baikal.jpg',
            'description': 'Самое глубокое озеро на планете'
        },
        {
            'name': 'Долина гейзеров',
            'city': 'Петропавловск-Камчатский',
            'image_path': 'uploads/places/geysers.jpg',
            'description': 'Уникальный природный комплекс'
        },
        {
            'name': 'Кижи',
            'city': 'Петрозаводск',
            'image_path': 'uploads/places/kizhi.jpg',
            'description': 'Музей-заповедник деревянного зодчества'
        },
        {
            'name': 'Соловецкий монастырь',
            'city': 'Архангельск',
            'image_path': 'uploads/places/solovki.jpg',
            'description': 'Древний монастырский комплекс'
        },
        {
            'name': 'Плато Путорана',
            'city': 'Норильск',
            'image_path': 'uploads/places/putorana.jpg',
            'description': 'Уникальное базальтовое плато'
        },
        {
            'name': 'Куршская коса',
            'city': 'Калининград',
            'image_path': 'uploads/places/curonian_spit.jpg',
            'description': 'Песчаная коса между Балтийским морем и Куршским заливом'
        },
        {
            'name': 'Алтайские горы',
            'city': 'Горно-Алтайск',
            'image_path': 'uploads/places/altai.jpg',
            'description': 'Горная система в Центральной Азии'
        },
        {
            'name': 'Ключевская сопка',
            'city': 'Петропавловск-Камчатский',
            'image_path': 'uploads/places/kluchevskaya.jpg',
            'description': 'Самый высокий действующий вулкан Евразии'
        },
        {
            'name': 'Телецкое озеро',
            'city': 'Горно-Алтайск',
            'image_path': 'uploads/places/teletskoye.jpg',
            'description': 'Крупнейшее озеро Алтая'
        },
        {
            'name': 'Домбай',
            'city': 'Черкесск',
            'image_path': 'uploads/places/dombay.jpg',
            'description': 'Горнолыжный курорт в Карачаево-Черкесии'
        },
        {
            'name': 'Валдайский национальный парк',
            'city': 'Валдай',
            'image_path': 'uploads/places/valday.jpg',
            'description': 'Уникальный природный комплекс'
        },
        {
            'name': 'Остров Врангеля',
            'city': 'Певек',
            'image_path': 'uploads/places/wrangel.jpg',
            'description': 'Заповедник в Северном Ледовитом океане'
        },
        {
            'name': 'Кунгурская ледяная пещера',
            'city': 'Кунгур',
            'image_path': 'uploads/places/kungur.jpg',
            'description': 'Одна из самых популярных достопримечательностей Урала'
        },
        {
            'name': 'Озеро Селигер',
            'city': 'Осташков',
            'image_path': 'uploads/places/seliger.jpg',
            'description': 'Система озёр ледникового происхождения'
        },
        {
            'name': 'Водопад Кивач',
            'city': 'Петрозаводск',
            'image_path': 'uploads/places/kivach.jpg',
            'description': 'Один из крупнейших равнинных водопадов Европы'
        },
        {
            'name': 'Лотосовые поля',
            'city': 'Астрахань',
            'image_path': 'uploads/places/lotus.jpg',
            'description': 'Уникальное природное явление в дельте Волги'
        },
        {
            'name': 'Красноярские Столбы',
            'city': 'Красноярск',
            'image_path': 'uploads/places/stolby.jpg',
            'description': 'Заповедник со скальными останцами'
        },
        {
            'name': 'Озеро Эльтон',
            'city': 'Волгоград',
            'image_path': 'uploads/places/elton.jpg',
            'description': 'Крупнейшее соленое озеро Европы'
        }
    ]

    with app.app_context():
        for place_data in places_data:
            place = Place.query.filter_by(name=place_data['name']).first()
            if not place:
                place = Place(**place_data)
                db.session.add(place)
        
        db.session.commit()

if __name__ == '__main__':
    create_places() 