from decimal import Decimal, getcontext
from django.utils.text import slugify
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


class Color(models.Model):
    color_group = models.CharField(max_length=50, choices=dictionary.COLOR_GROUP, verbose_name='Color Group')
    color_id = models.CharField(max_length=4, verbose_name='Code')
    description = models.CharField(max_length=100, verbose_name='Description')
    sort_group = models.ForeignKey(SortGroup, related_name='colors', on_delete=models.PROTECT, verbose_name='Sort Group', blank=True, null=True)
    sort_group_note = models.CharField(max_length=100, verbose_name='Sort Group Note', blank=True, null=True)
    wood_type = models.ForeignKey(WoodType, related_name='colors', on_delete=models.PROTECT, verbose_name='Wood Type', blank=True, null=True)
    gloss = models.CharField(max_length=20, verbose_name='Gloss', blank=True, null=True)
    printed = models.BooleanField(verbose_name='Printed', default=False)
    distressed = models.BooleanField(verbose_name='Distressed', default=False)
    distressed_remark = models.CharField(max_length=100, verbose_name='Distressed remark', blank=True, null=True)
    phun_hot = models.BooleanField(verbose_name='Phun hột', default=False)
    emboss = models.BooleanField(verbose_name='Emboss', default=False)
    scratch = models.BooleanField(verbose_name='Scratch', default=False)
    glazed = models.BooleanField(verbose_name='Glazed', default=False)
    danh_bui = models.BooleanField(verbose_name='Đánh bụi', default=False)
    remark = models.CharField(max_length=250, verbose_name='Remark')
    created_by = models.ForeignKey(User, related_name='color_creator', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(User, related_name='color_updater', on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.color_id + '-' + self.description


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

    class Meta:
        ordering = ('sym',)
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.sym

    def save(self, *args, **kwargs):
        self.sym = self.sym.upper()
        return super(Country, self).save(*args, **kwargs)

# Product Master Data


class Warehouse(models.Model):
    type = models.CharField(max_length=20, choices=dictionary.MATERIAL_TYPE, verbose_name='Type')
    id = models.SlugField(max_length=50, primary_key=True, verbose_name='Code')
    description = models.CharField(max_length=200, verbose_name='Description')
    credit_acc = models.IntegerField(verbose_name='credit code', blank=True, null=True)
    debit_acc = models.IntegerField(verbose_name='debit code', blank=True, null=True)

    class Meta:
        ordering = ('type', 'id')

    # def save(self,*args, **kwargs):
    #     self.id = slugify(str(self.id).upper())
    #     super(Warehouse, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class Unit(models.Model):
    unit = models.CharField(max_length=20, primary_key=True, verbose_name='Unit')

    def __str__(self):
        return self.unit


class UnitConversion(models.Model):
    f_unit = models.ForeignKey(Unit, related_name='f_unit', on_delete=models.CASCADE, verbose_name='From unit')
    t_unit = models.ForeignKey(Unit, related_name='t_unit', on_delete=models.CASCADE, verbose_name='To unit')
    ratio = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Ratio')


class Category(models.Model):
    id = models.SlugField(max_length=100, primary_key=True, verbose_name='Category')
    code = models.CharField(max_length=3, verbose_name='Code')
    is_root = models.BooleanField(default=False, verbose_name='Is root Catergory')
    parent = models.ForeignKey('self', related_name='child', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Parent Category')
    description = models.CharField(max_length=250, verbose_name='Description', blank=True, null=True)
    useSequence = models.BooleanField(default=True)

    class Meta:
        ordering = ('parent_id', 'id',)
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.id

    def get_main_parent_id(self):
        main_category = ''
        current_category = self.id
        if self.parent_id is None or self.is_root:
            return self.id
        else:
            while current_category.parent is not None:
                main_category = current_category.parent
            return main_category

    def get_parent_description(self):
        return Category.objects.values('description').get(id=self.parent_id)

    def get_full_parent_code(self):
        if not self.parent:
            return ''
        parent_link = ''
        is_top = False
        categories = []
        current_category = self.id
        while current_category is not None:
            categories.append(current_category)
            current_category = current_category.parent
        # '-'.join(map(str, categories))
        # '-'.join([str(elem) for elem in categories])
        return '-'.join(map(str, categories))


class Product(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='products', verbose_name='Warehouse', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT, verbose_name='Category')
    code = models.CharField(max_length=50, primary_key=True, verbose_name='Code')
    description = models.CharField(max_length=250, verbose_name='Description')
    profile = models.ForeignKey(Profile, related_name='product_profile', blank=True, null=True, on_delete=models.PROTECT)
    wood_type = models.ForeignKey(WoodType, related_name='product_woodtype', blank=True, null=True, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='products', on_delete=models.PROTECT, verbose_name='Color', blank=True, null=True)
    sort_group = models.ForeignKey(SortGroup, related_name='products', verbose_name='Sort Group', on_delete=models.PROTECT, blank=True, null=True)
    unit = models.ForeignKey(Unit, related_name='product_unit', verbose_name='Unit', on_delete=models.PROTECT)
    min_qty = models.IntegerField(default=0)
    max_qty = models.IntegerField(default=0)

    created_by = models.ForeignKey(User, related_name='product_creator', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='product_updater', on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.code)

