from import_export import resources, widgets, fields
from apps.master_file import models


class LengthResource(resources.ModelResource):
    freqUsed = fields.Field(widget=widgets.BooleanWidget())

    class Meta:
        model = models.Length
        fields = ('id','feet', 'inch', 'mm', 'freqUsed',)
        widgets = {
            'freqUsed': widgets.BooleanWidget()
        }

    def before_row_import(self, row, **kwargs):
        if "freqUsed" in row.keys():
            if row["freqUsed"] in ["True", "TRUE"]:
                row["freqUsed"] = True
            else:
                row["freqUsed"] = False

        return super().before_import_row(row, **kwargs)
