import requests
import json


def post_payload(url, payload):
    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json',
        # 'Cookie': 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE4MDExOTcxLCJpYXQiOjE2MTc5NTE5NzF9.sdUEdghVWmSUhedUsQ3zw0v_bBVqQ_Ikf-UWSJwJwRs'
        } 
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def get_current_host(request):
    scheme = request.is_secure() and "https" or "http"
    return f'{scheme}://{request.get_host()}/'


def get_request(url):
    # url = "localhost:8081/api/books/return/5/7"

    headers = {
    # 'Cookie': 'jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE4MDExOTcxLCJpYXQiOjE2MTc5NTE5NzF9.sdUEdghVWmSUhedUsQ3zw0v_bBVqQ_Ikf-UWSJwJwRs'
    }

    response = requests.request("GET", url)

    return response
    