# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memoryconsumer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memloadstat',
            old_name='totmem',
            new_name='availmem',
        ),
    ]
