/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

import { CdkDragMove } from '@angular/cdk/drag-drop';
import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  ElementRef,
  Input,
  OnChanges,
  SimpleChanges,
  ViewChild,
} from '@angular/core';
import { Store } from '@ngrx/store';
import { RxState } from '@rx-angular/state';
import { StoryView } from '@taiga/data';
import {
  selectLoadingStory,
  selectShowStoryView,
  selectStoryView,
} from '~/app/modules/project/data-access/+state/selectors/project.selectors';
import { LocalStorageService } from '~/app/shared/local-storage/local-storage.service';
interface WrapperSideViewState {
  showView: boolean;
  selectedStoryView: StoryView;
  loadingStory: boolean;
}

@Component({
  selector: 'tg-project-feature-story-wrapper-side-view',
  templateUrl: './project-feature-story-wrapper-side-view.component.html',
  styleUrls: ['./project-feature-story-wrapper-side-view.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [RxState],
})
export class ProjectFeatureStoryWrapperSideViewComponent implements OnChanges {
  @ViewChild('resizeSidepanel') public sidepanel?: ElementRef<HTMLElement>;
  @ViewChild('dragHandle') public dragHandle!: ElementRef<HTMLElement>;

  @Input() public kanbanWidth = 0;

  public readonly model$ = this.state.select();
  public sidepanelWidth = 0;
  public dragging = false;
  public sidepanelSetted = false;
  public sidebarOpen =
    LocalStorageService.get<boolean>('story_view_sidebar') ?? false;
  public minInlineSize = '';
  public maxInlineSize = '';

  public minWidthCollapsed = 440;
  public minWidthUncollapsed = 472;
  public widthToForceCollapse = 472;

  constructor(
    private store: Store,
    private cd: ChangeDetectorRef,
    private state: RxState<WrapperSideViewState>,
    private localStorage: LocalStorageService
  ) {
    this.state.connect('showView', this.store.select(selectShowStoryView));
    this.state.connect('selectedStoryView', this.store.select(selectStoryView));
    this.state.connect('loadingStory', this.store.select(selectLoadingStory));
  }

  public dragMove(dragHandle: HTMLElement, event: CdkDragMove<unknown>) {
    this.sidepanelWidth = window.innerWidth - event.pointerPosition.x;
    dragHandle.style.transform = 'translate(0, 0)';
  }

  public isDragging(isDragging: boolean) {
    this.dragging = isDragging;

    if (!isDragging) {
      this.localStorage.set('story_width', this.sidepanelWidth);
    }
  }

  public showDragbar() {
    const calculatedMinWidth = this.sidebarOpen
      ? this.minWidthCollapsed
      : this.minWidthUncollapsed;

    return this.kanbanWidth / 2 >= calculatedMinWidth;
  }

  public onToggleSidebar() {
    this.localStorage.set('story_view_sidebar', !this.sidebarOpen);
    this.sidebarOpen = !this.sidebarOpen;
  }

  public checkIfForceCollapse() {
    // Forcing collapse if width is inferior to widthToForceCollapse, only work on side-view.
    const selectedStoryView = this.state.get('selectedStoryView');
    if (
      this.sidepanelWidth <= this.widthToForceCollapse &&
      selectedStoryView === 'side-view'
    ) {
      this.sidebarOpen = false;
    }
  }

  public calculateInlineSize() {
    this.minInlineSize = this.calculateMinInlineSize();
    this.maxInlineSize = this.calculateMaxInlineSize();
  }

  public calculateMinInlineSize() {
    const quarterWidth = this.kanbanWidth / 4;
    const calculatedMinWidth = this.sidebarOpen
      ? this.minWidthCollapsed
      : this.minWidthUncollapsed;
    if (this.kanbanWidth && quarterWidth >= calculatedMinWidth) {
      return `${quarterWidth}px`;
    } else {
      return `${calculatedMinWidth}px`;
    }
  }

  public calculateMaxInlineSize() {
    return `${this.kanbanWidth / 2}px`;
  }

  public setInitialSidePanelWidth() {
    const storedStoryWidth = this.localStorage.get<number>('story_width');

    if (storedStoryWidth) {
      this.sidepanelWidth = storedStoryWidth;
      return;
    }

    this.sidepanelWidth = this.kanbanWidth / 4;

    const calculatedDifference =
      this.minWidthUncollapsed - this.minWidthCollapsed;

    if (this.sidebarOpen) {
      this.sidepanelWidth = this.sidepanelWidth + calculatedDifference;
    } else {
      this.sidepanelWidth = this.sidepanelWidth - calculatedDifference;
    }
  }

  public ngOnChanges(changes: SimpleChanges) {
    if (changes.kanbanWidth.currentValue && !this.sidepanelWidth) {
      this.setInitialSidePanelWidth();
      this.checkIfForceCollapse();
    }
    if (changes.kanbanWidth.currentValue) {
      this.calculateInlineSize();
    }
  }
}