# -*- coding: utf-8 -*-
from . import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    PartialUpdateModelMixin, RetrieveModelMixin, UpdateModelMixin
)


class CreateCachedModelMixin(CreateModelMixin):
    pass


class ListCachedModelMixin(ListModelMixin):
    pass


class RetrieveCachedModelMixin(RetrieveModelMixin):
    pass


class UpdateCachedModelMixin(UpdateModelMixin):
    pass


class PartialUpdateCachedModelMixin(PartialUpdateModelMixin):
    pass


class DestroyCachedModelMixin(DestroyModelMixin):
    pass
