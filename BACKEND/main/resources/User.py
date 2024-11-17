from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsersModel
from ..utils import userFilters, generalPagination
from main.auth.decorators import admin_required


# Recurso Usuario
class User(Resource):

    # Obtener recurso
    @jwt_required()
    def get(self, id):
        user = db.session.query(UsersModel).get_or_404(id)
        return user.to_json()

    # Eliminar recurso
    @admin_required
    def delete(self, id):
        user = db.session.query(UsersModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    # Modificar recurso
    @admin_required
    def put(self, id):
        user = db.session.query(UsersModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201


# Recurso Usuarios
class Users(Resource):

    # Obtener lista de recursos
    @jwt_required()
    def get(self):
        users = db.session.query(UsersModel)
       
        return jsonify({
            'users': [user.to_json_complete() for user in users],

        })

    # Insertar recurso
    @admin_required
    def post(self):
        user = UsersModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201