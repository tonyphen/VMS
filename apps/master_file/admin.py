from django.contrib import admin

from apps.master_file import models

admin.site.register(models.ProfileMaster)
admin.site.register(models.Profile)
admin.site.register(models.WoodType)
admin.site.register(models.Color)
admin.site.register(models.SortGroup)
admin.site.register(models.Length)
admin.site.register(models.Thick)
admin.site.register(models.LogScale)
admin.site.register(models.Country)
admin.site.register(models.Warehouse)
admin.site.register(models.Unit)
admin.site.register(models.UnitConversion)
admin.site.register(models.Category)
admin.site.register(models.Product)
