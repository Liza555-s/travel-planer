from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from extensions import db
from models import User, Post, Like, Comment, Note, Place, PlaceFavorite
import os
from datetime import datetime

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
                place_id=post_data['place'].id,
                date_posted=datetime.utcnow()
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
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Пользователь с таким именем уже существует')
            return redirect(url_for('main.register'))
        
        new_user = User(username=username, 
                       email=email,
                       password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна!')
        return redirect(url_for('main.login'))
    
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
        image = request.files.get('image')
        
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join('static/uploads', filename)
            image.save(os.path.join(current_app.root_path, image_path))
        else:
            image_path = None
            
        post = Post(
            title=title,
            content=content,
            city=city,
            image_path=image_path,
            user_id=current_user.id,
            place_id=place_id if place_id else None
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Пост успешно создан!', 'success')
        return redirect(url_for('main.post_detail', post_id=post.id))
    
    places = Place.query.all()
    cities = db.session.query(Place.city.distinct()).all()
    cities = [city[0] for city in cities]
    return render_template('create_post.html', places=places, cities=cities)

@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username == 'system':
        flash('Системные посты нельзя редактировать')
        return redirect(url_for('main.index'))
    if post.author != current_user:
        flash('У вас нет прав для редактирования этого поста')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.city = request.form.get('city')
        
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            if post.image_path:
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                            post.image_path.split('/')[-1])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            filename = secure_filename(image.filename)
            image_path = 'uploads/' + filename
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post.image_path = image_path
        
        db.session.commit()
        flash('Пост обновлен успешно!')
        return redirect(url_for('main.index'))
    
    return render_template('edit_post.html', post=post)

@bp.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('У вас нет прав для удаления этого поста')
        return redirect(url_for('main.index'))
    
    if post.image_path:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                post.image_path.split('/')[-1])
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    flash('Пост удален успешно!')
    return redirect(url_for('main.index'))

@bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'likes_count': post.likes.count()})
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'status': 'liked', 'likes_count': post.likes.count()})

@bp.route('/post/<int:post_id>/is_liked')
@login_required
def is_post_liked(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({'is_liked': post.is_liked_by(current_user)})

@bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')
    if content:
        new_comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Комментарий добавлен!', 'success')
    return redirect(request.referrer or url_for('main.index'))

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
        place_id = request.form.get('place_id')
        
        if not title or not content:
            flash('Заполните все обязательные поля', 'error')
            return redirect(url_for('main.notes'))
            
        try:
            note = Note(
                title=title,
                content=content,
                user_id=current_user.id,
                place_id=place_id if place_id else None
            )
            db.session.add(note)
            db.session.commit()
            flash('Заметка успешно создана!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при создании заметки', 'error')
            return redirect(url_for('main.notes'))
            
        return redirect(url_for('main.notes'))
        
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
    places = Place.query.all()
    return render_template('notes.html', notes=notes, places=places)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', results=None)
        
    try:
        # Поиск по местам
        places = Place.query.filter(
            (Place.name.ilike(f'%{query}%')) |
            (Place.city.ilike(f'%{query}%')) |
            (Place.description.ilike(f'%{query}%'))
        ).all()
        
        # Поиск по постам
        posts = Post.query.filter(
            (Post.title.ilike(f'%{query}%')) |
            (Post.content.ilike(f'%{query}%')) |
            (Post.city.ilike(f'%{query}%'))
        ).all()
        
        return render_template('search.html', 
                             results={'places': places, 'posts': posts},
                             query=query)
    except Exception as e:
        flash('Произошла ошибка при поиске', 'error')
        return render_template('search.html', results=None)

@bp.route('/place/<int:place_id>')
def place_detail(place_id):
    place = Place.query.get_or_404(place_id)
    posts = Post.query.filter_by(place_id=place_id).order_by(Post.date_posted.desc()).all()
    return render_template('place_detail.html', place=place, posts=posts)

@bp.route('/place/<int:place_id>/favorite', methods=['POST'])
@login_required
def toggle_place_favorite(place_id):
    place = Place.query.get_or_404(place_id)
    favorite = PlaceFavorite.query.filter_by(user_id=current_user.id, place_id=place_id).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_favorite = PlaceFavorite(user_id=current_user.id, place_id=place_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({'status': 'added'})

@bp.route('/place/<int:place_id>/is_favorite')
@login_required
def is_place_favorite(place_id):
    favorite = PlaceFavorite.query.filter_by(user_id=current_user.id, place_id=place_id).first()
    return jsonify({'is_favorite': favorite is not None})

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user, posts=current_user.posts)

@bp.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        
        # if 'avatar' in request.files:
        #     file = request.files['avatar']
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        #         current_user.avatar = filename
        
        db.session.commit()
        flash('Профиль обновлен успешно!')
        return redirect(url_for('main.user_profile', username=current_user.username))
    
    return render_template('edit_profile.html')

@bp.route('/favorites')
@login_required
def favorites():
    favorite_places = PlaceFavorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorite_places)

@bp.route('/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'Нет доступа'}), 403
    
    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.date = data.get('date', note.date)
    db.session.commit()
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'date': note.date.strftime('%Y-%m-%d') if note.date else None
    })

@bp.route('/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'Нет доступа'}), 403
    
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Заметка удалена'}) 

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