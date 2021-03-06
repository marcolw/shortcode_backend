# Generated by Django 3.0.2 on 2020-01-21 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcode', '0004_field_label'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ColumnProfile',
        ),
        migrations.AddField(
            model_name='field',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Field Order Number'),
        ),
        migrations.AddField(
            model_name='field',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Field Visible'),
        ),
    ]
