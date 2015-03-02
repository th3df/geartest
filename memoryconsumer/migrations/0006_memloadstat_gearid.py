# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memoryconsumer', '0005_auto_20150213_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='memloadstat',
            name='gearID',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
