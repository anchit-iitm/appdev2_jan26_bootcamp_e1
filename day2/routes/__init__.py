from flask import Blueprint

from .test import test_bp
from .security import security_bp

apis = [test_bp, security_bp]