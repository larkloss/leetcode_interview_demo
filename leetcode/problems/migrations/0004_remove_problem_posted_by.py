# Generated by Django 3.0.3 on 2020-02-19 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_mock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='posted_by',
        ),
    ]