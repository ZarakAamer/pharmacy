# Generated by Django 4.1.3 on 2023-02-23 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.CharField(max_length=20)),
                ('percentage', models.PositiveIntegerField()),
                ('avalible', models.BooleanField(default=True)),
            ],
        ),
    ]
