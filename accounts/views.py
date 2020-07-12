from django.conf import settings as s
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError
from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status, APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.shortcuts import get_list_or_404
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_filters import rest_framework as filters

from accounts.filter import UserFilter
from accounts.models import User
from accounts.serializers import (TokenSerializer, UserSerializer, UserInspectionSerializer,
                                  LoginUserSerializer, GroupsSerializer)
from accounts.permissions import IsPaidUser, AllowedByGroupLevel
from inspections.models import Inspection

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class IsPaidUserView(APIView):
    permission_classes = (IsAuthenticated, IsPaidUser)

    def get(self, request):
        content = {'paid': True}
        return Response(content)


class IsLoggedInView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'loggedin': True}
        return Response(content)


class SignupView(generics.CreateAPIView):
    # /accounts/register
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        password = request.POST.get("password", "")
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        if not password and not email:
            return Response(
                data={
                    "error": "missing params"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            new_user = User.objects.create_user(
                password=password, email=email, username=username
            )
        except IntegrityError:
            return Response(
                status=status.HTTP_409_CONFLICT
            )

        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.CreateAPIView):
    # /accounts/login/
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user is not None and user.check_password(password):
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args,
                                 **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': '{}?reset_password_token={}'.format(
            s.FRONTEND_URL,
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html',
                                          context)
    email_plaintext_message = render_to_string(
        'email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
    permission_classes = (permissions.DjangoModelPermissions, AllowedByGroupLevel)

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return self.queryset.exclude(pk=self.request.user.pk)

        return self.queryset

    @action(url_path='(?P<id_user_assigned>\d+)/inspections',
            methods=['get'], detail=False)
    def inspections(self, request, id_user_assigned=None):
        queryset = get_list_or_404(Inspection, user_assigned=id_user_assigned)
        serializer = UserInspectionSerializer(queryset, many=True, )
        return Response(serializer.data)

    def perform_update(self, serializer):
        password = serializer.validated_data.get('password')
        instance = serializer.save()
        if password:
            instance.set_password(password)
            instance.save()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupsSerializer
    queryset = Group.objects.all()
    permission_classes = (permissions.DjangoModelPermissions,)
