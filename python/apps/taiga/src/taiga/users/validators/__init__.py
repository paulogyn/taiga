# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

from pydantic import EmailStr, StrictBool, constr, validator
from taiga.base.i18n import i18n
from taiga.base.serializers import BaseModel
from taiga.conf import settings
from taiga.users.validators.mixins import PasswordMixin

#####################################################################
# User Profile
#####################################################################


class CreateUserValidator(PasswordMixin, BaseModel):
    email: EmailStr
    full_name: constr(max_length=50)  # type: ignore
    accept_terms: StrictBool
    lang: str | None
    project_invitation_token: str | None
    accept_project_invitation: StrictBool = True

    @validator("email", "full_name")
    def check_not_empty(cls, v: str) -> str:
        assert v != "", "Empty field is not allowed"
        return v

    @validator("email")
    def check_email_in_domain(cls, v: str) -> str:
        if not settings.USER_EMAIL_ALLOWED_DOMAINS:
            return v

        domain = v.split("@")[1]
        assert domain in settings.USER_EMAIL_ALLOWED_DOMAINS, "Email domain not allowed"
        return v

    @validator("accept_terms")
    def check_accept_terms(cls, v: bool) -> bool:
        assert v is True, "User has to accept terms of service"
        return v

    @validator("lang")
    def check_lang(cls, v: str) -> str:
        if v:
            assert v in i18n.available_languages, "Language is not available"
        return v


class UpdateUserValidator(BaseModel):
    full_name: constr(max_length=50)  # type: ignore
    lang: str

    @validator("full_name", "lang")
    def check_not_empty(cls, v: str) -> str:
        assert v != "", "Empty field is not allowed"
        return v

    @validator("lang")
    def check_lang(cls, v: str) -> str:
        if v:
            assert v in i18n.available_languages, "Language is not available"
        return v


class VerifyTokenValidator(BaseModel):
    token: str


#####################################################################
# Reset Password
#####################################################################


class RequestResetPasswordValidator(BaseModel):
    email: EmailStr


class ResetPasswordValidator(PasswordMixin, BaseModel):
    ...
