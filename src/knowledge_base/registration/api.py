# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny

from knowledge_base.api.v1.routers import router
from knowledge_base.core.api import viewsets
from knowledge_base.core.api.mixins import base as base_mixins
from knowledge_base.core.api.routers.single import SingleObjectRouter
from knowledge_base.registration.serializers import (
    RegistrationProfileSerializer,
    RegistrationResponseSerializer,
)


class RegistrationViewset(
    base_mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    permission_classes = (AllowAny,)

    serializer_class = RegistrationProfileSerializer
    create_serializer_class = RegistrationProfileSerializer
    retrieve_serializer_class = RegistrationResponseSerializer

    def get_queryset(self):
        user_model = get_user_model()
        return user_model.objects.all()

    @detail_route(methods=['POST'])
    def signup(self, request):
        """
        User registration.
        ---
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


router.register(
    r'auth',
    RegistrationViewset,
    base_name="auth-registration",
    router_class=SingleObjectRouter
)
