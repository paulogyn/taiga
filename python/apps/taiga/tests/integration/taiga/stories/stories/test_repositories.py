# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

import pytest
from asgiref.sync import sync_to_async
from taiga.stories.stories import repositories
from tests.utils import factories as f

pytestmark = pytest.mark.django_db


##########################################################
# create_story
##########################################################


async def test_create_story_ok() -> None:
    user = await f.create_user()
    project = await f.create_simple_project()
    workflow = await f.create_workflow(project=project)
    status = await f.create_workflow_status(workflow=workflow)

    story = await repositories.create_story(
        title="test_create_story_ok",
        project_id=project.id,
        workflow_id=workflow.id,
        status_id=status.id,
        user_id=user.id,
        order=100,
    )

    assert story.title == "test_create_story_ok"


##########################################################
# get_story
##########################################################


async def test_get_story() -> None:
    story1 = await f.create_story()
    story = await repositories.get_story(
        filters={"project_id": story1.project.id, "workflow_id": story1.workflow.id, "ref": story1.ref}
    )
    assert story1.ref == story.ref
    assert story1.title == story.title
    assert story1.id == story.id


##########################################################
# get_stories
##########################################################


async def test_get_stories() -> None:
    admin = await f.create_user()
    project = await f.create_project(owner=admin)
    workflow_1 = await sync_to_async(project.workflows.first)()
    status_1 = await sync_to_async(workflow_1.statuses.first)()
    workflow_2 = await f.create_workflow(project=project)
    status_2 = await sync_to_async(workflow_2.statuses.first)()

    story1 = await f.create_story(project=project, workflow=workflow_1, status=status_1)
    await f.create_story(project=project, workflow=workflow_1, status=status_1)
    await f.create_story(project=project, workflow=workflow_2, status=status_2)

    stories = await repositories.get_stories(filters={"project_id": project.id})
    assert len(stories) == 3
    assert stories[0].title and stories[0].ref and stories[0].status
    stories = await repositories.get_stories(filters={"workflow_id": workflow_1.id})
    assert len(stories) == 2
    stories = await repositories.get_stories(filters={"workflow_id": workflow_2.id})
    assert len(stories) == 1
    stories = await repositories.get_stories(filters={"workflow_id": workflow_1.id, "refs": [story1.ref]})
    assert len(stories) == 1


##########################################################
# update_story
##########################################################


async def test_update_story_success() -> None:
    project = await f.create_project()
    workflow = await project.workflows.afirst()
    status = await workflow.statuses.afirst()
    story = await f.create_story(project=project, workflow=workflow, status=status)

    assert await repositories.update_story(
        id=story.id,
        current_version=story.version,
        values={"title": "new title"},
    )


async def test_update_story_error() -> None:
    project = await f.create_project()
    workflow = await project.workflows.afirst()
    status = await workflow.statuses.afirst()
    story = await f.create_story(project=project, workflow=workflow, status=status)

    assert not await repositories.update_story(
        id=story.id,
        current_version=story.version + 1,
        values={"title": "new title"},
    )


##########################################################
# misc - get_story_neighbors
##########################################################


async def test_get_story_neighbors() -> None:
    pj_admin = await f.create_user()
    project = await f.create_project(owner=pj_admin)

    # same status for all stories
    workflow1 = await sync_to_async(project.workflows.first)()
    status11 = await sync_to_async(workflow1.statuses.first)()
    status12 = await sync_to_async(workflow1.statuses.last)()
    story1 = await f.create_story(project=project, workflow=workflow1, status=status11)
    story2 = await f.create_story(project=project, workflow=workflow1, status=status11)
    story3 = await f.create_story(project=project, workflow=workflow1, status=status11)
    await f.create_story(project=project, workflow=workflow1, status=status12)

    neighbors = await repositories.get_story_neighbors(story=story1, filters={"status_id": status11.id})
    assert neighbors.prev is None
    assert neighbors.next.ref == story2.ref

    neighbors = await repositories.get_story_neighbors(story=story2, filters={"status_id": status11.id})
    assert neighbors.prev.ref == story1.ref
    assert neighbors.next.ref == story3.ref

    neighbors = await repositories.get_story_neighbors(story=story3, filters={"status_id": status11.id})
    assert neighbors.prev.ref == story2.ref
    assert neighbors.next is None

    # different statuses
    workflow2 = await f.create_workflow(project=project)
    status21 = await f.create_workflow_status(workflow=workflow2, name="New", slug="new", color=1, order=1)
    status22 = await f.create_workflow_status(
        workflow=workflow2, name="In progress", slug="in-progress", color=1, order=2
    )
    status23 = await f.create_workflow_status(workflow=workflow2, name="Done", slug="Done", color=1, order=3)
    story1 = await f.create_story(project=project, workflow=workflow2, status=status21)
    story2 = await f.create_story(project=project, workflow=workflow2, status=status22)
    story3 = await f.create_story(project=project, workflow=workflow2, status=status23)

    neighbors = await repositories.get_story_neighbors(story=story1, filters={"workflow_id": workflow2.id})
    assert neighbors.prev is None
    assert neighbors.next.ref == story2.ref

    neighbors = await repositories.get_story_neighbors(story=story1, filters={"status_id": status21.id})
    assert neighbors.prev is None
    assert neighbors.next is None

    neighbors = await repositories.get_story_neighbors(story=story2, filters={"workflow_id": workflow2.id})
    assert neighbors.prev.ref == story1.ref
    assert neighbors.next.ref == story3.ref

    neighbors = await repositories.get_story_neighbors(story=story3, filters={"workflow_id": workflow2.id})
    assert neighbors.prev.ref == story2.ref
    assert neighbors.next is None


##########################################################
# misc - get_total_stories
##########################################################


async def test_get_total_stories() -> None:
    admin = await f.create_user()
    project = await f.create_project(owner=admin)
    workflow_1 = await sync_to_async(project.workflows.first)()
    status_1 = await sync_to_async(workflow_1.statuses.first)()
    workflow_2 = await f.create_workflow(project=project)
    status_2 = await sync_to_async(workflow_2.statuses.first)()

    await f.create_story(project=project, workflow=workflow_1, status=status_1)
    await f.create_story(project=project, workflow=workflow_1, status=status_1)
    await f.create_story(project=project, workflow=workflow_2, status=status_2)

    total_stories = await repositories.get_total_stories(filters={"project_id": project.id})
    assert total_stories == 3
    total_stories = await repositories.get_total_stories(
        filters={"project_id": project.id, "workflow_id": workflow_1.id}
    )
    assert total_stories == 2
    total_stories = await repositories.get_total_stories(
        filters={"project_id": project.id, "workflow_id": workflow_2.id}
    )
    assert total_stories == 1


##########################################################
# misc - get_stories_to_reorder
##########################################################


async def test_get_stories_to_reorder() -> None:
    admin = await f.create_user()
    project = await f.create_project(owner=admin)
    workflow = await sync_to_async(project.workflows.first)()
    status = await sync_to_async(workflow.statuses.first)()

    story1 = await f.create_story(project=project, workflow=workflow, status=status)
    story2 = await f.create_story(project=project, workflow=workflow, status=status)
    story3 = await f.create_story(project=project, workflow=workflow, status=status)

    stories = await repositories.get_stories_to_reorder(
        filters={"status_id": status.id, "refs": [story1.ref, story2.ref, story3.ref]}
    )
    assert stories[0].ref == story1.ref
    assert stories[1].ref == story2.ref
    assert stories[2].ref == story3.ref

    stories = await repositories.get_stories_to_reorder(
        filters={"status_id": status.id, "refs": [story1.ref, story3.ref, story2.ref]}
    )
    assert stories[0].ref == story1.ref
    assert stories[1].ref == story3.ref
    assert stories[2].ref == story2.ref

    stories = await repositories.get_stories_to_reorder(
        filters={"status_id": status.id, "refs": [story3.ref, story1.ref, story2.ref]}
    )
    assert stories[0].ref == story3.ref
    assert stories[1].ref == story1.ref
    assert stories[2].ref == story2.ref
