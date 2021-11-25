/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { TranslocoModule, TRANSLOCO_SCOPE } from '@ngneat/transloco';
import { TuiButtonModule, TuiSvgModule } from '@taiga-ui/core';
import { AvatarModule } from '@taiga/ui/avatar';
import { ProjectSettingsComponent } from './project-settings.component';

@NgModule({
  imports: [
    CommonModule,
    TuiButtonModule,
    TuiSvgModule,
    TranslocoModule,
    AvatarModule
  ],
  declarations: [
    ProjectSettingsComponent,
  ],
  providers: [
    {
      provide: TRANSLOCO_SCOPE,
      useValue: {
        scope: 'project_settings',
        alias: 'project_settings',
      },
    },
  ],
  exports: [
    ProjectSettingsComponent,
  ]

})
export class ProjectSettingsModule {}