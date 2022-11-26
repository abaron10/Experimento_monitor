import bcrypt
from flask_restful import Resource
from ..modelos import db, Usuario
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token ,get_jwt_identity
from datetime import datetime
from celery import Celery
import redis
import bcrypt
from http import HTTPStatus
import datetime
from PIL import Image
import os



class VistaSignIn(Resource):

    def post(self):
        contraseña = bcrypt.hashpw((request.json["contrasena"]).encode('utf-8'), bcrypt.gensalt())
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=contraseña)
        token_de_acceso = create_access_token(identity=request.json["nombre"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"mensaje": "usuario creado exitosamente", "token de acceso": token_de_acceso}

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    def post(self):
        print(request)
        u_nombre = request.json["nombre"]
        u_contraseña = request.json["contrasena"]
        usuario = Usuario.query.filter_by(nombre=u_nombre).first()
        db.session.commit()

        if not bcrypt.checkpw(u_contraseña.encode('utf8'), usuario.contrasena):
            return "Incorrect password"

        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.nombre)
            return {"mensaje": "Acceso consedido", "usuario": {"nombre": usuario.nombre, "id": usuario.id},
                    "token": token_de_acceso}

class VistaGetMedicalHistory(Resource):

    def __init__(self):
        self.redis_host = 'localhost'
        self.redis_port = 6379
        self.r = redis.StrictRedis(host = self.redis_host , port= self.redis_port, decode_responses=True)

    def hit_validation(self, user_ip):
        try:
            msg = self.r.get(user_ip)
            if msg is None:
                self.r.set(user_ip, str(datetime.datetime.now()))

            difference = (datetime.datetime.now()- datetime.datetime.strptime(msg, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
            print(difference)
            if difference < 5:
                print("Too much requests in a certain amount of time.Try again later.")
                return False
            self.r.set(user_ip, str(datetime.datetime.now()))
            return True        
        except Exception as e:
            message = "No jsonlines file found on the bucket"
            return {"message": message}, HTTPStatus.OK

    @jwt_required()
    def post(self , id_patient):
        user_id = Usuario.query.filter_by(nombre=get_jwt_identity()).first().id
        if user_id == id_patient:
            valid_request = self.hit_validation(id_patient)
            if valid_request:
                print("entro")
                file = Image.open('/Users/abaron/Documents/proyectos_maestria/segundo_semestre/arquitectura/MISW4202_G7_WZ8/experiment2/app/vistas/images/cvclinico{}.png'.format(user_id))
                file.show()
                return "Medical report served"
            return 'Unusual activity from {}'.format(id_patient)
        return "Not authorized"
