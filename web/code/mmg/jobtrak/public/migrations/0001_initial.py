# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-19 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Page Content',
                'verbose_name_plural': 'Page Content',
            },
        ),
    ]