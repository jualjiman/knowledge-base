# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from knowledge_base.api.v1.routers import router
from knowledge_base.core.api import mixins, viewsets
from knowledge_base.core.api.routers.single import SingleObjectRouter
from knowledge_base.registration.serializers import (
    ChangePasswordSerializer,
    NewPasswordSerializer,
    RegistrationProfileSerializer,
    RegistrationResponseSerializer,
)


class RegistrationViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    permission_classes = (AllowAny,)

    serializer_class = RegistrationProfileSerializer
    create_serializer_class = RegistrationProfileSerializer
    retrieve_serializer_class = RegistrationResponseSerializer

    def get_queryset(self):
        return get_user_model.objects.all()

    def create(self, request):
        """
        Register user
        ---

        type:
          photo:
            required: false
            type: file

        request_serializer: RegistrationProfileSerializer
        response_serializer: RegistrationProfileSerializer

        omit_serializer: false

        parameters_strategy: merge
        omit_parameters:
            - path

        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 201
              message: CREATED
            - code: 500
              message: INTERNAL SERVER ERROR

        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(RegistrationViewset, self).create(request)


class PasswordViewset(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = NewPasswordSerializer

    @detail_route(methods=['POST'])
    def new_password(self, request):
        """
        New password
        ---

        type:
          email:
            required: true
            type: string

        request_serializer: NewPasswordSerializer
        omit_serializer: true

        parameters_strategy: merge
        parameters:
            - name: email
              description: User mail.
              required: true
              type: string
              paramType: form

        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 201
              message: CREATED
            - code: 500
              message: INTERNAL SERVER ERROR

        consumes:
            - application/json
        produces:
            - application/json
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(
                {
                    'detail': 'Mail sent successfully'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @detail_route(methods=['POST'])
    def change_password(self, request):
        """
        Change password
        ---

        type:
          email:
            required: true
            type: string
          token:
            required: true
            type: string

        request_serializer: ChangePasswordSerializer
        omit_serializer: false

        parameters:
            - name: email
              description: User mail.
              required: true
              type: string
              paramType: form
            - name: token
              description: token validation.
              required: true
              type: string
              paramType: form

        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 200
              message: OK
            - code: 500
              message: INTERNAL SERVER ERROR

        consumes:
            - application/json
        produces:
            - application/json
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(
                "Password successfully changed",
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_serializer_class(self, action=None):
        """
        Returns the proper serializer for the current request.
        """
        if self.action == 'new_password':
            return NewPasswordSerializer

        elif self.action == 'change_password':
            return ChangePasswordSerializer


router.register(
    r'auth/signup',
    RegistrationViewset,
    base_name="registration",
)

router.register(
    r'auth',
    PasswordViewset,
    base_name="auth",
    router_class=SingleObjectRouter
)
