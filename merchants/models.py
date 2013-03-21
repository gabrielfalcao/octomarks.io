from merchants.app import app


db = app.db


class Merchant(db.Model):
    __tablename__ = 'merchant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    zip_code = db.Column(db.String(15), unique=True)


class CompetitorTracker(db.Model):
    __tablename__ = 'competitor_tracker'

    id = db.Column(db.Integer, primary_key=True)


class Category(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
