# Generated by Django 3.1.7 on 2021-04-18 19:58

import AppUsers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUsers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to=AppUsers.models.upload_path),
        ),
    ]