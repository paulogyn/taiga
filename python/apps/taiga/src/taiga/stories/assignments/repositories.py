# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

from typing import Literal, TypedDict
from uuid import UUID

from asgiref.sync import sync_to_async
from taiga.base.db.models import QuerySet
from taiga.stories.assignments.models import StoryAssignment
from taiga.stories.stories.models import Story
from taiga.users.models import User

##########################################################
# filters and querysets
##########################################################

DEFAULT_QUERYSET = StoryAssignment.objects.all()


class StoryAssignmentFilters(TypedDict, total=False):
    story_id: UUID
    username: str


def _apply_filters_to_queryset(
    qs: QuerySet[StoryAssignment],
    filters: StoryAssignmentFilters = {},
) -> QuerySet[StoryAssignment]:
    filter_data = dict(filters.copy())

    if "username" in filter_data:
        filter_data["user__username"] = filter_data.pop("username")

    return qs.filter(**filter_data)


StoryAssignmentSelectRelated = list[
    Literal[
        "story",
        "user",
    ]
]


def _apply_select_related_to_queryset(
    qs: QuerySet[StoryAssignment],
    select_related: StoryAssignmentSelectRelated,
) -> QuerySet[StoryAssignment]:
    return qs.select_related(*select_related)


##########################################################
# create story assignment
##########################################################


@sync_to_async
def create_story_assignment(story: Story, user: User) -> tuple[StoryAssignment, bool]:
    return StoryAssignment.objects.select_related("story", "user").get_or_create(story=story, user=user)


##########################################################
# delete story assignment
##########################################################


@sync_to_async
def delete_story_assignment(filters: StoryAssignmentFilters = {}) -> int:
    qs = _apply_filters_to_queryset(qs=DEFAULT_QUERYSET, filters=filters)
    count, _ = qs.delete()
    return count