# Generated by Django 3.0.2 on 2020-01-22 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shortcode', '0006_auto_20200121_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=63, verbose_name='Column Profile Description')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.RemoveField(
            model_name='field',
            name='order',
        ),
        migrations.RemoveField(
            model_name='field',
            name='visible',
        ),
        migrations.CreateModel(
            name='ColumnProfileField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=10000, verbose_name='Field Order')),
                ('visible', models.BooleanField(default=True, verbose_name='Field Visible?')),
                ('column_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortcode.ColumnProfile', verbose_name='Column Profile')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortcode.Field', verbose_name='Corresponding Field')),
            ],
        ),
    ]
