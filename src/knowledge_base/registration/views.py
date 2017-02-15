# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View

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
