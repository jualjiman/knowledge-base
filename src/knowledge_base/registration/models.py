# -*- coding: utf-8 -*-
import random

from datetime import timedelta
from hashlib import sha1

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from knowledge_base.core.db.models import TimeStampedMixin
from knowledge_base.users.models import User


class ActivationKeysManager(models.Manager):

    def reset_user_password(self, email, request=None):
        """
        Custom reset password
        """
        user = User.objects.get(
            email=email
        )
        # Create activation_key
        salt = sha1(str(random.random())).hexdigest()[:5]
        key = sha1(salt + user.username).hexdigest()
        ResetPassword.objects.create(
            user=user, activation_key=key
        )

        return user


class ResetPassword(TimeStampedMixin):
    """
    Mapping table reset password for users.
    """
    user = models.ForeignKey(
        User,
        related_name='reset_password'
    )
    activation_key = models.CharField(
        max_length=40,
        unique=True,
        verbose_name=_('activation key')
    )
    is_activated = models.BooleanField(
        default=False,
        verbose_name=_('is activated')
    )

    objects = ActivationKeysManager()

    class Meta:
        verbose_name = _('Reset Password')
        verbose_name_plural = _('Reset Passwords')

    @property
    def key_expired(self):
        """
        Tells wheter the activation key of the current profile is expired.
        The key is expired if the user was already activated or the current
        date is greater than the user's date that the user was joined plus
        the validity minutes of the key.
        Returns a boolean.
        """
        if not self.is_activated:
            return (True if (now() - self.created_date) >
                    timedelta(minutes=15) else False)

        return True
