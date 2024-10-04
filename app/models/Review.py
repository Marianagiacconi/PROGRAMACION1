from .. import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Calificación del 1 al 5
    poem_id = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)  # Relación con Poem
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relación con User