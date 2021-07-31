import decimal
from django.db import models


# class UpperCaseCharField(models.CharField):
#
#     def __init__(self, *args, **kwargs):
#         super(UpperCaseCharField, self).__init__(*args, **kwargs)
#
#     def pre_save(self, model_instance, add):
#         value = getattr(model_instance, self.attname, None)
#         if value:
#             value = value.upper()
#             setattr(model_instance, self.attname, value)
#             return value
#         else:
#             return super(UpperCaseCharField, self).pre_save(model_instance, add)


def created_updated(form, request):
    if form.instance.created_by is None:
        form.instance.created_by = request.user
    form.instance.updated_by = request.user
    return


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
