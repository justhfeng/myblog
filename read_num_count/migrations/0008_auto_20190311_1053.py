# Generated by Django 2.1.4 on 2019-03-11 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read_num_count', '0007_auto_20190217_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnum',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='readnumdetail',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]