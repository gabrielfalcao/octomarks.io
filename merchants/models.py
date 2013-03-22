from merchants.app import app


db = app.db


class Merchant(db.Model):
    __tablename__ = 'merchant'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), unique=True)
    last_name = db.Column(db.String(256), unique=True)
    zipcode = db.Column(db.Integer, unique=True)
    phone = db.Column(db.String(15), unique=True)
    address = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)


class CompetitorTracker(db.Model):
    __tablename__ = 'competitor_tracker'

    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, inst):
        pass

    def track(self, other):
        pass

    def tracking(self):
        return []


class Category(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
