from django.contrib.auth.models import User

def get_user(username):
    return User.objects.get(username=username)
