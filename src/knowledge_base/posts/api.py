# # -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated

from knowledge_base.api.v1.routers import router
from knowledge_base.core.api import mixins
from knowledge_base.core.api.viewsets import GenericViewSet
from knowledge_base.core.api.viewsets.nested import NestedViewset

from knowledge_base.posts import serializers
from knowledge_base.posts.models import Area, Post, Subject
from knowledge_base.utils.urlresolvers import get_query_params


class AreaViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Area.objects.filter(is_active=True)

    permission_classes = [IsAuthenticated, ]

    serializers_class = serializers.AreaSerializer
    list_serializer_class = serializers.AreaURISerializer
    retrieve_serializer_class = serializers.AreaSerializer

    def list(self, request, *args, **kwargs):
        """
        Return a list of areas.
        ---
        response_serializer: serializers.AreaSerializer

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
        return super(AreaViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        """
        Returns data of an area.
        ---
        response_serializer: serializers.AreaSerializer

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
        return super(AreaViewSet, self).retrieve(request, pk)


class SubjectViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    NestedViewset
):

    permission_classes = [IsAuthenticated, ]

    serializers_class = serializers.SubjectSerializer
    list_serializer_class = serializers.SubjectURISerializer
    retrieve_serializer_class = serializers.SubjectSerializer

    parent_model = Area
    parent_model_name = 'Area'
    parent_lookup_field = 'area_pk'

    def get_queryset(self, *args, **kwargs):
        """
        Return active subjects for specific area or all items.
        """
        queryset = Subject.objects.filter(is_active=True)

        if self.parent_lookup_field in kwargs:
            queryset = queryset.filter(area=kwargs[self.parent_lookup_field])

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Return a list of subjects that belongs to specific area.
        ---
        response_serializer: serializers.SubjectURISerializer
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
        return super(SubjectViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Get a data for a subject that belongs to specific area.
        ---
        response_serializer: serializers.SubjectSerializer
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
        return super(SubjectViewSet, self).retrieve(request, *args, **kwargs)


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    NestedViewset
):

    permission_classes = [IsAuthenticated, ]

    serializers_class = serializers.PostSerializer
    list_serializer_class = serializers.PostURISerializer
    retrieve_serializer_class = serializers.PostSerializer

    parent_model = Subject
    parent_model_name = 'Subject'
    parent_lookup_field = 'subject_pk'

    def get_queryset(self, *args, **kwargs):
        """
        Return active posts for specific subject or all items.
        """
        queryset = Post.objects.filter(is_active=True)

        if self.parent_lookup_field in kwargs:
            queryset = queryset.filter(
                subject=kwargs[self.parent_lookup_field]
            )

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Return a list of posts that belongs to specific subject.
        ---
        response_serializer: serializers.PostSerializer
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
        return super(PostViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Get a data for a post that belongs to specific subject.
        ---
        response_serializer: serializers.PostSerializer
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
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)


class ProfilePostViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated, ]

    serializers_class = serializers.PostSerializer
    list_serializer_class = serializers.PostSerializer
    retrieve_serializer_class = serializers.PostSerializer
    update_serializer_class = serializers.PostSerializer
    create_serializer_class = serializers.PostCreateSerializer

    def get_queryset(self, *args, **kwargs):
        query_params = get_query_params(self.request)
        is_active = query_params.get('isactive')

        #
        # This set of endpoints are used only to manage the posts of the
        # request user, so only those post should be visible in all cases.
        #
        request_user = self.request.user
        queryset = Post.objects.filter(author=request_user)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Allows to create a post in the knowledge base.
        ---
        request_serializer: serializers.PostDocSerializer
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
        # Used to pass extra information that was obtained from the
        # request info.
        #
        kwargs['extra_data'] = {
            'author': request.user.id
        }
        return super(ProfilePostViewSet, self).create(request, *args, **kwargs)

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
        return super(ProfilePostViewSet, self).partial_update(request, pk)

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
        return super(ProfilePostViewSet, self).destroy(request, pk)

    def list(self, request, *args, **kwargs):
        """
        Return a list of posts.
        ---
        response_serializer: serializers.PostSerializer

        parameters:
            - name: isactive
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
        return super(ProfilePostViewSet, self).list(request, *args, **kwargs)

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
        return super(ProfilePostViewSet, self).retrieve(request, pk)

router.register(
    r'areas',
    AreaViewSet,
    base_name='area'
)

router.register_nested(
    r'areas',
    r'subjects',
    SubjectViewSet,
    parent_lookup_name='area',
    base_name='subject'
)

router.register_nested(
    r'subjects',
    r'posts',
    PostViewSet,
    parent_lookup_name='subject',
    base_name='post',
    depth_level=2
)

#
# Set of endpoints used to manage user's posts.
#
router.register(
    r'me/posts',
    ProfilePostViewSet,
    base_name='me-post'
)
