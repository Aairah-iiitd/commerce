# Generated by Django 3.0.8 on 2020-07-17 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200717_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bidder',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='creator',
        ),
    ]
