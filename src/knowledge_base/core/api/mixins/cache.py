# -*- coding: utf-8 -*-
from django.core.cache import cache

from rest_framework.response import Response

from .base import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    PartialUpdateModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from ..exceptions import ImproperlyConfigured, MissingConfiguration
from ...cache.utils import (
    get_cache_expiration_time,
    get_from_cache,
    get_query_params_keys,
    save_to_cache
)


class CreateCachedModelMixin(CreateModelMixin):
    """
    Allow to create an instance, deleting list cache to include it.
    """
    def create(self, request, *args, **kwargs):
        response = super(CreateCachedModelMixin, self).create(
            request,
            *args,
            **kwargs
        )
        #
        # There is not way to remove selective cache, so all cache is cleared.
        #
        cache.clear()

        return response


class ListCachedModelMixin(ListModelMixin):
    """
    Returns a list of instances from cache if any, else if
    gets the information normally, but saves it on cache.
    """
    def list(
        self,
        request,
        response_serializer='list',
        queryset=None,
        *args,
        **kwargs
    ):
        cache_class_group_key = self.get_cache_class_group_key()
        method_prefix_key = 'list'
        identifier_key = 'many'
        query_params_keys = get_query_params_keys(request.query_params)

        cached_info = get_from_cache(
            group_key=cache_class_group_key,
            prefix_key=method_prefix_key,
            identifier_key=identifier_key + query_params_keys
        )

        if not cached_info:
            response = super(ListCachedModelMixin, self).list(
                request,
                response_serializer=response_serializer,
                queryset=queryset,
                *args,
                **kwargs
            )

            save_to_cache(
                group_key=cache_class_group_key,
                prefix_key=method_prefix_key,
                identifier_key=identifier_key + query_params_keys,
                info=response.data,
                timeout=get_cache_expiration_time()
            )
            return response

        return Response(cached_info)


class RetrieveCachedModelMixin(RetrieveModelMixin):
    """
    Returns an instance from cache if exists, else if
    gets the information normally, but saves it on cache.
    """
    def retrieve(
        self,
        request,
        pk=None,
        instance=None,
        response_serializer='retrieve',
        *args,
        **kwargs
    ):
        cache_class_group_key = self.get_cache_class_group_key()
        method_prefix_key = 'retrieve'
        identifier_key = self.kwargs['pk']
        query_params_keys = get_query_params_keys(request.query_params)

        cached_info = get_from_cache(
            group_key=cache_class_group_key,
            prefix_key=method_prefix_key,
            identifier_key=identifier_key + query_params_keys
        )

        if not cached_info:
            response = super(RetrieveCachedModelMixin, self).retrieve(
                request,
                pk=pk,
                instance=instance,
                response_serializer=response_serializer,
                *args,
                **kwargs
            )
            save_to_cache(
                group_key=cache_class_group_key,
                prefix_key=method_prefix_key,
                identifier_key=identifier_key + query_params_keys,
                info=response.data,
                timeout=get_cache_expiration_time()
            )
            return response

        return Response(cached_info)


class UpdateCachedModelMixin(UpdateModelMixin):
    """
    Updates an instance and saves it to cache, then clears cache.
    """
    def update(
        self,
        request,
        pk=None,
        instance=None,
        request_serializer='update',
        response_serializer='retrieve',
        *args,
        **kwargs
    ):
        cache_class_group_key = self.get_cache_class_group_key()
        method_prefix_key = 'retrieve'
        identifier_key = self.kwargs['pk']
        query_params_keys = get_query_params_keys(request.query_params)

        response = super(UpdateCachedModelMixin, self).update(
            request,
            pk=pk,
            instance=instance,
            request_serializer=request_serializer,
            response_serializer=response_serializer,
            *args,
            **kwargs
        )

        cache.clear()

        save_to_cache(
            group_key=cache_class_group_key,
            prefix_key=method_prefix_key,
            identifier_key=identifier_key + query_params_keys,
            info=response.data,
            timeout=get_cache_expiration_time()
        )

        return response


class PartialUpdateCachedModelMixin(PartialUpdateModelMixin):
    """
    Updates an instance and saves it to cache, then clears cache.
    """
    def partial_update(
        self,
        request,
        pk=None,
        instance=None,
        request_serializer='update',
        response_serializer='retrieve',
        *args,
        **kwargs
    ):
        cache_class_group_key = self.get_cache_class_group_key()
        method_prefix_key = 'retrieve'
        identifier_key = self.kwargs['pk']
        query_params_keys = get_query_params_keys(request.query_params)

        response = super(PartialUpdateCachedModelMixin, self).partial_update(
            request,
            pk=pk,
            instance=instance,
            request_serializer=request_serializer,
            response_serializer=response_serializer,
            *args,
            **kwargs
        )

        cache.clear()

        save_to_cache(
            group_key=cache_class_group_key,
            prefix_key=method_prefix_key,
            identifier_key=identifier_key + query_params_keys,
            info=response.data,
            timeout=get_cache_expiration_time()
        )

        return response


class DestroyCachedModelMixin(DestroyModelMixin):
    """
    Destroy an instance, and also clears cache.
    """
    def destroy(self, request, pk=None, instance=None, *args, **kwargs):
        response = super(DestroyCachedModelMixin, self).destroy(
            request, pk=None, instance=None, *args, **kwargs
        )
        cache.clear()

        return response


class BaseCacheMixin(object):
    """
    Base class of cache functionality.
    """
    cache_class_group_key = None

    def get_cache_class_group_key(self):
        cache_class_group_key = self.cache_class_group_key

        if cache_class_group_key is None:
            raise MissingConfiguration("cache_class_group_key")

        if not isinstance(cache_class_group_key, str):
            raise ImproperlyConfigured("cache_class_group_key")

        return cache_class_group_key
