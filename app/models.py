from app import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#A table that acts like a bridge that connects different databases "User" and "Perfumes"
userperf = db.Table('userperf', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('perfume_id', db.Integer, db.ForeignKey('perfumes.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    #Database fields
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    perfumes = db.relationship("Perfumes",secondary = "userperf",backref = "users")
    
    #Constructor
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    #Custom check_password methods defined to be called later with a dot operator.
    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"UserName: {self.username}"

class Perfumes(db.Model):
    #Database fields
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(140), nullable=False)
    price = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(140), nullable=False)
 
    #Constructors
    def __init__(self, pname, price, description):
        self.pname = pname
        self.price = price
        self.description = description