# Generated by Django 5.0.1 on 2024-02-10 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lovers', '0005_alter_userpropose_accepte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpropose',
            name='count',
        ),
    ]