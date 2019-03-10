from blueprints import db
from flask_restful import fields

class Users(db.Model):

    tablename = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    daerah = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    response_field = {
        'id' : fields.Integer,
        'name' : fields.String,
        'email' : fields.String,
        'phone_number' : fields.String,
        'daerah' : fields.String,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.String
    }
    def __init__(self, id, name, email, phone_number, daerah, username, password, status):
        
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.daerah = daerah
        self.username = username
        self.password = password
        self.status = status

    def __repr__(self):
        return '<user %r>' % self.id