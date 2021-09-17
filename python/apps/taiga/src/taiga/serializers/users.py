# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

from pydantic import EmailStr
from taiga.base.serializer import BaseModel


class UserBaseSerializer(BaseModel):
    id: int
    username: str
    full_name: str
    # photo: str  # TODO
    # big_photo: str  # TODO
    # gravatar_id: str  # TODO


class UserMeSerializer(UserBaseSerializer):
    email: EmailStr
    lang: str
    theme: str

    class Config:
        orm_mode = True