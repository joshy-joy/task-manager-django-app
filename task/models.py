from django.db import models

from django.conf import settings

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    status = models.CharField(max_length=50, null=False)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Client', on_delete=models.CASCADE, null=False)
    assignedto = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Employee', on_delete=models.CASCADE, null=True)
    assignedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Manager', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Logs(models.Model):
    datetime = models.DateTimeField()
    description = models.CharField(max_length=100, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title