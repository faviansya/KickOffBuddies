import requests, json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import jwt_required

bp_tempat_olahraga = Blueprint('tempat_olahraga', __name__)
api = Api(bp_tempat_olahraga) #daftar ke Api

class TempatOlahraga(Resource):
    google_places_host = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyB3GHH--AbFb9XDA16VX56gMUjQYSKlviQ&query=badminton+in+Jakarta'

# params={'query':'badminton+in+Malang'}
    def get(self):

        rq = requests.get(self.google_places_host)
        place = rq.json()
        data = []

        for i in range (len(place['results'])):
            
            # x = {
            #     'address': place[i]['formatted_address'],
            #     'nama': place[i]['name'],
            #     'rating': place[i]['rating'],
            #     'jumlah_pemberi_rating': place[i]['user_ratings_total']
            # }
            data.append(place['results'][i])
        return data  
        # return place['results']

api.add_resource(TempatOlahraga, '')
