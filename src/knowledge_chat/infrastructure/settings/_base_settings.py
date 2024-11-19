# Copyright (c) 2024 Moritz E. Beber
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


"""Provide a base settings configuration."""

from __future__ import annotations

import warnings

from pydantic_settings import BaseSettings as BaseSettings_
from pydantic_settings import SettingsConfigDict


class BaseSettings(BaseSettings_):
    """Define the base settings."""

    model_config = SettingsConfigDict(
        case_sensitive=True,
        populate_by_name=True,
        extra="ignore",
        env_file=".env",
        secrets_dir="/run/secrets",
    )

    @classmethod
    def create(cls, **kwargs) -> BaseSettings:
        """Create a settings instance from environment variables or secrets."""
        with warnings.catch_warnings():
            warnings.filterwarnings(
                action="ignore",
                message='directory "/run/secrets" does not exist',
                category=UserWarning,
            )
            return cls(**kwargs)
