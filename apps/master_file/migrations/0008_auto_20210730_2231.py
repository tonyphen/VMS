# Generated by Django 3.2.5 on 2021-07-30 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master_file', '0007_product_warehouse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='profile_id',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='wood_type_id',
            new_name='wood_type',
        ),
    ]