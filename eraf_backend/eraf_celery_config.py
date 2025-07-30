from flask import Flask
from celery import Celery, Task


class CeleryConfig:
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/1"
    timezone = "Asia/Kolkata"
    enable_utc = True  
    beat_schedule = { 
        "add-every-10-seconds_1": {
            "task": "eraf_backend.eraf_task.daily_reminder", 
            "schedule": 20.0, 
        },
         "add-every-10-seconds_2": {
            "task": "eraf_backend.eraf_task.send_monthly_report", 
            "schedule": 20.0, 
        },

    }


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app
