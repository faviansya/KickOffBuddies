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
          
    def get(self, id = None):
        if id == None :
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Pebisnis.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Pebisnis.response_field))

            return {'status':'success', 'data':rows}, 200, {'Content_type' : 'application/json'}
        else:
            qry = Pebisnis.query.get(id)
            data = marshal(qry, Pebisnis.response_field)              
            if qry is not None:
                return {'status':'success', 'data': data}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT FOUND','message':'Pebisnis not found'}, 404, {'Content-Type':'application/json'}

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
            user_new = Pebisnis('pebisnis', args['username'], password, args['name'], args['nama_tempat'], args['email'], args['phone_no'], args['address'], args['deskripsi'], args['url_image'])
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
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('nama_tempat', location='json')
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
                qry_user.password = password
                if args['username'] is not None:
                    qry_user.username = args['username']
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

        else:
            if args['username'] is not None:
                qry_user.username = args['username']
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

    @jwt_required 
    def delete(self):
        qry_del = Pebisnis.query.get(get_jwt_claims()['id'])
        db.session.delete(qry_del)
        db.session.commit()
        return {"code": 200, "message": "OK, your user profile has been deleted", "data": 'User has been deleted'}, 200, {'Content-Type': 'application/json'}
        
    def patch(self):
        return 'Not yet implemented', 501

class PebisnisSelfResource(Resource): 
    @jwt_required  
    def get(self):
        id = get_jwt_claims()['id']
        qry = Pebisnis.query.get(id) #select * from where id = id
        return {"status": "200 OK", "message": "Your user profile is on display", "data": marshal(qry, Pebisnis.response_field)}, 200, {'Content-Type': 'application/json'}   

api.add_resource(PebisnisResource, '', '/<int:id>')
api.add_resource(PebisnisSelfResource, '', '/myprofile')
