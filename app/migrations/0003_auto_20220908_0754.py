# Generated by Django 2.2.8 on 2022-09-08 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220905_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionmodelform',
            name='deadline',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='auctionmodelform',
            name='id',
            field=models.IntegerField(blank=True, default=0, primary_key=True, serialize=False),
        ),
    ]
