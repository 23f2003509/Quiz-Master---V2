from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
from passlib.hash import bcrypt

from eraf_backend.eraf_config import localDevConfig
from eraf_backend.eraf_model import db, User
from eraf_backend.eraf_api import User_login,User_register,Add_subject,Add_chapter,Add_question,Add_quiz,Export_details

from eraf_backend.eraf_config import cache 
from eraf_backend.eraf_celery_config import *

from eraf_backend import eraf_task

from flask_mail import Mail
mail=Mail() 


def create_app():
    app = Flask(__name__)
    app.config.from_object(localDevConfig)
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)

    return app


def admin():
    admin = User.query.filter_by(is_admin=True).first()
    if admin is None:
        admin = User(username="admin", email="admin@gmail.com", 
                     password=bcrypt.hash("admin"),dob=datetime.strptime("01-01-2000", "%d-%m-%Y").date(),
                     fullname="admin",qualification="BS", is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin created")


app = create_app()
celery=celery_init_app(app)
CORS(app)
api = Api(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    celery.conf.beat_schedule = CeleryConfig.beat_schedule
    admin()




api.add_resource(User_login, "/login")
api.add_resource(Add_subject, "/add_subject")

api.add_resource(Add_chapter,"/add_chapter","/add_chapter/<int:sub_id>","/edit_chapter/<int:chap_id>","/delete_chapter/<int:chap_id>")

api.add_resource(Add_question,"/add_question/<int:quiz_id>","/edit_question/<int:question_id>","/delete_question/<int:question_id>")

api.add_resource(Add_quiz,"/add_quiz","/add_quiz/<int:chap_id>","/edit_quiz/<int:quiz_id>","/delete_quiz/<int:quiz_id>")

api.add_resource(User_register,"/register")

api.add_resource(Export_details,"/export_details")





if __name__ == "__main__":
    app.run(debug=True)