from flask import request, Blueprint
from flask_security import auth_required, roles_accepted

from db import db, employee

test_bp = Blueprint('test', __name__)

@test_bp.route('/')
@auth_required()
@roles_accepted('user')
def index():
    return 'Hello World!'

@test_bp.route('/hello/<name>')
def hello_name(name):
    return f"Hello {name}"

@test_bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method=="POST":
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


@test_bp.route('/employees', methods=['GET', 'POST', 'PUT', 'DELETE'])
def employees():
    if request.method == 'GET':
        all_employees = employee.query.all()
        if not all_employees:
            return {'message': 'No employees found'}, 404
        return {'employees': [employee.formatter() for employee in all_employees], 'message': 'Employees found'}

    if request.method == 'POST':
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

    if request.method == 'PUT':
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

    if request.method == 'DELETE':
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