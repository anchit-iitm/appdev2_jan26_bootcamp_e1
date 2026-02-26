from . import db

class employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Employee {self.id}, {self.name}, {self.age}>"

    def formatter(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }