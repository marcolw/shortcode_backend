# Generated by Django 3.0.2 on 2020-01-21 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcode', '0003_productfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='label',
            field=models.CharField(default=None, max_length=63, verbose_name='Field Label'),
            preserve_default=False,
        ),
    ]