# Generated by Django 3.0.8 on 2020-07-17 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(default= 1, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(default= 1, on_delete=django.db.models.deletion.CASCADE, related_name='created_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
