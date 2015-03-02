# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memoryconsumer', '0004_auto_20150213_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memloadstat',
            name='availdelta',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='memloadstat',
            name='availmem',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='memloadstat',
            name='exp',
            field=models.ForeignKey(default=0, to='memoryconsumer.Experiment'),
        ),
        migrations.AlterField(
            model_name='memloadstat',
            name='memload',
            field=models.BigIntegerField(default=0),
        ),
    ]
