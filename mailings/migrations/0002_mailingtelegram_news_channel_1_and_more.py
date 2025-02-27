# Generated by Django 4.2.14 on 2024-10-10 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_newschannel_tag'),
        ('mailings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingtelegram',
            name='news_channel_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='news.newschannel'),
        ),
        migrations.AddField(
            model_name='mailingtelegram',
            name='news_channel_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='news.newschannel'),
        ),
        migrations.AddField(
            model_name='mailingtelegram',
            name='news_channel_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='news.newschannel'),
        ),
        migrations.AddField(
            model_name='mailingtelegram',
            name='news_channel_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='news.newschannel'),
        ),
        migrations.AddField(
            model_name='mailingtelegram',
            name='news_channel_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='news.newschannel'),
        ),
    ]
