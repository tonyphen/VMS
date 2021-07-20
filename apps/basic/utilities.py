from django.db import models
from import_export import resources

from apps.hr.models import HealthCheckItem


def created_updated(model, request):
    obj = model.objects.latest('pk')
    if obj.created_by is None:
        obj.created_by = request.user
    obj.updated_by = request.user
    obj.save()


class HealthCheckItemResource(resources.ModelResource):
    class Meta:
        model = HealthCheckItem
