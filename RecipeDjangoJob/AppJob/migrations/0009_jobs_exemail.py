# Generated by Django 3.1.7 on 2021-04-27 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppJob', '0008_auto_20210427_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='ExEmail',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
