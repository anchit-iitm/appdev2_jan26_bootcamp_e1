from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Hello World!'

# @app.route('/hello')
# def hello(): this will be done from the frontend
#     return render_template('hello.html')

@app.route('/hello/<name>')
def hello_name(name):
    return f"Hello {name}"

@app.route('/form', methods=['GET', 'POST'])
def form():
    # if request.method=="GET":
    #     return render_template('form.html')
    if request.method=="POST":
        data = request.json
        name = data.get('name')
        age = int(data.get('age'))
        if not name or not age:
            return "Name and age are required", 400
        if age < 0:
            return "Age cannot be negative", 400
        new_user = users(name=name, age=age)
        db.session.add(new_user)
        db.session.commit()
        return {'name': new_user.name, 'age': new_user.age}


if __name__ == '__main__':
    app.run()