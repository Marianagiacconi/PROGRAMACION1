from flask import app, jsonify, request
from flask_jwt_extended import jwt_required
from . import db
from .models import Poem, Review, User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    # Verificar si el usuario ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'User registered successfully!'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    
    return jsonify({'msg': 'Bad email or password'}), 401

# Obtener todos los poemas
@app.route('/api/poems', methods=['GET'])
@jwt_required()
def get_poems():
    poems = Poem.query.all()
    return jsonify([{
        'id': poem.id,
        'title': poem.title,
        'author': poem.author,
        'content': poem.content
    } for poem in poems])

# Obtener un poema específico
@app.route('/api/poems/<int:poem_id>', methods=['GET'])
def get_poem(poem_id):
    poem = Poem.query.get_or_404(poem_id)
    return jsonify({
        'id': poem.id,
        'title': poem.title,
        'author': poem.author,
        'content': poem.content
    })

# Crear un nuevo poema
@app.route('/api/poems', methods=['POST'])
@jwt_required()
def create_poem():
    data = request.get_json()
    new_poem = Poem(title=data['title'], author=data['author'], content=data['content'])
    db.session.add(new_poem)
    db.session.commit()
    return jsonify({'id': new_poem.id}), 201

# Obtener reseñas de un poema
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    poem_id = request.args.get('poemId')
    reviews = Review.query.filter_by(poem_id=poem_id).all()
    return jsonify([{
        'id': review.id,
        'comment': review.comment,
        'rating': review.rating,
        'poem_id': review.poem_id
    } for review in reviews])

# Crear una nueva reseña
@app.route('/api/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()
    new_review = Review(comment=data['comment'], rating=data['rating'], poem_id=data['poem_id'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'id': new_review.id}), 201
