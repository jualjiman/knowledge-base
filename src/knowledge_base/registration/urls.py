# -*- coding: utf-8 -*-
from django.conf.urls import url

from knowledge_base.registration.views import ActivateView, WelcomeView

urlpatterns = [
    url(
        r'^activate/(?P<token>[^/]+)$',
        ActivateView.as_view(),
        name='activate'
    ),
    url(
        r'^welcome$',
        WelcomeView.as_view(),
        name='welcome'
    ),
]
