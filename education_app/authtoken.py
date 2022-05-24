from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class ExtendedAuthToken(ObtainAuthToken):

    # def patch(self, request, args, **kwargs):
    #     for user in User.objects.all():
    #         Token.objects.get_or_create(user=user)

    def post(self, request, *args, **kwargs):
        print("{'username': '" + request.data.get("username") + "'} required Token")
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk
        })
