/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router } from '@angular/router';
import { ProjectApiService } from '@taiga/api';
import { ConfigService } from '@taiga/core';
import { InvitationInfo, Project } from '@taiga/data';
import { of, throwError } from 'rxjs';
import { catchError, mergeMap } from 'rxjs/operators';
import { AuthService } from '~/app/modules/auth/data-access/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class ProjectInvitationGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient,
    private config: ConfigService,
    private projectApiService: ProjectApiService
  ) {}

  public canActivate(route: ActivatedRouteSnapshot) {
    const token = route.params.token as string;

    return this.http
      .get<InvitationInfo>(
        `${this.config.apiUrl}/projects/invitations/${token}`
      )
      .pipe(
        mergeMap((invitation: InvitationInfo) => {
          if (this.authService.isLogged()) {
            return this.http
              .post<{ slug: Project['slug'] }>(
                `${this.config.apiUrl}/projects/invitations/${token}/accept`,
                {}
              )
              .pipe(
                mergeMap(() => {
                  void this.router.navigate([
                    `/project/${invitation.project.slug}`,
                  ]);
                  return of(true);
                })
              );
          } else {
            if (invitation.existingUser) {
              void this.router.navigate(['/login'], {
                queryParams: {
                  next: `/project/${invitation.project.slug}`,
                  invitationToken: token,
                },
              });
            } else {
              void this.router.navigate(['/signup'], {
                queryParams: {
                  project: invitation.project.name,
                  email: invitation.email,
                  token,
                },
              });
            }
            return of(true);
          }
        }),
        catchError((httpResponse: HttpErrorResponse) => {
          void this.router.navigate(['/']);
          return throwError(httpResponse);
        })
      );
  }
}