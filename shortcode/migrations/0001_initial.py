# Generated by Django 3.0.2 on 2020-01-16 17:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63, verbose_name='Field Name')),
                ('max_length', models.IntegerField(default=255, verbose_name='Field Max Length')),
                ('field_type', models.IntegerField(choices=[(0, 'Data'), (1, 'Shortcode'), (2, 'Result')])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sku', models.CharField(max_length=31, primary_key=True, serialize=False, unique=True, verbose_name='SKU')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Product Data')),
            ],
        ),
        migrations.CreateModel(
            name='Shortcode',
            fields=[
                ('sku', models.CharField(max_length=31, primary_key=True, serialize=False, unique=True, verbose_name='SKU')),
                ('value', models.TextField(verbose_name='Field Value')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortcode.Field', verbose_name='Field')),
            ],
        ),
    ]
