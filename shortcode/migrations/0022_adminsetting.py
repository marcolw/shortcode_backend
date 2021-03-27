# Generated by Django 3.0.2 on 2020-02-12 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcode', '0021_auto_20200211_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_url', models.CharField(max_length=511, verbose_name='Import Url')),
                ('export_method', models.IntegerField(choices=[(0, 'File'), (1, 'Url')], default=0, verbose_name='Export Method')),
                ('export_path', models.CharField(max_length=511, verbose_name='Export File Path')),
                ('export_url', models.CharField(max_length=511, verbose_name='Export Url')),
            ],
        ),
    ]