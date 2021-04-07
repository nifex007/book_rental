import jwt, datetime

import os

JWT_SECRET = os.environ.get('SECRET', 'secret')


def get_jwt(user_id):
    payload = {
            'id' : user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000),
            'iat': datetime.datetime.utcnow()
        }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256').decode('utf-8')

    return token


def decode_jwt(token):
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    return payload
