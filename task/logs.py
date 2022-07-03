from datetime import datetime

from .models import Logs

def create_logs(action, user, task):
    description = " ".join['Task', action]
    log = Logs(datetime=datetime.now(), description=description, user=user, task=task)
    log.save()
