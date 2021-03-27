# Generated by Django 3.0.2 on 2020-02-03 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortcode.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shortcode', '0018_auto_20200202_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_dropdown', shortcode.models.ColorField(default='#ffffff', max_length=10)),
                ('color_background', shortcode.models.ColorField(default='#ffffff', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]