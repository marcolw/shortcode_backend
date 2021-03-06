# Generated by Django 3.0.2 on 2020-01-19 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcode', '0002_columnprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('description', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
