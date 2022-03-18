/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { TranslocoService } from '@ngneat/transloco';

@Component({
  selector: 'tg-user-to-invite',
  templateUrl: './user-to-invite.component.html',
  styleUrls: [
    '../../../styles/kanban.shared.css',
    './user-to-invite.component.css',
  ],
})
export class UserToInviteComponent {
  constructor(private translocoService: TranslocoService) {}

  @Output()
  public delete = new EventEmitter<number>();

  @Input()
  public user!: FormGroup;

  @Input()
  public userIndex!: number;

  public rolesList = [
    this.translocoService.translate('kanban.invite_step.general'),
    this.translocoService.translate('kanban.invite_step.member'),
  ];

  public trackByIndex(index: number) {
    return index;
  }

  public deleteUser() {
    this.delete.next(this.userIndex);
  }

  public insertionOrder() {
    return 0;
  }
}