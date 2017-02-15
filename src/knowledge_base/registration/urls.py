# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic.base import TemplateView

from knowledge_base.registration.views import ActivateView

urlpatterns = [
    url(
        r'^activate/(?P<token>[^/]+)$',
        ActivateView.as_view(),
        name='activate'
    ),
    url(
        r'^welcome$',
        TemplateView.as_view(template_name='users/welcome.html'),
        name='welcome'
    ),
]
