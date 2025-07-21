from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
from passlib.hash import bcrypt

from eraf_backend.eraf_config import localDevConfig
from eraf_backend.eraf_model import db, User, Subject, Chapter, Quiz, Question, Score
from eraf_backend.eraf_api import User_login,Add_subject



def create_app():
    app = Flask(__name__)
    app.config.from_object(localDevConfig)
    db.init_app(app)

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
CORS(app)
api = Api(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    admin()


@app.route("/")
def hello():
    return "Hello World!"



api.add_resource(User_login, "/login")
api.add_resource(Add_subject, "/add_subject")







if __name__ == "__main__":
    app.run(debug=True)