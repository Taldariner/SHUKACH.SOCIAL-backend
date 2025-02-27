# Generated by Django 4.2.14 on 2024-10-30 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_newschannel_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postentity',
            name='display_name',
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='postentity',
            name='lemmatized_name',
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='posthashtag',
            name='name',
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='postkeyword',
            name='name',
            field=models.CharField(db_index=True, max_length=128),
        ),
    ]
