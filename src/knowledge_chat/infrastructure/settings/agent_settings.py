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


"""Provide response agent settings."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from ._base_settings import BaseSettings


class AgentSettings(BaseSettings):
    """Define the response agent settings."""

    topic: Annotated[str, Field(..., validation_alias="AGENT_TOPIC")]
    prompt: Annotated[str | None, Field(None)]
