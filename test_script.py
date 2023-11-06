import requests
from flask import request

# Replace 'your_jwt_token_here' with your actual JWT token
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTE4Njg2NiwianRpIjoiNmM2Njg1N2YtZDRmMS00YmVhLWExYmUtZmJjOGU1YzliMzdmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTIsIm5iZiI6MTY5OTE4Njg2NiwiZXhwIjoxNjk5MTg3NzY2fQ.pBq8xx_tWexVAxBAlCAO1Jj-wrnRGgK-cW14sWHxdSQ',
    'Content-Type': 'application/json',
}

data = {
    'title': 'Banker',
    'description': 'bank job',
    'salary': 50000,
    'location': 'London',
    'type': 'Jfull-time',
}

response = requests.post('http://localhost:5000/employers/post_job', headers=headers, json=data)

print(response.status_code)
print(response.json())

def get_access_token():
    auth_header = request.headers.get("Authorization")
    print("Authorization Header:", auth_header)   ##check if auth header is retrieved

    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    else:
        return None