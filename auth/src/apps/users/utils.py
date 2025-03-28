import datetime
import os

import jwt
import pytz
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def generate_jwt(user_id):
    tz = pytz.timezone(settings.TIME_ZONE)
    expiration_time = datetime.datetime.now(tz) + datetime.timedelta(hours=1)
    payload = {"user_id": str(user_id), "exp": expiration_time}
    load_dotenv()
    return jwt.encode(payload, SECRET_KEY_JWT, algorithm=JWT_ALGORITHM)


def validate_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
