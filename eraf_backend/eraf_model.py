from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False) 
    dob = db.Column(db.Date, nullable=True)
    fullname = db.Column(db.String(220), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    qualification = db.Column(db.String(170),  nullable=False)

    scores=db.relationship('Score', backref='user', cascade='all, delete')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    chapters=db.relationship('Chapter', backref='subject', cascade='all, delete')
    scores=db.relationship('Score', backref='subject', cascade='all, delete')

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    quizs=db.relationship('Quiz', backref='chapter', cascade='all, delete')
    scores=db.relationship('Score', backref='chapter', cascade='all, delete')
    questions=db.relationship('Question', backref='chapter', cascade='all, delete')


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    single_attempt = db.Column(db.Boolean, nullable=True)

    questions=db.relationship('Question', backref='quiz', cascade='all, delete')
    scores=db.relationship('Score', backref='quiz', cascade='all, delete')

    

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_tag = db.Column(db.String(100), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    total_possible_score=db.Column(db.Integer, nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    percentage=db.Column(db.Float, nullable=False)

