# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190903_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='upw',
            field=models.CharField(max_length=50),
        ),
    ]
