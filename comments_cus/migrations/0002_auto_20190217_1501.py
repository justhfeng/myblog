# Generated by Django 2.1.4 on 2019-02-17 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments_cus', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='comment_text',
        ),
    ]
