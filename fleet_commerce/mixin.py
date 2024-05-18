from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from utils.managers import IsDeletedManager

CONTENT_TYPE_JSON = "application/json; charset=utf-8"


class BaseApiMixin(object):
    def error_response(self, message="", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {"response": message, "errors": errors},
            status=status_code,
            content_type=CONTENT_TYPE_JSON,
        )

    def forbidden_response(
        self, message="Access denied", errors=None, status_code=status.HTTP_403_FORBIDDEN
    ):
        return Response(
            {"message": message, "errors": errors},
            status=status_code,
            content_type=CONTENT_TYPE_JSON,
        )

    def successful_post_response(self, message="", status_code=status.HTTP_201_CREATED):
        return Response(message, status=status_code, content_type=CONTENT_TYPE_JSON)

    def successful_response(self, message="", status_code=status.HTTP_200_OK):
        return Response({"message": message}, status=status_code, content_type=CONTENT_TYPE_JSON)

    def not_found_response(self, message="Not found", status_code=status.HTTP_404_NOT_FOUND):
        return Response({"message": message}, status=status_code, content_type=CONTENT_TYPE_JSON)

    def successful_get_response(self, message="", status_code=status.HTTP_200_OK):
        return Response(message, status=status_code, content_type=CONTENT_TYPE_JSON)


class IsDeletedMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = IsDeletedManager()

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = IsDeletedManager()  # Default manager

    class Meta:
        abstract = True


class AuthorTimeStampedModel(TimeStampedModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="+",
    )

    class Meta:
        abstract = True


class OrganisationTimeStampedModel(AuthorTimeStampedModel):
    organisation = models.ForeignKey(
        "accounts.Organisation",
        verbose_name=_("Organisation"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="+",
    )

    class Meta:
        abstract = True
