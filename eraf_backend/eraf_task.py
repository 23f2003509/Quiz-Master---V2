

from celery import shared_task
from eraf_backend.eraf_model import db, User, Subject, Chapter, Quiz, Question, Score
from eraf_backend.eraf_mail import mail_config, build_html_email

from eraf_backend.eraf_report import get_monthly_stats, get_user_scores_csv  
from eraf_backend.eraf_mail import build_monthly_html

@shared_task
def daily_reminder():
    users = User.query.all()
    quizs=Quiz.query.all()
    for user in users:
        if user.is_admin:
            continue
        unattempted_quizzes = []
        for quiz in quizs:
            attempt=Score.query.filter_by(user_id=user.id,quiz_id=quiz.id).first()
            if not attempt:
                unattempted_quizzes.append(quiz)
        if unattempted_quizzes:
            html_body=build_html_email(user.username,unattempted_quizzes)
            mail_config(
                to_address=user.email,
                subject='Reminder: Unattempted Quizzes',
                email_message=html_body)

@shared_task
def export_scores(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            print("User not found")
            return

        file_path = get_user_scores_csv(user_id)

        mail_config(
            to_address=user.email,
            subject="Quiz Report",
            email_message="Your Quiz Report is attached with this mail",
            attachment=file_path
        )
    except Exception as e:
        print(f"Error exporting scores: {e}")



@shared_task
def send_monthly_report():
    users = User.query.filter_by(is_admin=False).all()
    for user in users:
        month, avg_percentage, total_quizzes = get_monthly_stats(user)
        html_body = build_monthly_html(user.username, month, avg_percentage, total_quizzes)
        mail_config(
            to_address=user.email,
            subject='Monthly Report',
            email_message=html_body
        )


