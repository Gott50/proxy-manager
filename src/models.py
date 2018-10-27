from server import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True, nullable=False)
    proxy = db.Column(db.String(80), unique=True, nullable=False)
    instance = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r %r %r>' % (self.name, self.proxy, self.instance)
