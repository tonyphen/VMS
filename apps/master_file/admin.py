from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.master_file import models
from apps.master_file import resources

admin.site.register(models.ProfileMaster)
admin.site.register(models.Profile)
admin.site.register(models.WoodType)
admin.site.register(models.SortGroup)
admin.site.register(models.Length)
