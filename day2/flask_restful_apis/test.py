from flask import request

from . import Resource
from db import db, employee

class index(Resource):
    def get(self):
        return 'Hello World!'

class hello_name(Resource):
    def get(self, name):
        return f"Hello {name}"

class form(Resource):
    def post(self):
        data = request.json
        name = data.get('name')
        age = int(data.get('age'))
        if not name or not age:
            return "Name and age are required", 400
        if age < 0:
            return "Age cannot be negative", 400
        new_user = employee(name=name, age=age)
        db.session.add(new_user)
        db.session.commit()
        return {'name': new_user.name, 'age': new_user.age}


class employees(Resource):
    def get(self):
        all_employees = employee.query.all()
        if not all_employees:
            return {'message': 'No employees found'}, 404
        return {'employees': [employee.formatter() for employee in all_employees], 'message': 'Employees found'}

    def post(self):
        if not request.json:
            return {"message": "No data provided"}, 400
        data = request.json
        name = data.get('name')
        age = data.get('age')
        if not name or not age:
            return {"message": "Name and age are required"}, 400
        if age:
            age = int(age)
            if age < 1:
                return {"message": "Age cannot be negative"}, 400
        
        new_user = employee(name=name, age=age)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Employee added', 'name': new_user.name, 'age': new_user.age}

    def put(self):
        if not request.json:
            return {"message": "No data provided"}, 400
        data = request.json
        id = data.get('id')
        emp = employee.query.filter_by(id=id).first()
        if not emp:
            return {"message": "Employee not found"}, 404
        name = data.get('name')
        age = data.get('age')
        if name:
            emp.name = name
        if age:
            age = int(age)
            if age < 1:
                return {"message": "Age cannot be negative"}, 400
            emp.age = age
        db.session.commit()
        if name and age is None:
            return {'message': 'Employee updated', 'name': emp.name}
        if age and name is None:
            return {'message': 'Employee updated', 'age': emp.age}
        if name and age:
           return {'message': 'Employee updated', 'name': emp.name, 'age': emp.age}
        return {"message": "No update"}, 400

    def delete(self):
        if not request.json:
            return {"message": "No data provided"}, 400
        data = request.json
        id = data.get('id')
        emp = employee.query.filter_by(id=id).first()
        if not emp:
            return {"message": "Employee not found"}, 404
        db.session.delete(emp)
        db.session.commit()
        return {'message': 'Employee deleted'}