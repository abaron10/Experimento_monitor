from celery import Celery
from celery.signals import task_postrun
from flask import request
import requests
from flask_cors import CORS


celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='voting_pago')
def voting_pago(paciente):
        print ("llamar a servicio")
        
        API_ENDPOINT = "http://127.0.0.1:5000"
        print(API_ENDPOINT + "/send_payment")
        r = requests.post(url = API_ENDPOINT + "/send_payment", data=paciente)
       
