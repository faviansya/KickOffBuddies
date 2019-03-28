import random, logging
from blueprints import db
from flask_restful import fields


class Pebisnis(db.Model):
    __tablename__ = "pebisnis"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True) 
    nama_tempat = db.Column(db.String(255), nullable=False)  #nama tempat usaha nya 
    lapangan = db.Column(db.String(255), nullable=False) #lapangan olahraga apa yang dipunya
    email = db.Column(db.String(55), nullable=False)
    phone_no = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.String(255), nullable=False)

    response_field = {
        'id' : fields.Integer,
        'user_type' : fields.String,
        'username' : fields.String,
        'nama_tempat' : fields.String,
        'lapangan' : fields.String,
        'password' : fields.String,
        'name' : fields.String,
        'email' : fields.String,
        'phone_no' : fields.String,
        'address' : fields.String,
        'deskripsi' : fields.String,
    }
  
    def __init__(self, user_type, username, nama_tempat, lapangan, password, name, email, phone_no, address, deskripsi):
        self.user_type = user_type
        self.username = username
        self.nama_tempat = nama_tempat
        self.lapangan = lapangan
        self.password = password
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.address = address
        self.deskripsi = deskripsi
       
    def __repr__(self): #initiate table model
        return '<Pebisnis %r>' % self.id 
  