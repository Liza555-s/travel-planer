# Travel Planner

Веб-приложение для планирования путешествий и обмена опытом с другими путешественниками.

## Функциональность

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление постов о путешествиях
- Загрузка изображений к постам
- Лайки и комментарии к постам
- Добавление постов в избранное
- Создание личных заметок
- Поиск по городам и содержимому постов
- Редактирование профиля пользователя
- Адаптивный дизайн

## Технологии

- Python 3.8+
- Flask
- SQLAlchemy
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Font Awesome

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
venv\Scripts\activate

```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные:
```
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///travel.db
```

5. Инициализируйте базу данных:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Запуск

1. Активируйте виртуальное окружение (если еще не активировано):
```bash
venv\Scripts\activate

```

2. Запустите приложение:
```bash
python app.py
```

3. Откройте браузер и перейдите по адресу `http://localhost:5000`

## Структура проекта

```
travel-planner/
├── app.py                 # Основной файл приложения
├── requirements.txt       # Зависимости проекта
├── static/               # Статические файлы
│   ├── css/             # CSS стили
│   ├── js/              # JavaScript файлы
│   ├── uploads/         # Загруженные изображения
│   └── images/          # Изображения сайта
├── templates/           # HTML шаблоны
│   ├── base.html       # Базовый шаблон
│   ├── index.html      # Главная страница
│   ├── login.html      # Страница входа
│   ├── register.html   # Страница регистрации
│   ├── profile.html    # Профиль пользователя
│   ├── create_post.html # Создание поста
│   ├── edit_post.html  # Редактирование поста
│   ├── notes.html      # Заметки
│   └── search.html     # Поиск
└── README.md           # Документация
```

## Разработка

- Для добавления новых моделей используйте Flask-SQLAlchemy
- Для создания миграций используйте Flask-Migrate
- Следуйте PEP 8 для Python кода
- Используйте БЭМ методологию для CSS классов
- Следуйте принципам адаптивного дизайна

## Лицензия

MIT License 