# Generated by Django 4.2.14 on 2024-08-23 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_newspost_time_pipelined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postlanguage',
            name='spacy_model_name',
        ),
    ]
