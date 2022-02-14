/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

import { createAction, props } from '@ngrx/store';
import { Project, Role } from '@taiga/data';

export const fetchMemberRolesSuccess = createAction(
  '[Roles] fetch members success',
  props<{ roles: Role[] }>()
);

export const fetchPublicPermissionsSuccess = createAction(
  '[Roles] fetch public permissions success',
  props<{ permissions: string[] }>()
);

export const fetchWorkspacePermissionsSuccess = createAction(
  '[Roles] fetch workspace permissions success',
  props<{ permissions: string[] }>()
);

export const updateRolePermissions = createAction(
  '[Roles] update role permissions',
  props<{
    project: Project['slug'];
    roleSlug: Role['slug'];
    permissions: string[];
  }>()
);

export const updatePublicPermissions = createAction(
  '[Roles] update public permissions',
  props<{ project: Project['slug']; permissions: string[] }>()
);

export const updatePublicPermissionsSuccess = createAction(
  '[Roles] update public success',
  props<{ permissions: string[] }>()
);

export const updateWorkspacePermissions = createAction(
  '[Roles] update workspace permissions',
  props<{ project: Project['slug']; permissions: string[] }>()
);

export const updateWorkspacePermissionsSuccess = createAction(
  '[Roles] update workspace success',
  props<{ permissions: string[] }>()
);

export const updateRolePermissionsSuccess = createAction(
  '[Roles] update role permissions success',
  props<{ role: Role }>()
);

export const updateRolePermissionsError = createAction(
  '[Roles] update role permissions error'
);

export const resetPermissions = createAction('[Roles] reset all permissions');

export const initRolesPermissions = createAction(
  '[Roles] init roles and permissions',
  props<{ project: Project }>()
);