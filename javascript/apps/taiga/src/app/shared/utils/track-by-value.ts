/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2023-present Kaleidos INC
 */

import { TrackByFunction } from '@angular/core';

export const trackByValue: <T>() => TrackByFunction<T> =
  <T>() =>
  (_: number, item: T) => {
    return item;
  };