# Generated by Django 2.1.4 on 2019-02-13 10:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('read_num_count', '0003_auto_20190212_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadNumDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_date', models.DateField(default=datetime.datetime(2019, 2, 13, 10, 50, 33, 487334, tzinfo=utc))),
                ('read_num', models.IntegerField(default=0)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
            ],
        ),
        migrations.RemoveField(
            model_name='readnumagg',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='ReadNumAgg',
        ),
    ]
