# Generated by Django 4.0.3 on 2022-05-25 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_delete_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]