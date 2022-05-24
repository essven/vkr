from django.core import mail
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def get_group_address():
    pass


class notify_mail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # request.data - content post-запроса

        subject = request.data["subject"]
        body = request.data["body"]
        to_emails = request.data["to"]

        if isinstance(to_emails, list) and isinstance(subject, str) and isinstance(body, str):


            with mail.get_connection() as connection:
                mail.EmailMessage(
                    subject,  # subject - Тема письма
                    body,  # body - Сообщение
                    None,  # from - От кого отправить сообщение. default: DEFAULT_FROM_EMAIL
                    to_emails,  # to - Список или кортеж адресов получателей
                    connection=connection,
                ).send()


            return Response({
                "status": "notify sended",
                "request": request.data
            })

        return Response({
            "status": "notify error",
            "request": request.data
        })
