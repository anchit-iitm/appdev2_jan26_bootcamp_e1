from flask_restful import Api, Resource

api = Api(prefix='/frest')

from .test import index, hello_name, form, employees

api.add_resource(index, '/')
api.add_resource(hello_name, '/hello/<name>')
api.add_resource(form, '/form')
api.add_resource(employees, '/employees')
