from flask_restful import Resource
from flask import jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity,current_user,create_access_token,get_jwt,verify_jwt_in_request

from eraf_backend.eraf_model import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime, timedelta
from passlib.hash import bcrypt





class User_login(Resource):
    def post(self):
        data = request.get_json()
        print(data)
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


class User_register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = bcrypt.hash(data.get('password'))
        dob = datetime.strptime(data.get('dob'), "%Y-%m-%d").date()
        fullname = data.get('fullname')
        qualification = data.get('qualification')
        user=User.query.filter_by(username=username).first()
        if user:
            return {'message': 'User already exists'}, 409
        
        user = User(username=username, email=email, password=password,dob=dob,
                    fullname=fullname,qualification=qualification)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

class Add_subject(Resource):
    @jwt_required()
    def get(self):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can view subject'}, 401
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
        current_user= get_jwt_identity() # get the current user STORED IN JWT AS IDENTITY
        if current_user != "admin":
            return {'message': 'only admin can update subject'}, 401
        data = request.get_json()
        print(data)
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
            return {'message': 'only admin can delete subject'}, 401
        data = request.get_json()
        subject_id = data.get('subject_id')
        subject = Subject.query.filter_by(id=subject_id).first()
        if not subject:
            return {'message': 'Subject not found'}, 404
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Subject deleted successfully'}, 200


##############################for chapter############################


class Add_chapter(Resource):
    @jwt_required()
    def get(self):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can view chapter'}, 401
        chapter=Chapter.query.all()
        chapter_json = []
        for c in chapter:
            chapter_json.append({"id":c.id,"name":c.name,
                                 "description":c.description,
                                 "subject_id":c.subject_id})
        return chapter_json,200
    

    @jwt_required()
    def post(self,sub_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can add chapter'}, 401
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        subject_id=Subject.query.filter_by(id=sub_id).first()
        print(subject_id)
        if not subject_id:
            return {'message': 'Subject not found'}, 404
        print(subject_id)
        chapter = Chapter(name=name, description=description,subject_id=subject_id.id)
        db.session.add(chapter)
        db.session.commit()
        return {'message': 'Chapter added successfully'}, 201
    

    @jwt_required()
    def put(self,chap_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can update chapter'}, 401
        data = request.get_json()
        print(data)
        name = data.get('name')
        description = data.get('description')
        chapter = Chapter.query.filter_by(id=chap_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        chapter.name = name
        chapter.description = description
        db.session.commit()
        return {'message': 'Chapter updated successfully'}, 200
    

    @jwt_required()
    def delete(self,chap_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can delete chapter'}, 401
        chapter = Chapter.query.filter_by(id=chap_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        db.session.delete(chapter)
        db.session.commit()
        return {'message': 'Chapter deleted successfully'}, 200
    

class Add_quiz(Resource):
    @jwt_required()
    def get(self):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can view quiz'}, 401
        quiz=Quiz.query.all()
        quiz_json = []
        for q in quiz:
            attempts=None
            if q.single_attempt:
                attempts=Score.query.filter_by(quiz_id=q.id).count()
                if attempts is not None and attempts>0:
                    quiz.is_active=False
            # Convert duration in minutes → HH:MM:SS string
            duration_str = str(timedelta(minutes=q.duration))
            quiz_json.append({"id":q.id,"name":q.name,
                              "description":q.description,
                              "chapter_id":q.chapter_id,
                              "is_active":q.is_active,
                              "date_created":q.date_created,
                              "duration":duration_str,
                              "single_attempt":q.single_attempt,
                              'chapter':q.chapter.name,
                              "subject":q.chapter.subject.name,})
        return quiz_json,200
    

    @jwt_required()
    def post(self,chap_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can update quiz'}, 401
        data = request.get_json()
        print(data)
        name = data.get('name')
        description = data.get('description')
        chapter_id=Chapter.query.filter_by(id=chap_id).first()
        if not chapter_id:
            return {'message': 'Chapter not found'}, 404
        # Convert HH:MM:SS to minutes
        duration_parts = list(map(int, data.get('duration').split(':')))
        duration_minutes = duration_parts[0] * 60 + duration_parts[1]
        print(chapter_id)
        quiz = Quiz(name=name, description=description,chapter_id=chapter_id.id,
                    single_attempt=data.get('single_attempt'),
                    duration=duration_minutes,
                    date_created=datetime.strptime(data.get('date_created'), '%Y-%m-%d').date())
        db.session.add(quiz)
        db.session.commit()
        return {'message': 'Quiz added successfully'}, 201
    
    @jwt_required()
    def put(self,quiz_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can update quiz'}, 401
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        quiz.name = name
        quiz.description = description
        quiz.single_attempt=data.get('single_attempt')

        # 👇 Convert HH:MM:SS string to total minutes (int)
        duration_parts = list(map(int, data.get('duration').split(':')))
        quiz.duration = duration_parts[0] * 60 + duration_parts[1]

        quiz.date_created=datetime.strptime(data.get('date_created'), '%Y-%m-%d')
        
        
        quiz.chapter_id=data.get('chapter_id')

        db.session.commit()
        return {'message': 'Quiz updated successfully'}, 200
    

    @jwt_required()
    def delete(self,quiz_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can delete quiz'}, 401
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        db.session.delete(quiz)
        db.session.commit()
        return {'message': 'Quiz deleted successfully'}, 200




class Add_question(Resource):
    @jwt_required()
    def get(self,quiz_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can view question'}, 401
        question=Question.query.filter_by(quiz_id=quiz_id).all()
        question_json = []
        for q in question:
            question_json.append({"id":q.id,
                                  "question_tag":q.question_tag,
                                  "question_statement":q.question_statement,
                                  "option1":q.option1,
                                  "option2":q.option2,
                                  "option3":q.option3,
                                  "option4":q.option4,
                                  "correct_answer":q.correct_answer,
                                  "quiz_id":q.quiz_id,
                                  "chapter_id":q.chapter_id})
        return question_json,200

    
    @jwt_required()
    def post(self,quiz_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can add question'}, 401
        data = request.get_json()
        chapter_id=Quiz.query.filter_by(id=quiz_id).first()
        print(chapter_id)
        chap_id=chapter_id.chapter_id
        if not chapter_id:
            return {'message': 'Chapter not found'}, 404

        question = Question(question_tag=data.get('question_tag'),
                            question_statement=data.get('question_statement'),
                            option1=data.get('option1'),
                            option2=data.get('option2'),
                            option3=data.get('option3'),
                            option4=data.get('option4'),
                            correct_answer=data.get('correct_answer'),
                            quiz_id=quiz_id,
                            chapter_id=chap_id)
        db.session.add(question)
        db.session.commit()
        return {'message': 'Question added successfully'}, 201
    
    @jwt_required()
    def put(self,question_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can update question'}, 401
        data = request.get_json()
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message': 'Question not found'}, 404
        question.question_tag = data.get('question_tag')
        question.question_statement = data.get('question_statement')
        question.option1=data.get('option1')
        question.option2=data.get('option2')
        question.option3=data.get('option3')
        question.option4=data.get('option4')
        question.correct_answer=data.get('correct_answer')
        db.session.commit()
        return {'message': 'Question updated successfully'}, 200
    
    @jwt_required()
    def delete(self,question_id):
        current_user= get_jwt_identity()
        if current_user != "admin":
            return {'message': 'only admin can delete question'}, 401
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message': 'Question not found'}, 404
        db.session.delete(question)
        db.session.commit()
        return {'message': 'Question deleted successfully'}, 200
    



