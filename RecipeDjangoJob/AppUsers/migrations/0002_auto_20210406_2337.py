# Generated by Django 3.1.7 on 2021-04-06 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppUsers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='customUser',
            new_name='customUserID',
        ),
    ]