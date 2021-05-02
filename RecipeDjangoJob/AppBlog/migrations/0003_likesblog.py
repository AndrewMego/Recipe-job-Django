# Generated by Django 3.1.7 on 2021-05-01 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppUsers', '0006_users_skills'),
        ('AppBlog', '0002_auto_20210423_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='likesBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blogID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppBlog.blog')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppUsers.users')),
            ],
            options={
                'unique_together': {('userID', 'blogID')},
            },
        ),
    ]
