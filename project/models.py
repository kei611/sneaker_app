from project import db
 
 
class Sneaker(db.Model):
 
    __tablename__ = "sneakers"
 
    id = db.Column(db.Integer, primary_key=True)
    sneaker_model_name = db.Column(db.String, nullable=False)
    sneaker_retail_price = db.Column(db.Integer, nullable=False)
 
    def __init__(self, model_name, retail_price, image_filename=None, image_url=None):
        self.sneaker_model_name = model_name
        self.sneaker_retail_price = retail_price
 
    def __repr__ (self):
        return 'model_name {}'.format(self.name)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_plaintext = db.Column(db.String, nullable=False) # TEMPORARY - TO BE DELETED IN FAVOR OF HASHED PASSWORD

    def __init__(self, email, password_plaintext):
        self.email = email
        self.password_plaintext = password_plaintext

    def __repr__(self):
        return '<User {0}>'.format(self.name)