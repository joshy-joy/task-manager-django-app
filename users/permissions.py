from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework.permissions import BasePermission

from django.contrib.auth.models import User

# Permission Class for Client
class ClientPermission(BasePermission):
    """
    Allows access only to "Client" users.
    """
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if not user:
            return False
        return user.groups.filter(name='Client')

# Permission Class for Employee
class EmployeePermission(BasePermission):
    """
    Allows access only to "Client" users.
    """
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if not user:
            return False
        return user.groups.filter(name='Employee')

# Permission Class for Manager
class ManagerPermission(BasePermission):
    """
    Allows access only to "Client" users.
    """
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if not user:
            return False
        return user.groups.filter(name='Manager')


def set_user_permissions(role, instance):
    content_type = ContentType.objects.get(app_label='auth', model='user')
    if role == "Manager":
        group, _ = Group.objects.get_or_create(name='Manager')
        delete, _ = Permission.objects.get_or_create(codename='DELETE', name='Can Delete Task', content_type=content_type)
        assign, _ = Permission.objects.get_or_create(codename='ASSIGN', name='Can Assign Task', content_type=content_type)
        group.permissions.add(delete)
        group.permissions.add(assign)
        instance.groups.add(group)
    elif role == "Employee":
        group, _ = Group.objects.get_or_create(name='Employee')
        complete, _ = Permission.objects.get_or_create(codename='COMPLETE', name='Can Complete Task', content_type=content_type)
        group.permissions.add(complete)
        instance.groups.add(group)
    elif role == "Client":
        group, _ = Group.objects.get_or_create(name='Client')
        create, _ = Permission.objects.get_or_create(codename='CREATE', name='Can Complete Task', content_type=content_type)
        group.permissions.add(create)
        instance.groups.add(group)
    return True
