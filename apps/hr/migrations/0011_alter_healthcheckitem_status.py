# Generated by Django 3.2.5 on 2021-07-22 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0010_merge_0009_auto_20210720_1613_0009_auto_20210720_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthcheckitem',
            name='status',
            field=models.CharField(blank=True, choices=[('Chưa tiêm', 'Chưa tiêm'), ('Đã tiêm', 'Đã tiêm'), ('Hoãn tiêm', 'Hoãn tiêm'), ('Không được tiêm', 'Không được tiêm')], max_length=50, null=True, verbose_name='Tình trạng'),
        ),
    ]