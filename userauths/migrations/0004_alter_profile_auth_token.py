# Generated by Django 4.1.3 on 2023-04-05 11:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_alter_profile_auth_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='auth_token',
            field=models.CharField(default=uuid.UUID('2f88ad89-ab91-4e13-bfc5-7a0092cb5122'), max_length=200),
        ),
    ]