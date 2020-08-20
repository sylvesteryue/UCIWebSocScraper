from flask import Flask, jsonify
from flask_restful import Api


from resources.breadths import Breadths
from resources.departments import Departments
from resources.course import Course

app = Flask(__name__)
api = Api(app)


api.add_resource(Breadths, '/breadths')
api.add_resource(Departments, '/departments')
api.add_resource(Course, '/class')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)