# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsersInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('pw', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('id_delete', models.IntegerField(default=0)),
                ('create_time', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'usersinfo',
            },
        ),
    ]
