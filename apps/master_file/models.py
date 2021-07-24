from decimal import Decimal
from django.db import models

mm_ft = 304.8
cm_inch = 0.39370079


class ProfileMaster(models.Model):
    group_id = models.CharField(max_length=10, verbose_name='Group ID')
    group_name = models.CharField(max_length=200, verbose_name='Group Name')
    sales_target = models.IntegerField(default=0, verbose_name='Sales Target')

    def __str__(self):
        return self.group_name


class Profile(models.Model):
    group_master = models.ForeignKey(ProfileMaster, related_name='group_master', on_delete=models.CASCADE)
    profile_group = models.CharField(max_length=100, verbose_name='Profile Group', blank=True, null=True)
    profile_id = models.CharField(max_length=5, verbose_name='Profile ID', primary_key=True)
    profile_sym = models.CharField(max_length=50, verbose_name='Sym', blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name='Description')
    image = models.ImageField(upload_to='upload/images/master_file',blank=True, null=True, verbose_name='Image')
    width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Width(mm)', default=0.0)
    thick = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='Thick(mm)',default=0.0)
    CBM_Feet = models.DecimalField(max_digits=18, decimal_places=9, default=0.0, verbose_name='CBM/Feet')
    M2_Feet = models.DecimalField(max_digits=18, decimal_places=9, default=0.0, verbose_name='M2/Feet')
    bundle = models.IntegerField(verbose_name='Pcs/Bundle', default=0)

    def __str__(self):
        return self.profile_sym

    def save(self, *args, **kwargs):
        if self.width > 0 and self.thick > 0:
            self.CBM_Feet = (self.width * self.thick * mm_ft)/10**-9
            self.M2_Feet = (self.width * self.thick * mm_ft)/10**-6
        super(Profile, self).save(*args, **kwargs)


CHOICES_WG = (
    ("Main", "Main"),
    ("Secondary", "Secondary"),
)
CHOICES_TYPE = (
    ("Solid", "Solid"),
    ("F/J", "F/J"),
    ("F/J Edg", "F/J Edg"),
)


class WoodType(models.Model):
    wood_type_id = models.CharField(max_length=3, primary_key=True, verbose_name='Wood type Id')
    sym = models.CharField(max_length=5, blank=True, null=True, verbose_name='Sym')
    description = models.CharField(max_length=200, verbose_name='Name')
    parent_id = models.CharField(max_length=3, blank=True, null=True, default='', verbose_name='Main group')
    freqUse = models.BooleanField(default=True, blank=True, null=True)
    wood_group = models.CharField(max_length=20, choices=CHOICES_WG, blank=True, null=True, verbose_name='WG Type')
    type = models.CharField(max_length=10, choices=CHOICES_TYPE, blank=True, null=True, verbose_name='Prod Type')
    bod_view = models.BooleanField(default=False, blank=True, null=True, verbose_name='Shown')

    def __str__(self):
        return self.description


class SortGroup(models.Model):
    id = models.CharField(max_length=3, primary_key=True, verbose_name='ID')
    description = models.CharField(max_length=200, verbose_name='Description')
    sym = models.CharField(max_length=5, blank=True, null=True, verbose_name='Sym')
    parent = models.CharField(max_length=5, blank=True, null=True, verbose_name='Parent')
    freqUse = models.BooleanField(blank=True, null=True,verbose_name='Freq Used')

    def __str__(self):
        return self.description


class Length(models.Model):
    feet = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='Feet')
    inch = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Inch')
    mm = models.IntegerField(default=0,  blank=True, null=True, verbose_name='MM')
    freqUsed = models.BooleanField(default=False,  blank=True, null=True, verbose_name='Freq. used')

    def save(self, *args, **kwargs):
        self.inch = self.feet*12
        self.mm = self.feet*mm_ft
        super(Length, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.mm)


class Thick(models.Model):
    thick = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='Thickness CM')
    mm = models.DecimalField(max_digits=5,decimal_places=2, verbose_name='MM')
    inch = models.CharField(max_length=20, verbose_name='Inch')

    def save(self, *args, **kwargs):
        self.mm = self.thick*10
        self.inch = Decimal(self.thick*cm_inch)
        super(Thick, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.thick)

