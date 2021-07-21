from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.hr.models import Department, HealthCheck, HealthCheckItem


admin.site.register(Department)
admin.site.register(HealthCheck)
admin.site.register(HealthCheckItem)


class HealthCheckItemAdmin(ImportExportModelAdmin):
    list_display = ('id', 'stt', 'ho_ten', 'msnv', 'ngay_sinh', 'gioi_tinh', 'so_bhyt', 'cmnd', 'cong_ty', 'dia_chi',
                    'so_dt', 'ngay_kham', 'gio_kham', 'gio_ketthuc', 'status', 'completed')
