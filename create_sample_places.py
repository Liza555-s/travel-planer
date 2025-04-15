from app import create_app
from models import db, Place
import os

app = create_app()

with app.app_context():
    # Очищаем таблицу мест
    Place.query.delete()
    
    # Создаем директорию для изображений мест, если она не существует
    places_images_dir = os.path.join('static', 'uploads', 'places')
    os.makedirs(places_images_dir, exist_ok=True)

    # Список популярных мест в России
    places = [
        {
            'name': 'Красная площадь',
            'city': 'Москва',
            'country': 'Россия',
            'description': 'Главная площадь Москвы, расположенная в центре города. Здесь находятся Кремль, Собор Василия Блаженного и другие исторические памятники.'
        },
        {
            'name': 'Эрмитаж',
            'city': 'Санкт-Петербург',
            'country': 'Россия',
            'description': 'Один из крупнейших музеев мира, расположенный в Санкт-Петербурге. Его коллекция насчитывает более 3 миллионов произведений искусства.'
        },
        {
            'name': 'Озеро Байкал',
            'city': 'Иркутск',
            'country': 'Россия',
            'description': 'Самое глубокое озеро в мире и крупнейший природный резервуар пресной воды. Его уникальная экосистема поражает воображение.'
        },
        {
            'name': 'Кижи',
            'city': 'Петрозаводск',
            'country': 'Россия',
            'description': 'Музей-заповедник под открытым небом, где собраны уникальные памятники деревянного зодчества Русского Севера.'
        },
        {
            'name': 'Долина гейзеров',
            'city': 'Петропавловск-Камчатский',
            'country': 'Россия',
            'description': 'Уникальное природное явление, где на небольшой территории сосредоточено множество горячих источников и гейзеров.'
        },
        {
            'name': 'Сочи Парк',
            'city': 'Сочи',
            'country': 'Россия',
            'description': 'Первый тематический парк в России, расположенный в Олимпийском парке Сочи.'
        },
        {
            'name': 'Кунгурская пещера',
            'city': 'Кунгур',
            'country': 'Россия',
            'description': 'Одна из самых известных пещер России, известная своими ледяными образованиями.'
        },
        {
            'name': 'Петергоф',
            'city': 'Санкт-Петербург',
            'country': 'Россия',
            'description': 'Дворцово-парковый ансамбль, известный своими фонтанами и дворцами.'
        },
        {
            'name': 'Куршская коса',
            'city': 'Калининград',
            'country': 'Россия',
            'description': 'Уникальный природный заповедник, включенный в список Всемирного наследия ЮНЕСКО.'
        },
        {
            'name': 'Алмазный карьер Мир',
            'city': 'Мирный',
            'country': 'Россия',
            'description': 'Один из крупнейших алмазных карьеров в мире, глубиной более 500 метров.'
        },
        {
            'name': 'Домбай',
            'city': 'Карачаевск',
            'country': 'Россия',
            'description': 'Популярный горнолыжный курорт на Северном Кавказе.'
        },
        {
            'name': 'Плато Путорана',
            'city': 'Норильск',
            'country': 'Россия',
            'description': 'Уникальное плато с множеством водопадов и озер, включенное в список Всемирного наследия ЮНЕСКО.'
        },
        {
            'name': 'Волгоградская панорама',
            'city': 'Волгоград',
            'country': 'Россия',
            'description': 'Музей-панорама, посвященный Сталинградской битве.'
        },
        {
            'name': 'Кировский парк',
            'city': 'Екатеринбург',
            'country': 'Россия',
            'description': 'Один из старейших парков города с богатой историей и красивыми пейзажами.'
        },
        {
            'name': 'Остров Валаам',
            'city': 'Сортавала',
            'country': 'Россия',
            'description': 'Остров в Ладожском озере, известный своим монастырем и уникальной природой.'
        }
    ]
    
    # Добавляем места в базу данных
    for place_data in places:
        place = Place(**place_data)
        db.session.add(place)
    
    # Сохраняем изменения
    db.session.commit()
    
    print('Тестовые места успешно добавлены в базу данных!')

if __name__ == '__main__':
    create_places() 