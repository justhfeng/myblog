# Generated by Django 2.1.4 on 2019-02-12 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0004_auto_20190203_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readtime',
            name='blog',
        ),
        migrations.DeleteModel(
            name='ReadTime',
        ),
    ]
