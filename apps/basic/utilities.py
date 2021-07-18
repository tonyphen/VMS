from django.db import models


def created_updated(model, request):
    obj = model.objects.latest('pk')
    if obj.created_by is None:
        obj.created_by = request.user
    obj.updated_by = request.user
    obj.save()