from flask import Flask, render_template, request, redirect, url_for
from db import db

def create_app():
    initApp = Flask(__name__)
    import config 
    initApp.config.from_object(config)
    db.init_app(initApp) # register the models through sqlalchemy

    from routes import apis
    for route in apis:
        initApp.register_blueprint(route, url_prefix='/api')

    from flask_restful_apis import api
    api.init_app(initApp) 

    from security import security
    from db import user_datastore
    security.init_app(initApp, user_datastore)

    return initApp

def create_roles():
    from db import user_datastore
    user_datastore.find_or_create_role(name='admin', description='Admin role')
    user_datastore.find_or_create_role(name='user', description='User role')
    user_datastore.find_or_create_role(name='manager', description='Manager role')
    db.session.commit()
    return "roles already there or added successfully"

def create_admin():
    from db import user_datastore
    from security import ph
    if not user_datastore.find_user(email='admin@abc.com'):
        user_datastore.create_user(email='admin@abc.com', password=ph.hash('admin'), roles=['admin'])
    db.session.commit()
    return "admin already there or added successfully"

app = create_app()

with app.app_context():
    db.create_all()
    create_roles()
    create_admin()


if __name__ == '__main__':
    app.run()