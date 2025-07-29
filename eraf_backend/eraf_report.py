
import os
import csv
from datetime import datetime
from eraf_backend.eraf_model import db, Quiz, Score

def get_monthly_stats(user):
    month = datetime.now().strftime("%B")
    scores = Score.query.filter_by(user_id=user.id).all()
    total_quizzes = len(scores)
    if total_quizzes > 0:
        avg_percentage = sum([q.percentage for q in scores]) / total_quizzes
    else:
        avg_percentage = 0
    return month, avg_percentage, total_quizzes


def get_user_scores_csv(user_id):
    reports_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    file_path = os.path.join(
        reports_dir, f"{user_id}_quiz_reports_{datetime.now().strftime('%Y-%m-%d')}.csv"
    )

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Quiz ID", "Quiz Title", "Obtained Marks", "Total Marks", "Completion Date"])

        quizzes = db.session.query(
            Quiz.id,
            Quiz.name,
            Score.score.label("obtained_marks"),
            Score.total_possible_score.label("total_marks"),
            Score.date.label("completion_date")
        ).join(Score, Score.quiz_id == Quiz.id).filter(Score.user_id == user_id).all()

        for quiz in quizzes:
            writer.writerow([
                quiz.id,
                quiz.name,
                quiz.obtained_marks,
                quiz.total_marks,
                quiz.completion_date.strftime("%Y-%m-%d") if quiz.completion_date else "N/A"
            ])
    
    return file_path
