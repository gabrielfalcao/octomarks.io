from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from merchants.app import app


db = app.db


class Merchant(db.Model):
    __tablename__ = 'merchant'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            kwargs.update({
                'password': generate_password_hash(kwargs['password'])
            })

        # F*ck the API user, let's rewrite this key
        kwargs.update({
            'created': datetime.utcnow(),
        })
        super(Merchant, self).__init__(*args, **kwargs)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)


class CompetitorTracker(db.Model):
    __tablename__ = 'competitor_tracker'

    id = db.Column(db.Integer, primary_key=True)
    my_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)

    @classmethod
    def track(self, inst, other):
        pass

    @classmethod
    def tracking(self, inst):
        return []


class Category(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
