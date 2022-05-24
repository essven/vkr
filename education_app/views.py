from wsgiref.util import FileWrapper

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import Max, Sum
from django.http import HttpResponse
from rest_framework import viewsets, views
from rest_framework.decorators import action

from education_app.serializers import *
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class StudentViewSet(viewsets.ModelViewSet):
    # print("Students required")
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer


class ParentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Parent.objects.all().order_by('id')
    serializer_class = ParentSerializer


class AccountViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('id')
    serializer_class = AccountSerializer


class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer

    @action(methods=['get'], detail=True, url_path='students', url_name='students')
    def get_students(self, request, pk=None):
        queryset = Student.objects.filter(group__pk=pk)
        serializer = StudentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
  permission_classes = [IsAuthenticated]
  queryset = Employee.objects.all().order_by('id')
  serializer_class = EmployeeSerializer

  @action(methods=['get'], detail=True, url_path='groups', url_name='groups')
  def get_groups(self, request, pk=None):
    queryset = Group.objects.filter(teacher__pk=pk)
    serializer = GroupSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


class ScheduleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Schedule.objects.all().order_by('id')
    serializer_class = ScheduleSerializer


class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer

    @action(methods=['get'], detail=True, url_path='tasks', url_name='tasks')
    def get_tasks(self, request, pk=None):
      queryset = Task.objects.filter(item__pk=pk)
      serializer = TaskSerializer(queryset, many=True, context={'request': request})
      return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
  permission_classes = [IsAuthenticated]
  queryset = Course.objects.all().order_by('id')
  serializer_class = CourseSerializer

  @action(methods=['get'], detail=True, url_path='items', url_name='items')
  def get_items(self, request, pk=None):
    queryset = Item.objects.filter(course__pk=pk)
    serializer = ItemSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

  @action(methods=['get'], detail=True, url_path='grate', url_name='grate')
  def get_grate(self, request, pk=None):
      items = map(lambda item: item.id, Item.objects.filter(course__pk=pk))
      tasks = map(lambda task: task.id, Task.objects.filter(item__pk__in=items))
      answers = Answer.objects.filter(task__pk__in=tasks).filter(student__pk=request.query_params.get('student_id')).order_by('task')
      best_rates = answers.values('task').annotate(Max('rate')).order_by('task')
      rates = answers.filter(task__pk__in=map(lambda x: x['task'], best_rates)).filter(rate__in=map(lambda x: x['rate__max'], best_rates))
      if request.query_params.get('sum').lower() == 'true':
          return Response(rates.aggregate(total_rate=Sum('rate')))
      else:
          serializer = AnswerSerializer(rates, many=True, context={'request': request})
          return Response(serializer.data)





class TaskViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
  permission_classes = [IsAuthenticated]
  queryset = Task.objects.all().order_by('id')
  serializer_class = TaskSerializer

  @action(methods=['get'], detail=True, url_path='answers', url_name='answers')
  def get_answers(self, request, pk=None):
    queryset = Answer.objects.filter(task__pk=pk)
    serializer = AnswerSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all().order_by('id')
    serializer_class = AnswerSerializer

    @action(methods=['get'], detail=True, url_path='rate', url_name='rate')
    def get_rate(self, request, pk=None):
        queryset = Answer.objects.filter(student__pk=pk)
        serializer = AnswerSerializer(queryset, many=True, context={'request': request})

        return Response(max(serializer.data, key=lambda answer: answer['rate']))

class AttendanceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Attendance.objects.all().order_by('id')
    serializer_class = AttendanceSerializer

class DocumentDownload(views.APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='documents', url_name='documents')
    def get(self, request, pk=None):
        print("Запрос документа (" + pk + ") от: " + str(request.user))
        documentsLocation = "./media/documents"
        resultFile = open(documentsLocation + "/" + pk, 'rb')
        response = HttpResponse(FileWrapper(resultFile), content_type='multipart/form-data')
        return response