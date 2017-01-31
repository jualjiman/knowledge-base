# -*- coding: utf-8 -*-
from rest_framework.permissions import AllowAny

from knowledge_base.api.v1.routers import router
from knowledge_base.core.api import mixins
from knowledge_base.core.api.viewsets import GenericViewSet

from knowledge_base.posts import serializers
from knowledge_base.posts.models import Post
from knowledge_base.utils.urlresolvers import get_query_params


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [AllowAny, ]

    serializers_class = serializers.PostSerializer
    create_serializer_class = serializers.PostSerializer
    list_serializer_class = serializers.PostSerializer
    retrieve_serializer_class = serializers.PostSerializer
    update_serializer_class = serializers.PostSerializer

    def create(self, request, *args, **kwargs):
        """
        Allows to create a post in the knowledge base.
        ---
        request_serializer: serializers.PostSerializer
        response_serializer: serializers.PostSerializer

        responseMessages:
            - code: 201
              message: CREATED
            - code: 400
              message: BAD REQUEST
            - code: 403
              message: FORBIDDEN
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(PostViewSet, self).create(request, *args, **kwargs)

    def partial_update(self, request, pk=None):
        """
        Updates a post.
        ---
        request_serializer: serializers.PostSerializer
        response_serializer: serializers.PostSerializer

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
        return super(PostViewSet, self).partial_update(request, pk)

    def destroy(self, request, pk=None):
        """
        Deletes a post.
        ---
        omit_serializer: true
        responseMessages:
            - code: 204
              message: NO CONTENT
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
        return super(PostViewSet, self).destroy(request, pk)

    def list(self, request, *args, **kwargs):
        """
        Return a list of posts.
        ---
        response_serializer: serializers.PostSerializer

        parameters:
            - name: isActive
              description: if "true", returns only active registers.
              paramType: query
              type: boolean

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
        return super(PostViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        """
        Returns data of a post.
        ---
        response_serializer: serializers.PostSerializer
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
        return super(PostViewSet, self).retrieve(request, pk)

    def get_queryset(self, *args, **kwargs):
        query_params = get_query_params(self.request)
        is_active = query_params.get('isActive', None)

        queryset = Post.objects.all()

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset

router.register(
    r'posts',
    PostViewSet,
    base_name='post'
)
