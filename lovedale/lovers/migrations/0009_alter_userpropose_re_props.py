# Generated by Django 5.0.1 on 2024-02-12 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lovers', '0008_userpropose_re_props'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpropose',
            name='re_props',
            field=models.IntegerField(),
        ),
    ]
