from flask_restful import Resource, reqparse
from flask import request

from course_scraper import get_breadths

class Breadths(Resource):
    def get(self):
        breadths = get_breadths()

        if breadths:
            return breadths, 200
        else:
            return {'message': 'cannot find breadths'}, 404
