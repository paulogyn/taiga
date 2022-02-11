# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

import pytest
from django.contrib.auth.models import AnonymousUser
from taiga.base.api.permissions import And, Not, Or, check_permissions
from taiga.exceptions import api as ex
from taiga.permissions import (
    AllowAny,
    DenyAll,
    HasPerm,
    IsAuthenticated,
    IsObjectOwner,
    IsProjectAdmin,
    IsSuperUser,
    IsWorkspaceAdmin,
)
from tests.utils import factories as f

pytestmark = pytest.mark.django_db


#####################################################
# check_permissions (is_authorized)
#####################################################


async def test_check_permission_allow_any():
    user1 = await f.create_user()
    permissions = AllowAny()

    # always granted permissions
    assert await check_permissions(permissions=permissions, user=user1, obj=None) is None


async def test_check_permission_deny_all():
    user = await f.create_user()
    permissions = DenyAll()

    # never granted permissions
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user, obj=None)


async def test_check_permission_is_authenticated():
    user1 = await f.create_user()
    user2 = AnonymousUser()
    permissions = IsAuthenticated()

    # User.is_authenticated is always True
    assert await check_permissions(permissions=permissions, user=user1, obj=None) is None
    # AnonymousUser.is_authenticated is always False
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user2, obj=None)


async def test_check_permission_is_superuser():
    user1 = await f.create_user(is_superuser=True)
    user2 = await f.create_user(is_superuser=False)
    permissions = IsSuperUser()

    assert await check_permissions(permissions=permissions, user=user1, obj=None) is None
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user2, obj=None)


async def test_check_permission_has_perm():
    user1 = await f.create_user()
    user2 = await f.create_user()
    project1 = await f.create_project(owner=user1)
    project2 = await f.create_project()
    permissions = HasPerm("modify_project")

    # user1 has modify permissions
    assert await check_permissions(permissions=permissions, user=user1, obj=project1) is None
    # user2 hasn't modify permissions
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user2, obj=project2)


async def test_check_permission_is_owner():
    user1 = await f.create_user()
    user2 = await f.create_user()
    workspace = await f.create_workspace(name="workspace1", owner=user1)
    project = await f.create_project(owner=user1)
    permissions = IsObjectOwner()

    # user1 owns project
    assert await check_permissions(permissions=permissions, user=user1, obj=project) is None
    # user1 owns workspace
    assert await check_permissions(permissions=permissions, user=user1, obj=workspace) is None
    # user2 doesn't own project
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user2, obj=project)
    # user2 doesn't own wokspace
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user2, obj=workspace)


async def test_check_permission_is_project_admin():
    user1 = await f.create_user()
    user2 = await f.create_user()
    project = await f.create_project(owner=user1)
    permissions = IsProjectAdmin()

    # user1 is pj-admin
    assert await check_permissions(permissions=permissions, user=user1, obj=project) is None
    # user2 isn't pj-admin
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user2, obj=project)


async def test_check_permission_is_workspace_admin():
    user1 = await f.create_user()
    user2 = await f.create_user()
    workspace = await f.create_workspace(name="workspace1", owner=user1)
    permissions = IsWorkspaceAdmin()

    # user1 is ws-admin
    assert await check_permissions(permissions=permissions, user=user1, obj=workspace) is None
    # user2 isn't ws-admin
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, user=user2, obj=workspace)


#######################################################
# check_permissions (global & enough_perms)
#######################################################


async def test_check_permission_global_perms():
    # user is pj-admin
    user = await f.create_user()
    project = await f.create_project(owner=user)
    permissions = IsProjectAdmin()

    # user IsProjectAdmin (true) & globalPerm(AllowAny) (true)
    assert await check_permissions(permissions=permissions, global_perms=AllowAny(), user=user, obj=project) is None
    # user IsProjectAdmin (true) & globalPerm(AllowAny) (false)
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permissions, global_perms=DenyAll(), user=user, obj=project)


async def test_check_permission_enough_perms():
    # user is a pj-admin
    user = await f.create_user()
    project = await f.create_project(owner=user)
    true_permission = IsProjectAdmin()

    # user IsProjectAdmin (true) | globalPerm(AllowAny) (true)
    assert await check_permissions(permissions=true_permission, enough_perms=AllowAny(), user=user, obj=project) is None
    # user IsProjectAdmin (true) | globalPerm(AllowAny) (false)
    assert await check_permissions(permissions=true_permission, enough_perms=DenyAll(), user=user, obj=project) is None


#############################################
# PermissionOperators (Not/Or/And)
#############################################
async def test_check_permission_operators():
    # user is a pj-admin
    user = await f.create_user()
    project = await f.create_project(owner=user)

    permission_true_and = And(IsProjectAdmin(), HasPerm("modify_project"))
    permission_false_and = And(IsProjectAdmin(), HasPerm("modify_project"), IsSuperUser())
    permission_true_all_or = Or(IsProjectAdmin(), HasPerm("modify_project"))
    permission_true_some_or = Or(IsProjectAdmin(), HasPerm("modify_project"), IsSuperUser())
    permission_false_or = Or(IsSuperUser(), DenyAll())
    permission_true_not = Not(DenyAll())
    permission_false_not = Not(AllowAny())
    permission_true_all_together = Not(And(permission_true_all_or, permission_false_and))
    permission_false_all_together = Not(Or(permission_true_all_or, permission_false_and))

    # user IsProjectAdmin (true) & HasPerm("modify_project") (true)
    assert await check_permissions(permissions=permission_true_and, user=user, obj=project) is None
    # user IsProjectAdmin (true) & HasPerm("modify_project") (true) & IsSuperUser() (false)
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permission_false_and, user=user, obj=project)
    # user IsProjectAdmin (true) | HasPerm("modify_project") (true)
    assert await check_permissions(permissions=permission_true_all_or, user=user, obj=project) is None
    # user IsProjectAdmin (true) | HasPerm("modify_project") (true) | IsSuperUser() (false)
    assert await check_permissions(permissions=permission_true_some_or, user=user, obj=project) is None
    # user IsSuperUser (false) | DenyAll() (false)
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permission_false_or, user=user, obj=project)
    # Not(DenyAll()) Not(false)
    assert await check_permissions(permissions=permission_true_not, user=user, obj=project) is None
    # Not(AllowAny()) Not(true)
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permission_false_not, user=user, obj=project)
    # Not(permission_true_all_or (true) & permission_false_and (false))
    assert await check_permissions(permissions=permission_true_all_together, user=user, obj=project) is None
    # Not(permission_true_all_or (true) | permission_false_and (false))
    with pytest.raises(ex.ForbiddenError):
        await check_permissions(permissions=permission_false_all_together, user=user, obj=project)