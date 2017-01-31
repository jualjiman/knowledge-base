# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from knowledge_base.api.v1.routers import router
from knowledge_base.authentication import serializers
from knowledge_base.core.api.routers.single import SingleObjectRouter


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    serializer_class = serializers.LoginSerializer

    @detail_route(methods=['POST'])
    def login(self, request, *args, **kwargs):
        """
        User login.
        ---
        request_serializer: serializers.LoginSerializer
        response_serializer: serializers.LoginResponseSerializer

        type:
          email:
            required: true
            type: string
          password:
            required: true
            type: string

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
            user = serializer.get_user(serializer.data)

            response_serializer = serializers.LoginResponseSerializer(user)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

router.register(
    r'auth',
    AuthViewSet,
    base_name="auth",
    router_class=SingleObjectRouter
)
