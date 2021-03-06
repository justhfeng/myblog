# Generated by Django 2.1.4 on 2019-02-03 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_auto_20190202_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_time', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='blog',
            name='read_time',
        ),
        migrations.AddField(
            model_name='readtime',
            name='blog',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='mainsite.Blog'),
        ),
    ]
