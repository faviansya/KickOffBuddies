import logging, json, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..pemain import *
from sqlalchemy import desc
from password_strength import PasswordPolicy
import datetime

bp_googlehandler = Blueprint('googlehandler', __name__)
api = Api(bp_googlehandler)

class GoogleHandlerResources(Resource): 

    def __init__(self):
        pass

    def post(self):
        policy = PasswordPolicy.from_names(
            length=6,
            uppercase=1,
            numbers=1,
            special=1,
        )
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('url_image', location='json')
        parser.add_argument('googleID', location='json')
        args = parser.parse_args()

        qry = Pemain.query.all()

        # qry = Pemain.query.order_by(desc(Pemain.created_time)).all()
        # return {"message": "Success", "data":marshal(qry, Pemain.response_field)}, 200, {'Content-Type': 'application/json'}   
        #check Existence Of Data
        flag = False
        rows = []
        for row in qry:
            if args["email"] == marshal(row, Pemain.response_field)["username"]:
                flag = True
                break
            rows.append(marshal(row, Pemain.response_field))
        #if Daata Exist
        if (flag):
            return {"message": "Success", "data":"login"}, 200, {'Content-Type': 'application/json'}   
        
        #If Data Didnt Exist
        passwords = args['googleID'] + "Rekt$"
        validation = policy.test(passwords)
        if validation == [] :
            password = hashlib.md5(passwords.encode()).hexdigest()

            pemain = Pemain(args['email'],password,args['name'],args['email'],"0","empty","empty","pemain",str(datetime.datetime.now()),args['url_image'])
            db.session.add(pemain)
            db.session.commit()

            return {"message": "Success", "data":"registered"}, 200, {'Content-Type': 'application/json'}   

        return {"message": "Wrong Value", "data":"error"}, 200, {'Content-Type': 'application/json'}   
        
    def patch(self):
        return 'Not yet implemented', 501

api.add_resource(GoogleHandlerResources, '', '/<acceptlist_endpoint>')

