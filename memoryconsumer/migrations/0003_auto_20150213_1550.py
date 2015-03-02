# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memoryconsumer', '0002_auto_20150212_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memloadstat',
            name='usedmem',
        ),
        migrations.AddField(
            model_name='memloadstat',
            name='availdelta',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='memloadstat',
            name='availmem',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='memloadstat',
            name='memload',
            field=models.BigIntegerField(default=0),
        ),
    ]
