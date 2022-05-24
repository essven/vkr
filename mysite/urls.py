from django.contrib import admin
from django.urls import include, path

from education_app.authtoken import ExtendedAuthToken
from education_app.notifier import notify_mail

urlpatterns = [
    path('', include('education_app.urls')),
    path('admin/', admin.site.urls),
    path('api-token-auth/', ExtendedAuthToken.as_view()),
    path('notify/mails/', notify_mail.as_view())
]