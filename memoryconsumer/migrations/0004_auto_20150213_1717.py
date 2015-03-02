# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memoryconsumer', '0003_auto_20150213_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memloadstat',
            name='availdelta',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='memloadstat',
            name='availmem',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='memloadstat',
            name='memload',
            field=models.BigIntegerField(default=None),
        ),
    ]
