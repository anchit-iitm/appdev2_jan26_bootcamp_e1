from flask_security import Security
from argon2 import PasswordHasher

ph = PasswordHasher()
security = Security()