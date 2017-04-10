# -*- coding: utf-8 -*-
import os

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knowledge_base.api.v1.routers import router
from knowledge_base.core.api.mixins import base as base_mixins
from knowledge_base.core.api.routers.single import SingleObjectRouter
from knowledge_base.core.api.viewsets import GenericViewSet

from knowledge_base.users.serializers import (
    ProfileSerializer, ProfileUpdateImageSerializer,
    ProfileUpdateSerializer, SearchUserSerializer
)
from knowledge_base.utils.urlresolvers import get_query_params


class ProfileViewSet(
    base_mixins.RetrieveModelMixin,
    base_mixins.PartialUpdateModelMixin,
    GenericViewSet
):

    serializer_class = ProfileSerializer
    retrieve_serializer_class = ProfileSerializer
    update_serializer_class = ProfileUpdateSerializer
    change_image_serializer_class = ProfileUpdateImageSerializer

    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, pk=None):
        """
        Gets the user profile information.
        ---
        response_serializer: ProfileSerializer
        omit_serializer: false
        responseMessages:
            - code: 200
              message: OK
            - code: 403
              message: FORBIDDEN
            - code: 404
              message: NOT FOUND
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(ProfileViewSet, self).retrieve(request)

    def partial_update(self, request):
        """
        Updates the user profile information.
        ---
        request_serializer: ProfileSerializer
        response_serializer: ProfileSerializer
        omit_serializer: false
        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: BAD REQUEST
            - code: 403
              message: FORBIDDEN
            - code: 404
              message: NOT FOUND
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(ProfileViewSet, self).partial_update(request)

    @detail_route(methods=['PUT'])
    def change_image(self, request, *args, **kwars):
        """
        Allows the session's user to update his profile image.
        ---
        request_serializer: ProfileUpdateImageSerializer
        response_serializer: ProfileSerializer
        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        user = request.user

        # Serializer that will be used to validate the information.
        update_serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
            action='change_image'
        )

        update_serializer.is_valid(raise_exception=True)
        self.perform_delete_image()
        updated_user = update_serializer.save()

        retrieve_serializer = self.get_serializer(
            updated_user,
            action='retrieve'
        )
        return Response(retrieve_serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['DELETE'])
    def delete_image(self, request, *args, **kwars):
        """
        Allows delete the image for current user.
        omit_serializer: true
        ---
        responseMessages:
            - code: 204
              message: NO CONTENT
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        self.perform_delete_image()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user

    def perform_delete_image(self):
        user = self.request.user
        if user.photo and os.path.isfile(user.photo.path):
            os.remove(user.photo.path)
            user.photo = None
            if user.thumbnail and os.path.isfile(user.thumbnail.path):
                os.remove(user.thumbnail.path)
                user.thumbnail = None

            user.save()


class SearchUserViewSet(base_mixins.ListModelMixin, GenericViewSet):

    serializer_class = SearchUserSerializer
    list_serializer_class = SearchUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, *args, **kwargs):

        queryset = get_user_model().objects.filter(is_active=True)
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(email__icontains=q)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Return a list of users, that matches with the given word.
        ---
        response_serializer: SearchUserSerializer

        parameters:
            - name: q
              description: Search word.
              paramType: query
              type: string

        responseMessages:
            - code: 200
              message: OK
            - code: 403
              message: FORBIDDEN
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(SearchUserViewSet, self).list(request, *args, **kwargs)

router.register(
    'me',
    ProfileViewSet,
    base_name='me',
    router_class=SingleObjectRouter
)

router.register(
    r'users/search',
    SearchUserViewSet,
    base_name='users-search'
)
