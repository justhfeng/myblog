# Generated by Django 2.1.4 on 2019-03-15 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments_cus', '0007_auto_20190311_1053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
    ]
