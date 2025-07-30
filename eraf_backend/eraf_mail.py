import os
import logging
from flask_mail import Message
from flask import current_app

logging.getLogger("smtplib").setLevel(logging.ERROR)

def mail_config(to_address, subject, email_message, attachment=None):
    msg = Message(subject=subject,
                  recipients=[to_address],
                  html=email_message)

    if attachment and os.path.exists(attachment):
        with open(attachment, "rb") as f:
            msg.attach(
                filename=os.path.basename(attachment),
                content_type="text/csv",
                data=f.read()
            )
    elif attachment:
        print("Attachment file not found")

    with current_app.app_context():
        current_app.extensions['mail'].send(msg)
        print("Email sent successfully")



def build_html_email(username,unattempted_quizzes):
    html_body=f"""
    <html>
    <head>
    <style>
    table, th, td {{
        border: 1px solid black;
        border-collapse: collapse;
    }}
    th, td {{
        padding: 5px;
    }}
    </style>
    </head>
    <body>
    <h1>Hi {username},</h1>
    <p>Here are the unattempted quizzes:</p>
    <table>
    <tr>
    <th>Quiz Name</th>
    <th>Subject</th>
    <th>Chapter</th>
    </tr>
    """
    for quiz in unattempted_quizzes:
        html_body += f"""
        <tr>
        <td>{quiz.name}</td>
        <td>{quiz.chapter.subject.name}</td>
        <td>{quiz.chapter.name}</td>
        </tr>
        """
    html_body += """
    </table>
    <p>Thank you for using our service!</p>
    </body>
    </html>
    """
    return html_body



def build_monthly_html(username, month, avg_percentage, total_quizzes):
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2>Hi {username},</h2>
        <p>Here’s your monthly report for <strong>{month}</strong>:</p>
        <table border="1" cellpadding="10" style="border-collapse: collapse;">
          <tr style="background-color:#f2f2f2;">
            <th>Average Percentage</th>
            <th>Total Quizzes Attempted</th>
          </tr>
          <tr>
            <td align="center">{round(avg_percentage, 2)}%</td>
            <td align="center">{total_quizzes}</td>
          </tr>
        </table>
        <p style="margin-top:20px;">Keep learning and improving! 🚀</p>
      </body>
    </html>
    """
    return html_body