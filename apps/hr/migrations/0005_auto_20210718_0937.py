# Generated by Django 3.2.5 on 2021-07-18 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_auto_20210717_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcheckitem',
            name='dan_toc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='healthcheckitem',
            name='job',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='healthcheckitem',
            name='quoc_tich',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]