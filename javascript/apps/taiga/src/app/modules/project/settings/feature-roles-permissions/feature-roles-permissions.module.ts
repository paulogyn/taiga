/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProjectsSettingsFeatureRolesPermissionsComponent } from './feature-roles-permissions.component';
import { inViewportDirective } from '~/app/shared/directives/intersection-observer.directive';
import { TuiAutoFocusModule } from '@taiga-ui/cdk';

@NgModule({
  declarations: [
    ProjectsSettingsFeatureRolesPermissionsComponent,
    inViewportDirective
  ],
  imports: [
    CommonModule,
    TuiAutoFocusModule,
    RouterModule.forChild([
      {
        path: '',
        component: ProjectsSettingsFeatureRolesPermissionsComponent
      }
    ])
  ],
  exports: [
    ProjectsSettingsFeatureRolesPermissionsComponent,
    inViewportDirective
  ],
})
export class ProjectsSettingsFeatureRolesPermissionsModule { }
