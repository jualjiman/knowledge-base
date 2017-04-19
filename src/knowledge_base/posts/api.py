# # -*- coding: utf-8 -*-
from django.db.models import Q

from drf_haystack.generics import HaystackGenericAPIView

from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin

from knowledge_base.api.v1.routers import router
from knowledge_base.core.api.mixins import cache as cache_mixins
from knowledge_base.core.api.viewsets import GenericViewSet
from knowledge_base.core.api.viewsets.nested import NestedViewset

from knowledge_base.posts import serializers
from knowledge_base.posts.models import Area, Post, Subject
from knowledge_base.posts.serializers import PostSearchSerializer


class AreaViewSet(
    cache_mixins.RetrieveCachedModelMixin,
    cache_mixins.ListCachedModelMixin,
    cache_mixins.BaseCacheMixin,
    GenericViewSet
):
    cache_class_group_key = "area"
    queryset = Area.objects.filter(is_active=True).order_by('name')

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
    cache_mixins.RetrieveCachedModelMixin,
    cache_mixins.ListCachedModelMixin,
    cache_mixins.BaseCacheMixin,
    NestedViewset
):

    cache_class_group_key = "subject"
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

        if self.parent_lookup_field in self.kwargs:
            queryset = queryset.filter(
                area=self.kwargs[self.parent_lookup_field]
            )

        return queryset.order_by('name')

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
    cache_mixins.RetrieveCachedModelMixin,
    cache_mixins.ListCachedModelMixin,
    cache_mixins.BaseCacheMixin,
    NestedViewset
):

    cache_class_group_key = "post"
    cache_unique_by_user = True
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
        queryset = Post.objects.all()

        if self.parent_lookup_field in self.kwargs:
            return queryset.filter(
                Q(subject=self.kwargs[self.parent_lookup_field]) &
                (
                    #
                    # If the post is active
                    #
                    Q(is_active=True) |
                    (
                        #
                        # Or if is inactive but the request user is the author.
                        #
                        Q(is_active=False) &
                        Q(author=self.request.user)
                    ) |
                    (
                        #
                        # Or if is inactive but the request user has edit
                        # permissions.
                        #
                        Q(is_active=False) &
                        Q(editable_to=self.request.user)
                    )
                ) &
                (
                    #
                    # If available to users are defined, and the request user
                    # was included.
                    #
                    (
                        Q(available_to__isnull=False) &
                        Q(available_to=self.request.user)
                    ) |
                    #
                    # Or if available user wasn't defined.
                    #
                    Q(available_to__isnull=True)
                )
            ).distinct().order_by('name')

        return queryset.none()

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


class PostSearchViewSet(ListModelMixin, ViewSetMixin, HaystackGenericAPIView):
    index_models = [Post]
    serializer_class = PostSearchSerializer

    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, index_models=[]):
        queryset = super(PostSearchViewSet, self).get_queryset()

        queryset = queryset.filter(
            (
                #
                # If the post is active
                #
                Q(is_active=True) |
                (
                    #
                    # Or if is inactive but the request user is the author.
                    #
                    Q(is_active=False) &
                    Q(author_id=self.request.user.id)
                ) |
                (
                    #
                    # Or if is inactive but the request user has edit
                    # permissions.
                    #
                    Q(is_active=False) &
                    Q(editable_to=self.request.user.id)
                )
            ) &
            (
                #
                # If available to users are defined, and the request user was
                # included.
                #
                (
                    Q(is_available_to=True) &
                    Q(available_to=self.request.user.id)
                ) |
                #
                # Or if available user wasn't defined.
                #
                Q(is_available_to=False)
            )
        ).order_by(
            'area_name',
            'subject_name',
            'name'
        )

        return queryset

    def list(self, request):
        """
        List all matching posts.
        ---
        response_serializer: PostSearchSerializer
        parameters:
            - name: q
              description: search into text field of the post.
              paramType: query
              type: integer

        responseMessages:
            - code: 200
              message: OK
            - code: 403
              message: FORBIDDEN
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application / querystring
        produces:
            - application / json
        """
        return super(PostSearchViewSet, self).list(request)


class ProfilePostViewSet(
    cache_mixins.RetrieveCachedModelMixin,
    cache_mixins.ListCachedModelMixin,
    cache_mixins.CreateCachedModelMixin,
    cache_mixins.PartialUpdateCachedModelMixin,
    cache_mixins.DestroyCachedModelMixin,
    cache_mixins.BaseCacheMixin,
    GenericViewSet
):
    cache_class_group_key = "profile-posts"
    cache_unique_by_user = True
    permission_classes = [IsAuthenticated, ]

    serializers_class = serializers.PostSerializer
    list_serializer_class = serializers.PostURISerializer
    retrieve_serializer_class = serializers.PostSerializer
    update_serializer_class = serializers.PostCreateSerializer
    create_serializer_class = serializers.PostCreateSerializer

    def get_queryset(self, *args, **kwargs):
        #
        # This set of endpoints are used only to manage the posts of the
        # request user or those where he has permissions to edit, so only
        # those post should be visible in all cases.
        #
        request_user = self.request.user
        queryset = Post.objects.filter(
            Q(author=request_user) |
            Q(editable_to=request_user)
        ).distinct().order_by(
            'subject__area',
            'subject',
            'name',
        )

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

router.register(
    r'posts/search',
    PostSearchViewSet,
    base_name="post-search"
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
