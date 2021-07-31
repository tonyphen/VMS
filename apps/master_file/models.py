from decimal import Decimal, getcontext

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from apps.basic import dictionary

mm_ft = 304.8
cm_inch = 0.39370079


class ProfileMaster(models.Model):
    group_id = models.CharField(max_length=10,  primary_key=True, verbose_name='Group ID')
    group_name = models.CharField(max_length=200, verbose_name='Group Name')
    sales_target = models.IntegerField(default=0, verbose_name='Sales Target')
    created_by = models.ForeignKey(User, related_name='profile_master_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='profile_master_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.group_name

    def get_update_url(self):
        return reverse("profile_master_update", args=(self.pk,))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.group_id = self.group_id.upper()
        return super(ProfileMaster, self).save(force_insert, force_update, *args, **kwargs)


class Profile(models.Model):
    group_master = models.ForeignKey(ProfileMaster, related_name='group_master', verbose_name='Gourp master', on_delete=models.DO_NOTHING)
    profile_group = models.CharField(max_length=100, verbose_name='Profile Group', blank=True, null=True)
    profile_group_description = models.CharField(max_length=200, verbose_name='Group description')
    profile_id = models.CharField(max_length=5, verbose_name='Profile ID', primary_key=True)
    profile_sym = models.CharField(max_length=50, verbose_name='Sym', blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name='Description')
    image = models.ImageField(upload_to='upload/images/master_file', blank=True, null=True, verbose_name='Image')
    width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Width(mm)', default=0.0)
    thick = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='Thick(mm)', default=0.0)
    CBM_Feet = models.DecimalField(max_digits=18, decimal_places=6, verbose_name='CBM/Feet', default=0)
    M2_Feet = models.DecimalField(max_digits=18, decimal_places=6, verbose_name='M2/Feet', default=0)
    bundle = models.IntegerField(verbose_name='Pcs/Bundle', default=0)
    created_by = models.ForeignKey(User, related_name='profile_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='profile_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.profile_sym

    def save(self, *args, **kwargs):
        self.profile_group = self.profile_group.upper()
        self.profile_id = self.profile_id.upper()
        self.profile_sym = self.profile_sym.upper()
        if self.width > 0 and self.thick > 0:
            getcontext().prec = 6
            self.CBM_Feet = Decimal(self.width) * Decimal(self.thick) * Decimal(mm_ft)*Decimal(10**-9)
            self.M2_Feet = Decimal(self.width) + Decimal(self.thick*2) * Decimal(mm_ft)*Decimal(10**-6)
        return super(Profile, self).save(*args, **kwargs)


class WoodType(models.Model):
    wood_type_id = models.CharField(max_length=3, primary_key=True, verbose_name='Wood type Id')
    sym = models.CharField(max_length=5, blank=True, null=True, verbose_name='Sym')
    description = models.CharField(max_length=200, verbose_name='Name')
    parent_id = models.CharField(max_length=3, blank=True, null=True, default='', verbose_name='Main group')
    freqUsed = models.BooleanField(default=True, blank=True, null=True)
    wood_group = models.CharField(max_length=50, choices=dictionary.WOOD_GROUP_CHOICE, blank=True, null=True, verbose_name='WG Type')
    prod_type = models.CharField(max_length=20, choices=dictionary.PROD_TYPE, blank=True, null=True, verbose_name='Prod Type')
    bod_view = models.BooleanField(default=False, blank=True, null=True, verbose_name='Shown')
    created_by = models.ForeignKey(User, related_name='wood_type_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='wood_type_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.sym = self.sym.upper()
        self.description = self.description.upper()
        return super(WoodType, self).save(*args, **kwargs)


class SortGroup(models.Model):
    id = models.CharField(max_length=3, primary_key=True, verbose_name='ID')
    description = models.CharField(max_length=200, verbose_name='Description')
    sym = models.CharField(max_length=20, blank=True, null=True, verbose_name='Sym')
    parent = models.CharField(max_length=50, blank=True, null=True, verbose_name='Parent')
    freqUse = models.BooleanField(blank=True, null=True,verbose_name='Freq Used')
    created_by = models.ForeignKey(User, related_name='sort_group_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='sort_group_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.sym = self.sym.upper()
        return super(SortGroup, self).save(*args, **kwargs)


class Length(models.Model):
    mm = models.IntegerField(primary_key=True, default=0, verbose_name='MM')
    feet = models.DecimalField(max_digits=8, decimal_places=4, verbose_name='Feet')
    inch = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Inch')
    freqUsed = models.BooleanField(blank=True, null=True, verbose_name='Freq. used')
    created_by = models.ForeignKey(User, related_name='length_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='length_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('mm',)

    def save(self, *args, **kwargs):
        self.inch = Decimal(self.feet)*12
        super(Length, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.mm)


class Thick(models.Model):
    mm = models.IntegerField(primary_key=True, verbose_name='MM')
    cm = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='CM')
    inch = models.CharField(max_length=20, verbose_name='Inch', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='thick_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='thick_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('mm',)

    def __str__(self):
        return str(self.mm)


class LogScale(models.Model):
    dia = models.DecimalField(max_digits=18,decimal_places=2, verbose_name='Diameter')
    length = models.DecimalField(max_digits=18,decimal_places=2, verbose_name='Length')
    BF = models.DecimalField(max_digits=18,decimal_places=2, verbose_name='Board FT')

    class Meta:
        ordering = ('dia', 'length',)

    def save(self, *args, **kwargs):
        self.BF = Decimal(self.length) * Decimal(self.dia - 4) * Decimal(self.dia - 4) / 16
        super(LogScale, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.dia)


class Country(models.Model):
    sym = models.CharField(max_length=3, primary_key=True, verbose_name='Country')
    name = models.CharField(max_length=50, verbose_name='Name')
    created_by = models.ForeignKey(User, related_name='country_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='country_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.sym

    def save(self, *args, **kwargs):
        self.sym = self.sym.upper()
        return super(Country, self).save(*args, **kwargs)

# Product Master Data


class Warehouse(models.Model):
    type = models.IntegerField(verbose_name='Type')
    id = models.CharField(max_length=50, primary_key=True, verbose_name='Code')
    description = models.CharField(max_length=200, verbose_name='Description')
    credit_acc = models.IntegerField(verbose_name='credit code', blank=True, null=True)
    debit_acc = models.IntegerField(verbose_name='debit code', blank=True, null=True)

    class Meta:
        ordering = ('type', 'id')

    def __str__(self):
        return self.name


class Unit(models.Model):
    unit = models.CharField(max_length=20, primary_key=True, verbose_name='Unit')


class UnitConversion(models.Model):
    f_unit = models.CharField(max_length=20, verbose_name='From unit')
    t_unit = models.CharField(max_length=20, verbose_name='To unit')
    ratio = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Ratio')


class Product(models.Model):
    warehouse_id = models.ForeignKey(Warehouse, related_name='product_warehouse', verbose_name='Warehouse', on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=50, primary_key=True, verbose_name='Code')
    description = models.CharField(max_length=250, verbose_name='Description')
    profile = models.ForeignKey(Profile, related_name='product_profile', blank=True, null=True, on_delete=models.DO_NOTHING)
    wood_type = models.ForeignKey(WoodType, related_name='product_woodtype', blank=True, null=True, on_delete=models.DO_NOTHING)
    unit = models.ForeignKey(Unit, related_name='product_unit', verbose_name='Unit', on_delete=models.DO_NOTHING)
    min_qty = models.IntegerField(default=0)
    max_qty = models.IntegerField(default=0)

    created_by = models.ForeignKey(User, related_name='product_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='product_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.description)
