from flask_restful import Resource, reqparse
from flask import request

from course_scraper import get_departments

class Departments(Resource):
    def get(self):
        departments = get_departments()

        if departments:
            return departments, 200
        else:
            return {'message': 'cannot find departments'}, 404
