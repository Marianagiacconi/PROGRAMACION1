from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

#Decorador para restringir el acceso a usuarios admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request() #Verificar que el JWT es correcto
        claims = get_jwt() #Obtener claims de adentro del JWT

        #Verificar que el rol sea admin
        if claims.get('admin', False):  # Verifica si 'admin' es True
            return fn(*args, **kwargs)
        else:
            return 'Only admins can access', 403
    return wrapper

#Define el atributo que se utilizará para identificar el usuario
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id #Definir ID como atributo identificatorio

#Define que atributos se guardarán dentro del token
@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    claims = {
        'admin': bool(user.admin),  # Booleano en lugar de entero
        'id': user.id,
        'email': user.email
    }
    return claims
