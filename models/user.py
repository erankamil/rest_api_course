from db import db
import hashlib, uuid

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    salt = db.Column(db.LargeBinary)
    hashed_password = db.Column(db.LargeBinary)

    def __init__(self, username, password):
        self.username = username
        self.salt = uuid.uuid4().bytes
        self.hashed_password = hashlib.sha512(password.encode('utf-8') + self.salt).digest()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # using class method helps us to change self to something else and then we dont need to hard coded the class name User
    @classmethod
    def find_by_username(cls, username):
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return UserModel.query.filter_by(id=_id).first()
