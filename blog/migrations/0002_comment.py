# -*- coding: utf-8 -*-
"""Initial migration. Autocreated.

- Migration - determines migration objects
"""
from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):
    """Determine migration process and objects."""

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True,
                                        auto_created=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('text', models.TextField()),
                ('post', models.ForeignKey(related_name='comments', to='blog.Post')),
            ],
        ),
    ]
