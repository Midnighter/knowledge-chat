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


"""Provide Ollama connection settings."""

from __future__ import annotations

from typing import Annotated

from langchain_ollama import ChatOllama
from pydantic import Field, HttpUrl

from ._base_settings import BaseSettings


class OllamaSettings(BaseSettings):
    """Define the Ollama connection settings."""

    url: Annotated[HttpUrl, Field(..., validation_alias="OLLAMA_URL")]
    model: Annotated[str, Field(..., validation_alias="OLLAMA_MODEL")]
    temperature: Annotated[
        float,
        Field(default=0.0, validation_alias="OLLAMA_TEMPERATURE"),
    ]

    def create_model(self) -> ChatOllama:
        """Return an Ollama chat model instance."""
        return ChatOllama(
            base_url=str(self.url),
            model=self.model,
            temperature=self.temperature,
        )
