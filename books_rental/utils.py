from rest_framework.response import Response
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

def format_response(code, data, msg):
    response = Response({
        'code': code,
        'message': msg,
        'data': data
    }, status=code)

    return response


def format_error_response(code, msg):
    response = Response({
        'code': code,
        'message': msg
    }, status=code)

    return response


def get_days(start_date):
    today = datetime.date.today()
    days = abs(today - start_date).days + 1
    return days

def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days) + 1