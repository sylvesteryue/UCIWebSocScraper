from flask_restful import Resource, reqparse
from flask import request

from course_scraper import get_classes

class Course(Resource):
    def get(self):
        params = request.args

        courses = get_classes(params)

        if courses:
            return courses, 200
        else:
            return {'message': 'cannot find specified classes'}, 404
