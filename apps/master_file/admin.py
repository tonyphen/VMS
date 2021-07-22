from django.contrib import admin

from apps.master_file import models


admin.site.register(models.ProfileMaster)
admin.site.register(models.Profile)
