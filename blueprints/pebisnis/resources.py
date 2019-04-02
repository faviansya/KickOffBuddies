import logging, json, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from password_strength import PasswordPolicy

bp_pebisnis = Blueprint('pebisnis', __name__)
api = Api(bp_pebisnis)

class PebisnisResource(Resource): 

    def __init__(self):
        pass
          
    @jwt_required  
    def get(self):
        id = get_jwt_claims()['id']
        qry = Pebisnis.query.get(id) #select * from where id = id
        return {"status": "200 OK", "message": "Your user profile is on display", "data": marshal(qry, Pebisnis.response_field)}, 200, {'Content-Type': 'application/json'}   

    def post(self): #for pebisnis to register 
        policy = PasswordPolicy.from_names(
            length=6,
            uppercase=1,
            numbers=1,
            special=1,
        )
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('nama_tempat', location='json')
        parser.add_argument('lapangan', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('phone_no', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('deskripsi', location='json')
        parser.add_argument('url_image', location='json')
        args = parser.parse_args() 

        validation = policy.test(args['password'])
        
        if validation == [] :
            user_type = 'pebisnis'
            password = hashlib.md5(args['password'].encode()).hexdigest()
            user_new = Pebisnis('pebisnis', args['username'], password, args['name'], args['nama_tempat'], args['lapangan'], args['email'], args['phone_no'], args['address'], args['deskripsi'], str(datetime.datetime.now()),args['url_image'])
            db.session.add(user_new) #insert the input data into the database
            db.session.commit() 
            return {"code": 200, "message": "OK, your user profile has been created", "data":marshal(user_new, Pebisnis.response_field)}, 200, {'Content-Type': 'application/json'}   
        return {'status' : 'Password Invalid'}, 400, {'Content_type' : 'application/json'}

    @jwt_required 
    def put(self):
        policy = PasswordPolicy.from_names(
            length=6,
            uppercase=1,
            numbers=1,
            special=1,
        )
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('nama_tempat', location='json')
        parser.add_argument('lapangan', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('phone_no', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('deskripsi', location='json')
        parser.add_argument('url_image', location='json')
        args = parser.parse_args()
        
        qry_user = Pebisnis.query.get(get_jwt_claims()['id'])

        if args['password'] is not None:
            validation = policy.test(args['password'])
            if validation == [] :
                password = hashlib.md5(args['password'].encode()).hexdigest()
                qry.password = password
        else:
            if args['lapangan'] is not None:
                qry_user.lapangan = args['lapangan']
            if args['nama_tempat'] is not None:
                qry_user.nama_tempat = args['nama_tempat']
            if args['password'] is not None:
                qry_user.password = password
            if args['name'] is not None:
                qry_user.name = args['name']
            if args['email'] is not None:
                qry_user.email = args['email']
            if args['phone_no'] is not None:
                qry_user.phone_no = args['phone_no']
            if args['address'] is not None:
                qry_user.address = args['address']
            if args['deskripsi'] is not None:
                qry_user.deskripsi = args['deskripsi']
            if args['url_image'] is not None:
                qry_user.url_image = args['url_image']
            db.session.commit()
            return {"code": 200, "message": "OK, your user profile has been created", "data": marshal(qry_user, Pebisnis.response_field)}, 200, {'Content-Type': 'application/json'}
        return {'status' : 'Password Invalid'}, 400, {'Content_type' : 'application/json'}

    @jwt_required 
    def delete(self, id):
        qry_del = Pebisnis.query.get(id)
        if qry_del is not None and get_jwt_claims['id'] == id: 
            db.session.delete(qry_del)
            db.session.commit()
            return {"code": 200, "message": "OK, your user profile has been deleted", "data": 'User with id = %d has been deleted' % id}, 200, {'Content-Type': 'application/json'}
        return {"code": 404, "message": "Failed to edit. Wrong username or password"}, 404, {'Content-Type': 'application/json'}
        
    def patch(self):
        return 'Not yet implemented', 501

api.add_resource(PebisnisResource, '', '/<int:id>')
