import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.pemain import *

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()

        qry = Pemain.query.filter_by(username = args['username']).filter_by(password = args['password']).first()
        if qry is not None:
            token = create_access_token(marshal(qry, Pemain.response_field))
        else:
            return {'status' : 'UNAUTHORIZED', 'message' : 'Invalid key'}, 401, {'Content_type' : 'application/json'}
        return {'token' : token}, 200, {'Content_type' : 'application/json'}

api.add_resource(CreateTokenResources, '')