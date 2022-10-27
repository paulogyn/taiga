# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

import pytest
from fastapi import status
from tests.utils import factories as f

pytestmark = pytest.mark.django_db


#########################################################################
# PUT /projects/<project_slug>/roles/<role_slug>/permissions
#########################################################################


async def test_update_project_role_permissions_anonymous_user(client):
    project = await f.create_project()
    role_slug = "general"
    data = {"permissions": ["view_story"]}

    response = client.put(f"/projects/{project.slug}/roles/{role_slug}/permissions", json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.text


async def test_update_project_role_permissions_project_not_found(client):
    user = await f.create_user()
    data = {"permissions": ["view_story"]}

    client.login(user)
    response = client.put("/projects/non-existent/roles/role-slug/permissions", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


async def test_update_project_role_permissions_role_not_found(client):
    project = await f.create_project()
    data = {"permissions": ["view_story"]}

    client.login(project.owner)
    response = client.put(f"/projects/{project.slug}/roles/role-slug/permissions", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


async def test_update_project_role_permissions_user_without_permission(client):
    user = await f.create_user()
    project = await f.create_project()
    data = {"permissions": ["view_story"]}

    client.login(user)
    response = client.put(f"/projects/{project.slug}/roles/role-slug/permissions", json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.text


async def test_update_project_role_permissions_role_admin(client):
    project = await f.create_project()
    role_slug = "admin"
    data = {"permissions": ["view_story"]}

    client.login(project.owner)
    response = client.put(f"/projects/{project.slug}/roles/{role_slug}/permissions", json=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.text


async def test_update_project_role_permissions_incompatible_permissions(client):
    project = await f.create_project()
    role_slug = "general"
    data = {"permissions": ["view_task"]}

    client.login(project.owner)
    response = client.put(f"/projects/{project.slug}/roles/{role_slug}/permissions", json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


async def test_update_project_role_permissions_not_valid_permissions(client):
    project = await f.create_project()
    role_slug = "general"
    data = {"permissions": ["not_valid", "foo"]}

    client.login(project.owner)
    response = client.put(f"/projects/{project.slug}/roles/{role_slug}/permissions", json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


async def test_update_project_role_permissions_ok(client):
    project = await f.create_project()
    role_slug = "general"
    data = {"permissions": ["view_story"]}

    client.login(project.owner)
    response = client.put(f"/projects/{project.slug}/roles/{role_slug}/permissions", json=data)

    assert response.status_code == status.HTTP_200_OK, response.text
    assert data["permissions"] == response.json()["permissions"]