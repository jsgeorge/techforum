# Generated by Django 4.0.4 on 2022-05-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
