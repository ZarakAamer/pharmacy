# Generated by Django 4.1.3 on 2023-03-11 21:32

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_bankinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankinfo',
            name='instructions',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=' '),
            preserve_default=False,
        ),
    ]
