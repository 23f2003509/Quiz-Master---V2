from flask_restful import Resource
from flask import jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity,current_user,create_access_token,get_jwt,verify_jwt_in_request

from eraf_backend.eraf_model import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime
from passlib.hash import bcrypt





class User_login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        if user and bcrypt.verify(password, user.password):
            access_token = create_access_token(identity=username,additional_claims={"user_id":user.id})
            if user.is_admin:
                return {'message': 'Admin login successful', 
                        'access_token': access_token, 'user_id': user.id,
                        'username':user.username}, 200
            else:
                return {'message': 'User login successful', 'access_token': access_token, 
                        'user_id': user.id,'username':user.username}, 200
        else:
            return {'message': 'Invalid username or password'}, 401


class Add_subject(Resource):
    @jwt_required()
    def get(self):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can add subject'}, 401
        subject=Subject.query.all()
        subject_json = []
        for s in subject:
            chapters=Chapter.query.filter_by(subject_id=s.id).all()
            chapters_json = []
            for c in chapters:
                chapters_json.append({"id":c.id,"name":c.name,
                                      "description":c.description})
            subject_json.append({"id":s.id,"name":s.name,
                                 "description":s.description,
                                 "chapters":chapters_json})
        return subject_json,200

    @jwt_required()
    def post(self):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can add subject'}, 401
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        return {'message': 'Subject added successfully'}, 201


    @jwt_required()
    def put(self):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can add subject'}, 401
        data = request.get_json()
        subject_id = data.get('subject_id')
        name = data.get('name')
        description = data.get('description')
        subject = Subject.query.filter_by(id=subject_id).first()
        if not subject:
            return {'message': 'Subject not found'}, 404
        subject.name = name
        subject.description = description
        db.session.commit()
        return {'message': 'Subject updated successfully'}, 200
    

    @jwt_required()
    def delete(self):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can add subject'}, 401
        data = request.get_json()
        subject_id = data.get('subject_id')
        subject = Subject.query.filter_by(id=subject_id).first()
        if not subject:
            return {'message': 'Subject not found'}, 404
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Subject deleted successfully'}, 200