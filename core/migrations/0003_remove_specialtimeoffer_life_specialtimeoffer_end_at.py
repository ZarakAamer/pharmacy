# Generated by Django 4.1.3 on 2023-02-23 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialtimeoffer',
            name='life',
        ),
        migrations.AddField(
            model_name='specialtimeoffer',
            name='end_at',
            field=models.DateTimeField(null=True),
        ),
    ]
