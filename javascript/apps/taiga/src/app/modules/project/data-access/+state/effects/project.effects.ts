/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';

import { map, tap } from 'rxjs/operators';

import * as ProjectActions from '../actions/project.actions';
import { ProjectApiService } from '@taiga/api';
import { fetch } from '@nrwl/angular';
import { NavigationService } from '~/app/shared/navigation/navigation.service';

@Injectable()
export class ProjectEffects {

  public loadProject$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(ProjectActions.fetchProject),
      fetch({
        run: (action) => {
          return this.projectApiService.getProject(action.slug).pipe(
            map((project) => {
              return ProjectActions.fetchProjectSuccess({ project });
            })
          );
        },
        onError: () => {
          return null;
        },
      })
    );
  });

  public projectSuccess$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(ProjectActions.fetchProjectSuccess),
      tap(({ project }) => {
        this.navigationService.add(project);
      })
    );
  }, { dispatch: false });

  public loadRoles$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(ProjectActions.fetchRoles),
      fetch({
        run: (action) => {
          return this.projectApiService.getRoles(action.slug).pipe(
            map((roles) => {
              return ProjectActions.fetchRolesSuccess({ roles });
            })
          );
        },
        onError: () => {
          return null;
        },
      })
    );
  });

  constructor(
    private actions$: Actions,
    private projectApiService: ProjectApiService,
    private navigationService: NavigationService,
  ) {}

}