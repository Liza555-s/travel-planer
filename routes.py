from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from extensions import db
from models import User, Post, Like, Comment, Note, Place, PlaceFavorite
import os
from datetime import datetime
from sqlalchemy import or_

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=12)
    
    # Если нет постов, создаем тестовые данные
    if not posts.items:
        # Создаем тестового пользователя
        test_user = User.query.filter_by(username='test_user').first()
        if not test_user:
            test_user = User(
                username='test_user',
                email='test@example.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(test_user)
            db.session.commit()
        
        # Создаем тестовые места
        places = [
            Place(name='Красная площадь', city='Москва', country='Россия'),
            Place(name='Эрмитаж', city='Санкт-Петербург', country='Россия'),
            Place(name='Озеро Байкал', city='Иркутск', country='Россия'),
            Place(name='Кижи', city='Петрозаводск', country='Россия'),
            Place(name='Долина гейзеров', city='Петропавловск-Камчатский', country='Россия')
        ]
        
        for place in places:
            if not Place.query.filter_by(name=place.name).first():
                db.session.add(place)
        
        # Создаем тестовые посты
        test_posts = [
            {
                'title': 'Красота Красной площади',
                'content': 'Красная площадь - это сердце Москвы и один из самых узнаваемых символов России. Здесь находится множество исторических памятников, включая Собор Василия Блаженного и Кремль.',
                'city': 'Москва',
                'place': places[0]
            },
            {
                'title': 'Величественный Эрмитаж',
                'content': 'Эрмитаж - один из крупнейших музеев мира, расположенный в Санкт-Петербурге. Его коллекция насчитывает более 3 миллионов произведений искусства.',
                'city': 'Санкт-Петербург',
                'place': places[1]
            },
            {
                'title': 'Жемчужина Сибири - Байкал',
                'content': 'Озеро Байкал - самое глубокое озеро в мире и крупнейший природный резервуар пресной воды. Его уникальная экосистема поражает воображение.',
                'city': 'Иркутск',
                'place': places[2]
            },
            {
                'title': 'Деревянное зодчество Кижей',
                'content': 'Кижи - это музей-заповедник под открытым небом, где собраны уникальные памятники деревянного зодчества Русского Севера.',
                'city': 'Петрозаводск',
                'place': places[3]
            },
            {
                'title': 'Природное чудо Камчатки',
                'content': 'Долина гейзеров - это уникальное природное явление, где на небольшой территории сосредоточено множество горячих источников и гейзеров.',
                'city': 'Петропавловск-Камчатский',
                'place': places[4]
            }
        ]
        
        for post_data in test_posts:
            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                city=post_data['city'],
                user_id=test_user.id,
                place_id=post_data['place'].id
            )
            db.session.add(post)
        
        db.session.commit()
        
        # Обновляем запрос постов
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=12)
    
    return render_template('index.html', posts=posts)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Проверка на существующего пользователя
        user_by_username = User.query.filter_by(username=username).first()
        if user_by_username:
            flash('Пользователь с таким именем уже существует', 'error')
            return redirect(url_for('main.register'))
            
        # Проверка на существующий email
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('main.register'))
        
        try:
            new_user = User(username=username, 
                          email=email,
                          password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.', 'error')
            return redirect(url_for('main.register'))
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.index'))
        
        flash('Неверное имя пользователя или пароль')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        city = request.form.get('city')
        place_id = request.form.get('place_id')
        place_name = request.form.get('place_name')
        image = request.files.get('image')

        if not all([title, content, city]):
            flash('Пожалуйста, заполните все обязательные поля', 'error')
            return redirect(url_for('main.create_post'))

        # Создаем пост
        post = Post(
            title=title,
            content=content,
            user_id=current_user.id,
            city=city  # Добавляем город
        )

        # Обрабатываем место, если оно указано
        if place_id:
            place = Place.query.get(place_id)
            if place:
                post.place_id = place.id
        elif place_name:
            # Проверяем, существует ли уже такое место в этом городе
            existing_place = Place.query.filter_by(name=place_name, city=city).first()
            if existing_place:
                post.place_id = existing_place.id
            else:
                place = Place(name=place_name, city=city)
                db.session.add(place)
                db.session.commit()
                post.place_id = place.id

        # Обрабатываем изображение
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            post.image_path = filename

        db.session.add(post)
        db.session.commit()

        flash('Пост успешно создан!', 'success')
        return redirect(url_for('main.index'))

    # Для GET запроса получаем список мест
    places = Place.query.all()
    return render_template('create_post.html', places=places)

@bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('У вас нет прав для редактирования этого поста', 'error')
        return redirect(url_for('main.post_detail', post_id=post_id))
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.city = form.city.data
        post.place = form.place.data
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(filepath)
            post.image_path = filename
        
        db.session.commit()
        flash('Пост успешно обновлен', 'success')
        return redirect(url_for('main.post_detail', post_id=post_id))
    
    form.title.data = post.title
    form.content.data = post.content
    form.city.data = post.city
    form.place.data = post.place
    
    return render_template('edit_post.html', form=form, post=post)

@bp.route('/delete_post/<int:post_id>', methods=['POST', 'DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    # Удаляем связанные лайки и комментарии
    Like.query.filter_by(post_id=post.id).delete()
    Comment.query.filter_by(post_id=post.id).delete()
    
    # Удаляем изображение поста, если оно есть
    if post.image_path:
        try:
            os.remove(os.path.join(current_app.root_path, 'static', post.image_path))
        except:
            pass
    
    db.session.delete(post)
    db.session.commit()
    flash('Пост был успешно удален', 'success')
    return redirect(url_for('main.index'))

@bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'likes_count': len(post.likes)})
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'status': 'liked', 'likes_count': len(post.likes)})

@bp.route('/post/<int:post_id>/is_liked')
@login_required
def is_post_liked(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({'is_liked': post.is_liked_by(current_user)})

@bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not content:
        flash('Комментарий не может быть пустым', 'error')
        return redirect(url_for('main.post_detail', post_id=post_id))
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post_id,
        created_at=datetime.utcnow()
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Произошла ошибка при добавлении комментария', 'error')
    
    return redirect(url_for('main.post_detail', post_id=post_id))

@bp.route('/favorite/<int:post_id>', methods=['POST'])
@login_required
def toggle_favorite(post_id):
    favorite = PlaceFavorite.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_favorite = PlaceFavorite(user_id=current_user.id, post_id=post_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({'status': 'added'})

@bp.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        
        note = Note(
            title=title,
            content=content,
            date=date,
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        
        flash('Заметка создана успешно!', 'success')
        return redirect(url_for('main.notes'))
    
    # Получаем все заметки пользователя
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc()).all()
    
    # Группируем заметки по датам для календаря
    notes_by_date = {}
    for note in notes:
        date_key = note.date.strftime('%Y-%m-%d')
        if date_key not in notes_by_date:
            notes_by_date[date_key] = []
        notes_by_date[date_key].append(note)
    
    return render_template('notes.html', notes=notes, notes_by_date=notes_by_date)

@bp.route('/notes/date/<date>')
@login_required
def notes_by_date(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        notes = Note.query.filter(
            Note.user_id == current_user.id,
            db.func.date(Note.date) == date_obj.date()
        ).order_by(Note.date.desc()).all()
        
        # Группируем заметки по датам для календаря
        notes_by_date = {}
        for note in notes:
            date_key = note.date.strftime('%Y-%m-%d')
            if date_key not in notes_by_date:
                notes_by_date[date_key] = []
            notes_by_date[date_key].append(note)
        
        return render_template('notes.html', notes=notes, notes_by_date=notes_by_date, selected_date=date)
    except ValueError:
        flash('Неверный формат даты', 'error')
        return redirect(url_for('main.notes'))

@bp.route('/notes/<int:note_id>', methods=['PUT', 'DELETE'])
@login_required
def note_operations(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)
    
    if request.method == 'PUT':
        data = request.get_json()
        note.title = data.get('title')
        note.content = data.get('content')
        note.date = datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M')
        db.session.commit()
        return jsonify(id=note.id)
    
    elif request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify(message='Заметка удалена')

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    place_query = request.args.get('place', '')
    city_query = request.args.get('city', '')
    
    if query or place_query or city_query:
        # Поиск по местам
        places = Place.query.filter(
            or_(
                Place.name.ilike(f'%{place_query}%'),
                Place.city.ilike(f'%{city_query}%')
            )
        ).all()
        
        # Поиск по постам, связанным с найденными местами
        place_ids = [place.id for place in places]
        posts = Post.query.filter(Post.place_id.in_(place_ids)).all() if place_ids else []
    else:
        places = []
        posts = []
    
    return render_template('search.html', posts=posts, places=places, 
                         query=query, place_query=place_query, city_query=city_query)

@bp.route('/place/<int:place_id>')
def place_detail(place_id):
    place = Place.query.get_or_404(place_id)
    posts = Post.query.filter_by(place_id=place_id).order_by(Post.date_posted.desc()).all()
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = PlaceFavorite.query.filter_by(user_id=current_user.id, place_id=place_id).first() is not None
    return render_template('place.html', place=place, posts=posts, is_favorite=is_favorite)

@bp.route('/place/<int:place_id>/is_favorite')
@login_required
def is_place_favorite(place_id):
    favorite = PlaceFavorite.query.filter_by(user_id=current_user.id, place_id=place_id).first()
    return jsonify({'is_favorite': favorite is not None})

@bp.route('/place/<int:place_id>/toggle_favorite', methods=['POST'])
@login_required
def toggle_place_favorite(place_id):
    favorite = PlaceFavorite.query.filter_by(user_id=current_user.id, place_id=place_id).first()
    
    if favorite:
        db.session.delete(favorite)
        status = 'unfavorited'
    else:
        favorite = PlaceFavorite(user_id=current_user.id, place_id=place_id)
        db.session.add(favorite)
        status = 'favorited'
    
    db.session.commit()
    return jsonify({'status': status})

@bp.route('/place/<int:place_id>/create_note', methods=['POST'])
@login_required
def create_note(place_id):
    place = Place.query.get_or_404(place_id)
    title = request.form.get('title')
    content = request.form.get('content')
    
    if not title or not content:
        flash('Заполните все поля', 'error')
        return redirect(url_for('main.place_detail', place_id=place_id))
    
    note = Note(
        title=title,
        content=content,
        user_id=current_user.id,
        place_id=place_id,
        date=datetime.utcnow()
    )
    db.session.add(note)
    db.session.commit()
    
    flash('Заметка добавлена', 'success')
    return redirect(url_for('main.place_detail', place_id=place_id))

@bp.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.date_posted.desc()).all()
    
    # Получаем статистику
    total_likes = sum(len(post.likes) for post in posts)
    total_comments = sum(len(post.comments) for post in posts)
    
    return render_template('profile.html', 
                         user=user, 
                         posts=posts,
                         total_likes=total_likes,
                         total_comments=total_comments)

@bp.route('/profile')
@login_required
def my_profile():
    return redirect(url_for('main.profile', user_id=current_user.id))

@bp.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        avatar = request.files.get('avatar')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Проверяем уникальность username и email
        if username != current_user.username:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Это имя пользователя уже занято', 'danger')
                return redirect(url_for('main.edit_profile'))

        if email != current_user.email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Этот email уже используется', 'danger')
                return redirect(url_for('main.edit_profile'))

        # Обновляем аватар
        if avatar:
            filename = secure_filename(avatar.filename)
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            avatar_path = os.path.join('uploads', 'avatars', filename)
            avatar.save(os.path.join(upload_dir, filename))
            current_user.avatar = avatar_path

        # Обновляем пароль, если предоставлен текущий пароль
        if current_password and new_password and confirm_password:
            if not current_user.check_password(current_password):
                flash('Неверный текущий пароль', 'danger')
                return redirect(url_for('main.edit_profile'))
            if new_password != confirm_password:
                flash('Новые пароли не совпадают', 'danger')
                return redirect(url_for('main.edit_profile'))
            current_user.set_password(new_password)

        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash('Профиль успешно обновлен', 'success')
        return redirect(url_for('main.profile', user_id=current_user.id))

    return render_template('edit_profile.html')

@bp.route('/favorites')
@login_required
def favorites():
    favorite_places = PlaceFavorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorite_places)

@bp.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Нет доступа'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Комментарий удален'})

@bp.route('/profile/delete', methods=['POST'])
@login_required
def delete_account():
    try:
        # Удаляем все связанные данные
        Like.query.filter_by(user_id=current_user.id).delete()
        Comment.query.filter_by(user_id=current_user.id).delete()
        Note.query.filter_by(user_id=current_user.id).delete()
        PlaceFavorite.query.filter_by(user_id=current_user.id).delete()
        
        # Удаляем посты пользователя
        posts = Post.query.filter_by(user_id=current_user.id).all()
        for post in posts:
            # Удаляем связанные лайки и комментарии
            Like.query.filter_by(post_id=post.id).delete()
            Comment.query.filter_by(post_id=post.id).delete()
            # Удаляем изображение поста, если оно есть
            if post.image_path:
                try:
                    os.remove(os.path.join(current_app.root_path, 'static', post.image_path))
                except:
                    pass
            db.session.delete(post)
        
        # Удаляем аватар пользователя, если он есть
        if current_user.avatar:
            try:
                os.remove(os.path.join(current_app.root_path, 'static', current_user.avatar))
            except:
                pass
        
        # Удаляем пользователя
        db.session.delete(current_user)
        db.session.commit()
        
        flash('Ваш аккаунт был успешно удален', 'success')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        db.session.rollback()
        flash('Произошла ошибка при удалении аккаунта', 'error')
        return redirect(url_for('main.profile', user_id=current_user.id)) 