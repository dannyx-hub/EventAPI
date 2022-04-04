from flask import request, Response, abort, jsonify, Blueprint
from datetime import datetime, timedelta
from config.config import appconfig
from functools import wraps
from database.Database import db
from mail.mail import Email
import hashlib
import logging

login_route = Blueprint('loginroute', __name__)
config = appconfig()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return "token missing"
        try:
            data = jwt.decode(token, config['SECRET_KEY'], algorithms="HS256")
        except Exception as e:
            print(e)
            return Response("invalid token", status=403)
        return f(*args, **kwargs)

    return decorator
