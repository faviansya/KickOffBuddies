import json, logging, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_pemain = Blueprint('pemain', __name__)
api = Api(bp_pemain)
       
class PemainResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, pemain_endpoint = None):
        jwtclaim = get_jwt_claims()
        if pemain_endpoint is not None:
            if pemain_endpoint == "me":
                qry = Pemain.query.get(jwtclaim['id'])
                return {'status' : 'Success', 'data' : marshal(qry, Pemain.response_field)}, 200, {'Content_type' : 'application/json'} 
            else:
                parser = reqparse.RequestParser()
                qry = Pemain.query.get(pemain_endpoint)
                if(qry is None):
                    return {'status' : 'Success', 'data' : []}, 200, {'Content_type' : 'application/json'} 
                return {'status' : 'Success', 'data' : marshal(qry, Pemain.response_field)}, 200, {'Content_type' : 'application/json'} 
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 50)
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Pemain.query

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Pemain.response_field))
            
            return {'status' : 'Success', 'data' : rows}, 200, {'Content_type' : 'application/json'} 
    
    @jwt_required
    def delete(self):
        qry = Pemain.query.get(jwtclaim['id'])
        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'Success', 'message' : 'See You Again In Another Time'}, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtclaim = get_jwt_claims()
        qry = Pemain.query.get(jwtclaim['id'])
        marshal_pemain = marshal(qry, Pemain.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('password', location = 'json',default = marshal_pemain["password"])
        parser.add_argument('name', location = 'json',default = marshal_pemain["name"])
        parser.add_argument('email', location = 'json',default = marshal_pemain["email"])
        parser.add_argument('phone_no', location = 'json',default = marshal_pemain["phone_no"])
        parser.add_argument('address', location = 'json',default = marshal_pemain["address"])
        parser.add_argument('favourite_sport', location = 'json',default = marshal_pemain["favourite_sport"])
        parser.add_argument('url_image', location = 'json',default = marshal_pemain["url_image"])

        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        qry.password = password
        qry.name = args['name']
        qry.email = args['email']
        qry.phone_no = args['phone_no']
        qry.address = args['address']
        qry.favourite_sport = args['favourite_sport']
        qry.url_image = args['url_image']

        db.session.commit()
        marshal_pemain = marshal(qry, Pemain.response_field)

        return {'status' : 'Success Change', 'data' : marshal_pemain}, 200, {'Content_type' : 'application/json'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('phone_no', location = 'json')
        parser.add_argument('address', location = 'json', required = True)
        parser.add_argument('favourite_sport', location = 'json', required = True)
        parser.add_argument('url_image', location = 'json', required = True)
        args = parser.parse_args()
        password = hashlib.md5(args['password'].encode()).hexdigest()

        pemain = Pemain(args['username'],password,args['name'],args['email'],args['phone_no'],args['address'],args['favourite_sport'],"pemain",str(datetime.datetime.now()),args['url_image'])
        db.session.add(pemain)
        db.session.commit()

        return {'status' : 'Success', 'data' : marshal(pemain, Pemain.response_field)}, 200, {'Content_type' : 'application/json'}

api.add_resource(PemainResources, '', '/<pemain_endpoint>')
