import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_polling = Blueprint('polling', __name__)
api = Api(bp_polling)

class PollingResource(Resource): 

    def __init__(self):
        pass
          
    def get(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('sport', location='args')
        args = parser.parse_args() 
        qry = Polling.query 
        if args['sport'] is not None:
            qry = qry.filter(Polling.sport.like("%"+args['sport']+"%"))
            rows = []
            hasil_jumlah_polling = 0
            for row in qry :
                hasil_jumlah_polling += 1
            return {"status": "200 OK", "message": "Hasil polling is on display", "data": hasil_jumlah_polling}, 200, {'Content-Type': 'application/json'}   
        else:
            rows = []
            for row in qry.all():
                rows.append(marshal(row, Polling.response_field))
            return {"status": "200 OK", "message": "All polling posted is on display", "data": rows}, 200, {'Content-Type': 'application/json'}   

    @jwt_required      
    def post(self): #for pemain to add polling       
        parser = reqparse.RequestParser()
        parser.add_argument('sport', location='json')
        parser.add_argument('lokasi', location='json')
        parser.add_argument('jumlah_polling', location='json')
        args = parser.parse_args() 
        name = get_jwt_claims()['name'] 

        if get_jwt_claims()['user_type']  == 'pemain':
            add_polling = Polling(name, args['sport'], args['lokasi'], args['jumlah_polling'])
            db.session.add(add_polling) #insert the input data into the database
            db.session.commit() 
        return {"code": 200, "message": "OK, polling has been successfully posted", "data":marshal(add_polling, Polling.response_field)}, 200, {'Content-Type': 'application/json'}   

    @jwt_required 
    def delete(self, id):
        qry_del = Polling.query.get(id)
        if qry_del is not None: 
            db.session.delete(qry_del)
            db.session.commit()
            return {"code": 200, "message": "OK, polling has been removed", "data": 'User with id = %d has been deleted' % id}, 200, {'Content-Type': 'application/json'}
        return {"code": 404, "message": "Failed to edit. Wrong username or password"}, 404, {'Content-Type': 'application/json'}
        
    def patch(self):
        return 'Not yet implemented', 501

api.add_resource(PollingResource, '', '/<int:id>')

# class PollingResult(Resource): 

#     def __init__(self):
#         pass
          
#     def post(self): 
#         parser = reqparse.RequestParser()
#         parser.add_argument('sport', location='json')
#         args = parser.parse_args() 
#         qry = Polling.query #select * from where id = id
#         qry = qry.filter_by(sport=args["sport"])
#         hasil_jumlah_polling = 0
#         for row in qry.all() : 
#             if row.sport == args['sport']:
#                 hasil_jumlah_polling += 1
#         return {"status": "200 OK", "message": "Result polling for that sport is on display", "data": hasil_jumlah_polling}, 200, {'Content-Type': 'application/json'}   
        
#     def patch(self):
#         return 'Not yet implemented', 501

# api.add_resource(PollingResult, '/result', '/result/<int:id>')
