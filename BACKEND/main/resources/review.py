from flask import request  
from flask_jwt_extended import jwt_required, get_jwt_identity  
from flask_restful import Resource  
from ..models import ReviewModel  # Asegúrate de que esta línea es correcta  
from .. import db  

class ReviewResource(Resource):  
    # Obtener una reseña por ID  
    @jwt_required()  
    def get(self, id):  
        review = db.session.query(ReviewModel).get_or_404(id)  
        return review.to_json(), 200  # Convertir la reseña a JSON  

     

    # Actualizar reseña existente  
    @jwt_required()  
    def put(self, id):  
        review = db.session.query(ReviewModel).get_or_404(id)  
        current_user_id = get_jwt_identity()  

        if review.userID != current_user_id:  # Comprobar si el usuario es el propietario de la reseña  
            return {'message': 'No tienes permiso para modificar esta reseña.'}, 403  

        data = request.get_json()  
        review.comment = data.get('comment', review.comment)  # Actualiza comentario si se proporciona  
        review.score = data.get('score', review.score)  # Actualiza score si se proporciona  

        db.session.commit()  
        return {'message': 'Reseña actualizada correctamente.'}, 200  

    # Eliminar reseña existente  
    @jwt_required()  
    def delete(self, id):  
        review = db.session.query(ReviewModel).get_or_404(id)  
        current_user_id = get_jwt_identity()  

        if review.userID != current_user_id:  # Comprobar si el usuario es el propietario de la reseña  
            return {'message': 'No tienes permiso para eliminar esta reseña.'}, 403  

        db.session.delete(review)  
        db.session.commit()  
        return {'message': 'Reseña eliminada correctamente.'}, 204  

class ReviewsResource(Resource):  
    # Obtener todas las reseñas  
    @jwt_required()  
    def get(self):  
        reviews = ReviewModel.query.all()  
        return [review.to_json() for review in reviews], 200  # Convertir todas las reseñas a JSON
    # Crear nueva reseña  
    @jwt_required()  
    def post(self):  
        data = request.get_json()  
        user_id = get_jwt_identity()  # Obtener el ID del usuario actual  
        
        new_review = ReviewModel(  
            userID=user_id,  # Uso de userID según tu modelo  
            poemID=data['poemID'],  # Asegúrate de que este JSON es correcto  
            score=data['score'],  
            comment=data['comment']  
        )  

        db.session.add(new_review)  
        db.session.commit()  
        return {'message': 'Reseña creada correctamente.'}, 201 