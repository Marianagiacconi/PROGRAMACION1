from flask_restful import Resource  
from flask import logging, request, jsonify
from .. import db  
from ..models import PoemsModel
from flask_jwt_extended import jwt_required, get_jwt_identity  

# Recurso Poem  
class Poem(Resource):  
    # Obtener recurso  

    @jwt_required()  
    def get(self, id):  
        poem = db.session.query(PoemsModel).get_or_404(id)  
        return poem.to_json()  

      # Modificar recurso  
   
    @jwt_required()  
    def put(self, id):  
        poem = db.session.query(PoemsModel).get_or_404(id)  # Obtener poema por ID  
        current_user_id = get_jwt_identity()  # Obtener ID del usuario actual  

        # Verificar que solo el propietario puede modificar el poema  
        if poem.userID != current_user_id:  
            return {'message': 'No tienes permiso para modificar este poema.'}, 403  

        data = request.get_json()  # Obtener datos a actualizar  

        # Actualizar los campos del poema  
        for key, value in data.items():  
            if hasattr(poem, key):  # Verifica si el campo existe en el modelo  
                setattr(poem, key, value)  # Establece el nuevo valor  

        db.session.commit()  # Confirmar cambios  
        return poem.to_json(), 200  # Devolver el poema actualizado  


    @jwt_required()  
    def delete(self, id):  
        # Obtener el poema por ID, devuelve 404 si no se encuentra  
        poem = db.session.query(PoemsModel).get_or_404(id)  
        current_user_id = get_jwt_identity()  # Obtener ID del usuario actual  

        # Verificar que solo el propietario puede eliminar el poema  
        if poem.userID != current_user_id:  
            print(f'Usuario {current_user_id} no tiene permiso para eliminar el poema {id}.')  # Log para depuración  
            return {'message': 'No tienes permiso para eliminar este poema.'}, 403  

        db.session.delete(poem)  # Intentar eliminar el poema  
        db.session.commit()  # Confirmar eliminación  
        print(f'Poema {id} eliminado por el usuario {current_user_id}.')  # Log para confirmación  
        return '', 204  # Respuesta vacía con código 204  

# Recurso Poems  
class Poems(Resource):  
    # Obtener lista de poemas  
    def get(self):  
        poems = db.session.query(PoemsModel).all()  # Asegúrate de obtener todos los poemas  
        
        return jsonify({  
            'poems': [poem.to_json() for poem in poems],  
        })  

    @jwt_required()  
    def post(self):  
        try:  
            data = request.get_json()  # Obtén el JSON enviado en la petición  
            poem = PoemsModel.from_json(data)  # Crea el poema desde el JSON  
            poem.userID = get_jwt_identity()  # Asigna el ID del usuario actual  
            
            db.session.add(poem)  # Añade el poema a la sesión  
            db.session.commit()   # Confirma los cambios en la base de datos  
            
            return poem.to_json(), 201  # Retorna el poema creado con código 201  
        except Exception as e:  
            logging.error(f'Error al crear el poema: {str(e)}')  # Loguea el error  
            return {'message': 'Error al crear el poema', 'error': str(e)}, 400  