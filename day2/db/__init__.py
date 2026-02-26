from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .test import employee
from .security import User, Role, RolesUsers, user_datastore

