from app import create_app
from .modelos import db
from flask_restful import Api
from .vistas import VistaLogIn,VistaSignIn,VistaGetMedicalHistory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
app = create_app('default')
app_context = app.app_context()
app_context.push()
app.debug = True
db.init_app(app)
db.create_all()

cors = CORS(app)
api = Api(app)
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaGetMedicalHistory, '/medical_info/<int:id_patient>')

jwt = JWTManager(app)


    

