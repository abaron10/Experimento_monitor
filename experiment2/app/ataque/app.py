import sys
# sys.path.insert(0,"../../")
from flask import Flask, jsonify , request
app = Flask(__name__)
from faker import Faker
import random
import requests
import json
import sqlite3
import time

MONITOR_URL = "http://127.0.0.1:5000/medical_info/2"
headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzMjk1MTg3NiwianRpIjoiMmFmYTMyNDEtYjZkZi00NDQ1LWI3NDMtZWViNjRhYjEyNmVjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ik1pZ3VlbCIsIm5iZiI6MTYzMjk1MTg3NiwiZXhwIjoxNjMyOTUyNzc2fQ.zJxjLFDnZhhIpvbonQrms1_NDUcWCludAqw0FCGefxA"}

@app.route('/attack',methods=['POST'])
def run_experiment():
    for iteration in range(1,120):
        r = requests.post(url = MONITOR_URL , headers=headers)
        # time.sleep(5)

    return "DDos"


if __name__ == '__main__':
    app.run(debug=True,port=4000)
