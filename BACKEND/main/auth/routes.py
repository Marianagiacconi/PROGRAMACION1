from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from..auth.decorators import admin_required
from main import db
from main.models import UsersModel, ReviewModel, PoemsModel
from main.mail.functions import sendMail


auth = Blueprint('auth', __name__, url_prefix='/auth')
app= Blueprint('app', __name__, url_prefix='')

@auth.route('/login', methods=['POST'])  
def login():  
    # Buscar usuario por email  
    email = request.get_json().get("email")  
    user = db.session.query(UsersModel).filter(UsersModel.email == email).first()  

    if user is None:  
        return {'msg': 'User not found'}, 404  # Usuario no encontrado  

    # Validar contraseña  
    if user.validate_pass(request.get_json().get("password")):  
        # Generar token de acceso y pasar el objeto completo  
        access_token = create_access_token(identity=user)  

        # Retornar datos del usuario y el token  
        data = {  
            'id': str(user.id),  
            'email': user.email,  
            'access_token': access_token  
        }  
        return data, 200  
    else:  
        return {'msg': 'Incorrect password'}, 401  # Contraseña incorrecta
    
@auth.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()
    if not data or 'firstname' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'msg': 'Firstname, email, and password are required'}), 400

    if UsersModel.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'User with this email already exists'}), 400

    new_user = UsersModel.from_json(data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'User created successfully!'}), 201


@auth.route('/reviews', methods=['GET'])
@jwt_required()
def get_reviews():
    reviews = db.session.query(ReviewModel).all()
    return jsonify([review.to_json() for review in reviews]), 200

# Endpoint para obtener un usuario específico
@auth.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = db.session.query(UsersModel).filter_by(id=id).first_or_404()
    return jsonify(user.to_json()), 200
# Endpoint para obtener todos los usuarios (solo para admin)
@auth.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users = db.session.query(UsersModel).all()  
    return jsonify([user.to_json() for user in users]), 200  

# Endpoint para actualizar un usuario específico (solo para admin)
@auth.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(id):
    data = request.get_json()
    user = db.session.query(UsersModel).filter_by(id=id).first_or_404()
    if "email" in data:
        user.email = data["email"]
    if "admin" in data:
        user.admin = data["admin"]
    db.session.commit()
    return jsonify(user.to_json()), 200

# Endpoint para eliminar un usuario específico (solo para admin)
@auth.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(id):
    user = db.session.query(UsersModel).filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200

# Endpoint para actualizar una reseña específica
@auth.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id):
    data = request.get_json()
    review = db.session.query(ReviewModel).filter_by(id=id).first_or_404()
    if "content" in data:
        review.content = data["content"]
    if "rating" in data:
        review.rating = data["rating"]
    db.session.commit()
    return jsonify(review.to_json()), 200

# Endpoint para eliminar una reseña
@auth.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = db.session.query(ReviewModel).filter_by(id=id).first_or_404()
    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review deleted"}), 200

# Crear un nuevo poema
@auth.route('/poems', methods=['POST'])
@jwt_required()
def create_poem():
    data = request.get_json()
    try:
        poem = PoemsModel.from_json(data)  # Crea una instancia de PoemModel desde el JSON de entrada
        db.session.add(poem)
        db.session.commit()
        return jsonify(poem.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
@auth.route('/can_upload', methods=['GET'])  
@jwt_required()  
def can_upload_poem():  
    user_id = get_jwt_identity()  
    return _can_upload_poem(user_id)  

def _can_upload_poem(user_id):  
    user = UsersModel.query.get(user_id)  
    if not user:  
        return jsonify({"error": "Usuario no encontrado"}), 404  

    reviews_count = ReviewModel.query.filter_by(user_id=user_id).count()  
    poems_count = PoemsModel.query.filter_by(user_id=user_id).count()  

    # Permitimos que suba un poema por cada 5 reseñas realizadas  
    can_upload = reviews_count >= (poems_count + 1) * 5  

    return jsonify({"canUpload": can_upload})
@auth.route('/users/<user_id>/poem-count', methods=['GET'])
@jwt_required()
def get_user_poem_count(user_id):
    try:
        poem_count = PoemsModel.query.filter_by(user_id=user_id).count()
        return jsonify(poem_count=poem_count), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener la cantidad de poemas'}), 500

# Obtener todos los poemas
@auth.route('/', methods=['GET'])
@jwt_required()
def get_poems():
    poems = db.session.query(PoemsModel).all()
    return jsonify([poem.to_json() for poem in poems]), 200

# Obtener un poema específico por ID
@auth.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_poem(id):
    poem = db.session.query(PoemsModel).filter_by(id=id).first_or_404()
    return jsonify(poem.to_json()), 200

# Actualizar un poema específico
@auth.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_poem(id):
    data = request.get_json()
    poem = db.session.query(PoemsModel).filter_by(id=id).first_or_404()

    if "title" in data:
        poem.title = data["title"]
    if "content" in data:
        poem.content = data["content"]

    db.session.commit()
    return jsonify(poem.to_json()), 200

# Eliminar un poema específico
@auth.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_poem(id):
    poem = db.session.query(PoemsModel).filter_by(id=id).first_or_404()
    db.session.delete(poem)
    db.session.commit()
    return jsonify({"msg": "Poem deleted"}), 200

