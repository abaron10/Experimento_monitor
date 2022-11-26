import sys
# sys.path.insert(0,"../../")
from flask import Flask, jsonify , request
app = Flask(__name__)
from faker import Faker
import random
import requests
import json
import sqlite3
from celery import Celery

data_factory = Faker()
MONITOR_URL = "http://127.0.0.1:5000/"
celery_app = Celery(__name__, broker='redis://localhost:6379/0')

conn = sqlite3.connect('patient_payments.db', check_same_thread=False)
cur = conn.cursor()

@celery_app.task(name='voting_pago')
def voting_pago(*args):
    pass

def create_database():
    cur.execute('DROP TABLE IF EXISTS payments')
    cur.execute('''
    CREATE TABLE payments (id INTEGER, name TEXT,lastname TEXT, email TEXT, phone_number TEXT, billing INTEGER, exit_granted BOOLEAN)''')

@app.route('/payment',methods=['POST'])
def run_experiment():
    lis = []
    create_database()
    for iteration in range(1,20):
        lis.append(payment(iteration,
                data_factory.name().split(" ")[0],
                data_factory.name().split(" ")[1],
                data_factory.email(),
                "+57 " + str(random.randint(1000000, 9000000)),
                random.randint(100000, 900000),
                False))
    return jsonify(lis)


def payment(id,name,lastname,email,phone_number,billing,exit_granted):

    patient = {"id": id,
                "name": name, 
                "lastname": lastname, 
                "email":email,
                "phone_number":phone_number,
                "billing":billing,
                "exit_granted":exit_granted}
    try:
        #r = requests.post(url = MONITOR_URL + "/send_payment", data=patient)
        response = "enqueued"
        args = (patient,)
        voting_pago.apply_async(args=args, queue = 'logs')
        #response = json.loads(r.content)
    except:
        response = "Mistake"

    return response
    

if __name__ == '__main__':
    app.run(debug=True,port=4000)
