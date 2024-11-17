from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    poems = db.relationship('Poems',back_populates ="user", cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates="user", cascade="all, delete-orphan")

    # region Functions

    def __repr__(self) -> str:
        """Debug def

        Keyword arguments:
        self

        Return: str
        """
        return '<Usuario: %r %r >' % (self.firstname, self.password)

    # Getter de la contraseña plana no permite leerla
    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')

    # Setter de la contraseña toma un valor en texto plano
    # calcula el hash y lo guarda en el atributo password
    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    # Método que compara una contraseña en texto plano con el hash guardado en la db
    def validate_pass(self, password):
        """This will to check password hash

        Keyword arguments:
        self, password

        Return: True ,False
        """
        return check_password_hash(self.password, password)

    def to_json(self):
        """This function obtains Users and return a JSON object

        Keyword arguments:
        self

        Return: json
        """
        user_json = {
            'id': self.id,
            'firstname': str(self.firstname),
            'email': self.email,
            'admin': self.admin,


        }
        return user_json
    
    def to_json_short(self):
        """This function obtains Users and return a JSON object

        Keyword arguments:
        self

        Return: json
        """
        user_json = {
            'id': self.id,
            'firstname': str(self.firstname),
            'admin': self.admin,


        }
        return user_json


    def to_json_complete(self):
        poems = [poem.to_json() for poem in self.poems]

        user_json = {
            'id': self.id,
            'firstname': str(self.firstname),
            'email': self.email,
            'admin': self.admin,
            'poems': poems,
            'count_poems':len(self.poems)
        }
        return user_json

    @staticmethod
    def from_json(user_json):
        """This get a JSON and return a Users python object

        Keyword arguments:
        user_json - json object

        Return: object
        """

        id = user_json.get('id')
        firstname = user_json.get('firstname')
        email = user_json.get('email')
        password = user_json.get('password')
        admin = user_json.get('admin')
        return Users(
            id=id,
            firstname=firstname,
            email=email,
            plain_password=password,
            admin=admin)
