from .. import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    poemID = db.Column(db.Integer, db.ForeignKey('poems.id'))
    score = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    user = db.relationship('Users', back_populates="reviews", uselist=False, single_parent=True)
    poems = db.relationship('Poems', back_populates="reviews", uselist=False, single_parent=True)

    def __repr__(self) -> str:
        return f'Review: {self.score} {self.comment}'

    #Conversor objeto a JSON
    def to_json(self):
        review_json = {
            'id': self.id,
            'userID': self.userID,
            'poemID': self.poemID,
            'score': self.score,
            'user': self.user.to_json(),
            'poems': self.poems.to_json(),
            'comment': self.comment
        }
        return review_json

    #Conversor JSON a objeto
    @staticmethod
    def from_json(review_json):
        id = review_json.get('id')
        userID = review_json.get('userID')
        poemID = review_json.get('poemID')
        score = review_json.get('score')
        comment = review_json.get('comment')
        return Review(id=id, userID=userID, poemID=poemID, score=score, comment=comment)