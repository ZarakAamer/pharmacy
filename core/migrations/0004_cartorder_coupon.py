# Generated by Django 4.1.3 on 2023-02-23 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_specialtimeoffer_life_specialtimeoffer_end_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.coupon'),
        ),
    ]
