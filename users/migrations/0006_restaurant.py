# Generated by Django 5.1.2 on 2024-11-09 05:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_foodbank_contact_number_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=255)),
                ('restaurant_phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'), ('NL', 'Newfoundland and Labrador'), ('NS', 'Nova Scotia'), ('ON', 'Ontario'), ('PE', 'Prince Edward Island'), ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut'), ('YT', 'Yukon')], max_length=100)),
                ('country', models.CharField(default='Canada', max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('website', models.URLField(blank=True, null=True)),
                ('id_verification', models.ImageField(blank=True, null=True, upload_to='id_cards/')),
                ('is_verified', models.BooleanField(default=False)),
                ('total_donations', models.IntegerField(default=0)),
                ('donation_frequency', models.FloatField(default=0.0)),
                ('donation_variety_count', models.IntegerField(default=0)),
                ('donation_volume', models.FloatField(default=0.0)),
                ('average_rating', models.FloatField(blank=True, null=True)),
                ('response_to_emergency_count', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
