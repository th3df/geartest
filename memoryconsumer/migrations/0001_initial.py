# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Memloadstat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('memload', models.TextField(default='')),
                ('usedmem', models.TextField(default='')),
                ('totmem', models.TextField(default='')),
                ('exp', models.ForeignKey(to='memoryconsumer.Experiment', default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
