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
