# Generated by Django 4.2.14 on 2024-09-25 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_postlanguage_spacy_model_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newschannel',
            name='tag',
            field=models.CharField(db_index=True, max_length=128),
        ),
    ]
