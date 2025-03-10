# Generated by Django 5.1.2 on 2024-11-07 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_city_profile_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='average_rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='emergency_alerts_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='reviews_given',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_donations',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_reservations',
            field=models.IntegerField(default=0),
        ),
    ]
