from django.db import models


mm_ft = 304.8


class ProfileMaster(models.Model):
    group_id = models.CharField(max_length=10, verbose_name='Group ID')
    group_name = models.CharField(max_length=200, verbose_name='Group Name')
    sales_target = models.IntegerField(default=0, verbose_name='Sales Target')


class Profile(models.Model):
    group_master = models.ForeignKey(ProfileMaster, related_name='group_master', on_delete=models.CASCADE)
    profile_id = models.CharField(max_length=5, verbose_name='Profile ID', primary_key=True)
    profile_sym = models.CharField(max_length=50, verbose_name='Sym', blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name='Description')
    image = models.ImageField(upload_to='upload/images/master_file',blank=True, null=True, verbose_name='Image')
    width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Width(mm)', default=0.0)
    thick = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='Thick(mm)',default=0.0)
    CBM_Feet = models.DecimalField(max_digits=18, decimal_places=9, default=0.0, verbose_name='CBM/Feet')
    M2_Feet = models.DecimalField(max_digits=18, decimal_places=9, default=0.0, verbose_name='M2/Feet')
    bundle = models.IntegerField(verbose_name='Pcs/Bundle', default=0)

    def save(self, *args, **kwargs):
        if self.width > 0 and self.thick > 0:
            self.CBM_Feet = (self.width * self.thick * mm_ft)/10**-9
            self.M2_Feet = (self.width * self.thick * mm_ft)/10**-6
        super(Profile, self).save(*args, **kwargs)

