# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2023-present Kaleidos INC

# Generated by Django 4.2.3 on 2023-09-01 19:15

import django.db.models.deletion
import taiga.base.db.models
import taiga.base.utils.datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("storage", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        blank=True,
                        default=taiga.base.db.models.uuid_generator,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=taiga.base.utils.datetime.aware_utcnow,
                        verbose_name="created at",
                    ),
                ),
                ("name", models.TextField(verbose_name="file name")),
                ("content_type", models.TextField(verbose_name="file content type")),
                ("size", models.IntegerField(verbose_name="file size (bytes)")),
                ("object_id", models.UUIDField(verbose_name="object id")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "storaged_object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="attachments",
                        to="storage.storagedobject",
                        verbose_name="storaged object",
                    ),
                ),
                (
                    "object_content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                        verbose_name="object content type",
                    ),
                ),
            ],
            options={
                "verbose_name": "attachment",
                "verbose_name_plural": "attachments",
                "ordering": ["object_content_type", "object_id", "-created_at"],
                "indexes": [
                    models.Index(
                        fields=["object_content_type", "object_id"],
                        name="attachments_object__8a3a6a_idx",
                    )
                ],
            },
        ),
    ]
