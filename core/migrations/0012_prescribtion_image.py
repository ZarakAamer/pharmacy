# Generated by Django 4.1.3 on 2023-04-23 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_product_stock_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescribtion',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='prescription'),
        ),
    ]
