import sys
from flask import Flask, jsonify , request
import requests
from celery import Celery
import random 
from flask_cors import CORS
import time

app = Flask(__name__)
cors = CORS(app)

servers_status = [{"server_1": False},
                  {"server_2": False},
                  {"server_3": False}]

servers_id = {"server_1": 1 , "server_2": 2, "server_3": 3}

API_ENDPOINT = "http://127.0.0.1:500{}"

LEADER = "server_1"

@app.route('/send_payment',methods=['POST'])
def process_payment():
    try:
        r = requests.post(url = API_ENDPOINT.format(servers_id[LEADER]) + "/payment", data = request.form)
    except:
        time.sleep(2)
        r = requests.post(url = API_ENDPOINT.format(servers_id[LEADER]) + "/payment", data = request.form)
    return r.content
    


def verify_life_servers():
    global LEADER

    for i , server in enumerate(servers_status):
        iteration = i + 1
    
        try:
            r = requests.post(url = API_ENDPOINT.format(iteration) + "/ping")
            alive_server = "server_{}".format(iteration)
           
            servers_status[iteration-1][alive_server] = True
            print(str(r.content.decode('UTF-8')) + " from server " + str(iteration))
           
        except Exception:
            failed_server = "server_{}".format(iteration)
            servers_status[iteration-1][failed_server] = False
            if failed_server == LEADER:
                
                LEADER  = reassign_leader(iteration)
            print("I AM OFF from server " + str(iteration))

    print("The leader is " + LEADER + "\n")
    
def reassign_leader(id_failed_leader):
  
    test_list = [1, 2 ,3]
  
    id_new_leader = random.choice([ele for ele in test_list if ele != id_failed_leader])
    return "server_{}".format(id_new_leader)


if __name__ == '__main__':
    app.run(debug=True,port=4000)
