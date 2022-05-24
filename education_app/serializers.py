from django.contrib.auth import get_user_model
from rest_framework import serializers

from education_app.models import *


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ParentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        # excluded: ('groups', 'last_login', 'is_superuser', 'user_permissions', 'created_at')
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']  # {"name", "surname"}  # Student.field.names

    def create(self, request_data):
        """Create and return a new user."""
        UserModel = get_user_model()
        user = UserModel.objects.create_user(
            username=request_data['username'],
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            email=request_data['email'],
        )

        user.set_password(request_data['password'])
        user.save()

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  # {"name", "surname"}  # Student.field.names


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  # {"name", "surname"}  # Student.field.names


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  # {"name", "surname"}  # Student.field.names


class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
