# Generated by Django 4.1.3 on 2023-05-19 22:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_alter_profile_auth_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='auth_token',
            field=models.CharField(default=uuid.UUID('e0069a2f-b238-445b-8247-eb19b08a542f'), max_length=200),
        ),
    ]