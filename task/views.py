#Python imports

# Django import
from django.shortcuts import render

#rest_framework imports
from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

#project imports
from .serializer import TaskSerializer
from users.utils import create_response
from .models import Task
from users.permissions import ClientPermission, EmployeePermission, ManagerPermission
from users.dao import get_user

# Create task 
class CreateTaskController(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ClientPermission]
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = get_user(request.user)
        data['createdby'] = user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return create_response("success", "Task created successfully", status.HTTP_201_CREATED, serializer.data)
        return create_response("status", "Data validation failed", status.HTTP_400_BAD_REQUEST)


#Delete Task
class DeleteTaskController(generics.DestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ManagerPermission]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(id=self.kwargs.get('pk'))
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return create_response("success", "Task deleted successfully", status.HTTP_200_OK)

#Assign Task
class AssignTaskController(generics.UpdateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ManagerPermission]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(id=self.kwargs.get('pk'))
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data
        instance = self.get_object()

        data['title'] = instance.title
        data['description'] = instance.description
        data['status'] = instance.status
        data['createdby'] = instance.createdby.id
        data['assignedby'] = get_user(request.user).id
        data['assignedto'] = get_user(data['assignedto']).id

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return create_response("success", "Task updated successfully", status.HTTP_200_OK, serializer.data)
        return create_response("status", "Data validation failed", status.HTTP_400_BAD_REQUEST)


#Change Task status
class UpdateTaskStatusController(generics.UpdateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, EmployeePermission]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(id=self.kwargs.get('pk'))
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get('status') not in ['PENDING', 'COMPLETED']:
            return create_response("status", "invalid status. allowd values: ['PENDING', 'COMPLETED']", status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        data = request.data
        instance = self.get_object()

        data['title'] = instance.title
        data['description'] = instance.description
        data['createdby'] = instance.createdby.id
        data['assignedby'] = instance.assignedby.id
        data['assignedto'] = instance.assignedto.id

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return create_response("success", "Status updated successfully", status.HTTP_200_OK, serializer.data)
        return create_response("status", "Data validation failed", status.HTTP_400_BAD_REQUEST)