# Generated by Django 3.1.7 on 2021-04-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUsers', '0002_auto_20210406_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]