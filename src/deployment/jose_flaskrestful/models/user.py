from first_flask.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, id_, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, password={self.password})"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id_: str):
        return cls.query.filter_by(id=id_).first()
