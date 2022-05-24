import enum

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

fileSystemStorage = FileSystemStorage(location="./media/documents", base_url="/documents/")


# Authorization
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# python manage.py migrate
class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    surname = models.CharField(max_length=225, default=None)
    phone_number = models.CharField(max_length=15, default=None)
    account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)

    def __str__(self):
        return f"{self.name}"


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.CharField(max_length=255, default=None)  # change to enums
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    teacher = models.ForeignKey(Employee, on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return f"Group-{self.number}"


class Parent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    phone_number = models.CharField(max_length=15, default=None)
    job_place = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.name


class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    surname = models.CharField(max_length=255, default=None)
    phone_number = models.CharField(max_length=15, default=None)
    school = models.CharField(max_length=255, default=None)
    grade = models.CharField(max_length=255, default=None)
    location = models.CharField(max_length=255, default=None)
    parent = models.ManyToManyField(Parent, default=None, blank=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    group = models.ManyToManyField(Group, default=None, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class UnActiveStudent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    surname = models.CharField(max_length=255, default=None)
    phone_number = models.CharField(max_length=15, default=None)
    school = models.CharField(max_length=255, default=None)
    grade = models.CharField(max_length=255, default=None)
    location = models.CharField(max_length=255, default=None)
    parent = models.ManyToManyField(Parent, default=None, blank=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    group = models.ManyToManyField(Group, default=None, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    day = models.CharField(max_length=255, default=None)
    time = models.TimeField(name="time", default=None)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, default=None, blank=True, null=True)  # this type of foreign key - Ok


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, default=None, null=True)
    src = models.URLField(verbose_name="source of course item", name="item", default=None, null=True)
    description = models.CharField(max_length=255, default=None, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None)
    document = models.FileField(storage=fileSystemStorage, null=True)
    rate = models.IntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'id={self.id}, task_id={self.task.id}, rate={self.rate}, student_id={self.student.id}'


class Attendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, default=None)
    date = models.DateTimeField(default=None)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, default=None)
    was = models.BooleanField(default=None)
    reason = models.CharField(max_length=128, default=None, null=True)

class Application(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default=None)