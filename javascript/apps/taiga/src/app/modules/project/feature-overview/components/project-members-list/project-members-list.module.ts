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
import {
  TuiButtonModule,
  TuiHintModule,
  TuiLinkModule,
  TuiSvgModule,
} from '@taiga-ui/core';
import { AvatarModule } from '@taiga/ui/avatar';
import { UserCardModule } from '~/app/shared/user-card/user-card-component.module';
import { ProjectMembersListComponent } from './project-members-list.component';

@NgModule({
  imports: [
    CommonModule,
    TuiButtonModule,
    TuiSvgModule,
    AvatarModule,
    TranslocoModule,
    TuiLinkModule,
    UserCardModule,
    TuiHintModule,
  ],
  declarations: [ProjectMembersListComponent],
  exports: [ProjectMembersListComponent],
  providers: [
    {
      provide: TRANSLOCO_SCOPE,
      useValue: {
        scope: 'project_overview',
        alias: 'project_overview',
      },
    },
  ],
})
export class ProjectMembersListModule {}