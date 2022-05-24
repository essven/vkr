from django.urls import include, path
from rest_framework import routers

from education_app import views
from education_app.views import DocumentDownload

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'parents', views.ParentViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'attendances', views.AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('documents/<pk>', DocumentDownload.as_view())
]