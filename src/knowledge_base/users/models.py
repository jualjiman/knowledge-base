# -*- coding: utf-8 -*-
import os
from hashlib import md5

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.gis.db import models
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from knowledge_base.posts.models import Area, Subject


class UserManager(BaseUserManager):
    """
    Custom manager for create users staff and superuser.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Method for create new users.
        """
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            last_login=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creating new user staff.
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creating new user superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


def get_user_image_path(instance, filename):
    """
    Get the upload path to the profile image.
    """
    return '{0}/{1}{2}'.format(
        "users/originals",
        md5(filename).hexdigest(),
        os.path.splitext(filename)[-1]
    )


def get_user_thumbnail_path(instance, filename):
    """
    Get the proper upload path to the thumbnail profile image.
    """
    return '{0}/{1}'.format(
        "users/thumbnails",
        filename
    )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Mapping table user Tandlr.
    """
    email = models.EmailField(
        max_length=50,
        unique=True,
        null=False
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True
    )
    photo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_user_image_path
    )
    thumbnail = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_user_thumbnail_path
    )
    register_date = models.DateField(
        auto_now=True,
    )
    last_modify_date = models.DateField(
        auto_now_add=True
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is_active')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is_staff')
    )
    activation_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # User preferences.
    favorite_subjects = models.ManyToManyField(
        Subject,
        blank=True
    )
    area = models.ForeignKey(
        Area,
        related_name='users',
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Return full name user:
             name last_name
        """
        return u'{0} {1}'.format(
            self.name, self.last_name
        )

    def get_short_name(self):
        """
        Return short name user:
            name last_name
        """
        return self.name

    def send_email(self, subject, body, html=None, from_email=None, **kwargs):
        """
        Send an email to this user.
            Args:
                subject (str): The subject for the email message.
                body (str): Body for the email message. Must be plain txt.
                html (optional[str]): HTML formatted version of the body.
                    If provided, this version shall be appended to message as
                    an alternative. Defaults to None.
                from_email (optional[str]): Email address that shall be used
                    as the sender of the email message. If it is not provided,
                    then the message will be marked as sent from the address
                    specified in the ```DEFAULT_FROM_EMAIL``` setting.
                    Defaults to None.
                **kwargs: Arbitrary keyword arguments that shall be used to
                    instantiate the ```EmailMultiAlternatives``` class.
            Returns:
                bool: True if the message was successfully sent.
        """
        if not from_email and settings.DEFAULT_FROM_EMAIL:
            from_email = settings.DEFAULT_FROM_EMAIL


        message = EmailMultiAlternatives(
            subject,
            body,
            from_email,
            [self.email],
            **kwargs
        )

        if html is not None:
            message.attach_alternative(html, 'text/html')

        return message.send() > 0
