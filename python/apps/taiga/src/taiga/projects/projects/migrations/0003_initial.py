# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

# Generated by Django 4.1.1 on 2022-09-30 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("workspaces", "0001_initial"),
        ("projects", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="projects",
                to="workspaces.workspace",
                verbose_name="workspace",
            ),
        ),
        migrations.AlterIndexTogether(
            name="project",
            index_together={("name", "id")},
        ),
    ]