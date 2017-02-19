# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.hashers import make_password
from django.conf import settings

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.create(username=settings.ADMIN_LOGNAME,
                        email=settings.ADMIN_EMAIL,
                        password=make_password(settings.ADMIN_PASS),
                        is_superuser=True,
                        is_staff=True,
                        is_active=True)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170115_1541'),
        ('auth', '__latest__')
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
