import decimal
from django.db import models
from import_export import resources

from apps.hr.models import HealthCheckItem


def created_updated(model, request):
    obj = model.objects.latest('pk')
    if obj.created_by is None:
        obj.created_by = request.user
    obj.updated_by = request.user
    obj.save()

def format_number(value, max_digits, decimal_places):
    """
    Formats a number into a string with the requisite number of digits and
    decimal places.
    """
    if value is None:
        return None
    if isinstance(value, decimal.Decimal):
        context = decimal.getcontext().copy()
        if max_digits is not None:
            context.prec = max_digits
        if decimal_places is not None:
            value = value.quantize(decimal.Decimal(".1") ** decimal_places, context=context)
        else:
            context.traps[decimal.Rounded] = 1
            value = context.create_decimal(value)
        return "{:f}".format(value)
    if decimal_places is not None:
        return "%.*f" % (decimal_places, value)
    return "{:f}".format(value)
