# Generated by Django 3.1.7 on 2021-04-25 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppJob', '0004_auto_20210425_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplaycer',
            name='uploadCer',
            field=models.FileField(blank=True, null=True, upload_to='files/certificate/'),
        ),
        migrations.AlterUniqueTogether(
            name='aplaycer',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='aplaycer',
            name='cerID',
        ),
        migrations.DeleteModel(
            name='certificate',
        ),
    ]