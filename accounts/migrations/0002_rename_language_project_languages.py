# Generated by Django 4.2.14 on 2024-08-17 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='language',
            new_name='languages',
        ),
    ]
