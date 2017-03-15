# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView, View

from knowledge_base.users.models import User


class ActivateView(View):
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        user = get_object_or_404(
            User, activation_code=token, is_active=False
        )
        user.is_active = True
        user.save()

        return redirect('registration:welcome')


class WelcomeView(TemplateView):
    template_name = 'users/welcome.html'

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)

        url_schema = self.request.META['wsgi.url_scheme']

        current_site = Site.objects.get_current()
        context['url'] = '{0}://{1}/'.format(
            url_schema,
            current_site.domain,
        )

        return context
