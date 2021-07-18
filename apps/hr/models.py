from django.contrib.auth.models import User
from django.db import models

HC_STATUS = (
    ("Đã tiêm", "Đã tiêm"),
    ("Hoãn tiêm", "Hoãn tiêm"),
    ("Không được tiêm", "Không được tiêm"),
)

GENDER_OPTIONS = (
    ('Nam', 'Nam'),
    ('Nữ', 'Nữ')
)

CTY_OPTIONS = (
    ('VINAWOOD', 'VINAWOOD'),
    ('Other', 'Other'),
)


class Department(models.Model):
    ma_bp = models.CharField(max_length=30)
    ten_bp = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Department'

    def __str__(self):
        return str(self.ten_bp)


class HealthCheck(models.Model):
    name = models.CharField(max_length=250, verbose_name="Đợt khám")
    ngay = models.DateField(verbose_name="Ngày")
    noi_dung = models.TextField(verbose_name="Nội dung")
    hc_image = models.ImageField(upload_to="assets/images/", default="", null=True, blank=True)
    attachment = models.FileField(blank=True, null=True, verbose_name="Tài liệu đính kèm")
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='create')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='update')

    class Meta:
        verbose_name = 'Health Check'
        verbose_name_plural = 'Health Check'

    def __str__(self):
        return str(self.name)


class HealthCheckItem(models.Model):
    hc = models.ForeignKey(HealthCheck, related_name='items', on_delete=models.CASCADE)
    stt = models.IntegerField(verbose_name="STT")
    ho_ten = models.CharField(max_length=200, verbose_name="Họ Tên")
    msnv = models.IntegerField(blank=True, null=True, verbose_name="MSNV")
    ngay_sinh = models.DateField(verbose_name="Ngày sinh", blank=True, null=True)
    gioi_tinh = models.CharField(max_length=20, choices=GENDER_OPTIONS, null=True, verbose_name="Giới tính")
    so_bhyt = models.CharField(max_length=30, default="", null=True, verbose_name="Số BHYT")
    cmnd = models.CharField(max_length=30, blank=True, null=True, verbose_name="Số CMND")
    cong_ty = models.CharField(max_length=100, choices=CTY_OPTIONS, verbose_name="Công ty", default='')
    dia_chi = models.CharField(max_length=250, blank=True, null=True, default="", verbose_name="Địa chỉ")
    so_dt = models.CharField(max_length=30, blank=True, null=True, default="", verbose_name="Số điện thoại")
    ngay_kham = models.DateField(verbose_name="Ngày khám", blank=True, null=True)
    gio_kham = models.TimeField(blank=True, null=True, verbose_name="Giờ khám")
    gio_ketthuc = models.TimeField(blank=True, null=True, verbose_name="Giờ kết thúc")
    status = models.CharField(max_length=50, choices=HC_STATUS, blank=True, null=True, verbose_name="Tình trạng")
    completed = models.BooleanField(default=False, blank=True, null=True, verbose_name="Hoàn tất")

    class Meta:
        verbose_name = 'Health Check Detail'
        verbose_name_plural = 'Health Check Detail'

    def __str__(self):
        return str(self.ho_ten)
