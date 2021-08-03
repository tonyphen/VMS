# Generated by Django 3.2.5 on 2021-08-03 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_file', '0022_auto_20210731_2032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('parent_id', 'id'), 'verbose_name_plural': 'Category'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='category',
            name='level',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent_id',
        ),
        migrations.RemoveField(
            model_name='category',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='category',
            name='is_root',
            field=models.BooleanField(default=False, verbose_name='Is root Catergory'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='master_file.category', verbose_name='Parent Category'),
        ),
    ]