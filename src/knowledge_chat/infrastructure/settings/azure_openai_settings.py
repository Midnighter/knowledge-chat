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


"""Provide Azure OpenAI connection settings."""

from __future__ import annotations

from typing import Annotated

from langchain_openai import AzureChatOpenAI
from pydantic import Field, SecretStr

from ._base_settings import BaseSettings


class AzureOpenAISettings(BaseSettings):
    """Define the Azure OpenAI connection settings."""

    service: Annotated[str, Field(..., validation_alias="AZURE_OPENAI_SERVICE")]
    api_key: Annotated[SecretStr, Field(..., validation_alias="AZURE_OPENAI_API_KEY")]
    api_version: Annotated[
        str,
        Field(
            default="2023-03-15-preview",
            validation_alias="AZURE_OPENAI_API_VERSION",
        ),
    ]
    api_type: Annotated[
        str,
        Field(default="azure", validation_alias="AZURE_OPENAI_API_TYPE"),
    ]
    deployment_name: Annotated[
        str,
        Field(default="chat", validation_alias="AZURE_OPENAI_DEPLOYMENT_NAME"),
    ]
    model_name: Annotated[
        str,
        Field(default="gpt-4", validation_alias="AZURE_OPENAI_MODEL_NAME"),
    ]
    temperature: Annotated[
        float,
        Field(default=0.0, validation_alias="AZURE_OPENAI_TEMPERATURE"),
    ]

    def create_model(self) -> AzureChatOpenAI:
        """Return a langchain Azure OpenAI chat model instance."""
        return AzureChatOpenAI(
            azure_endpoint=f"https://{self.service}.openai.azure.com",
            openai_api_key=self.api_key.get_secret_value(),  # type: ignore[arg-type]
            openai_api_version=self.api_version,
            azure_deployment=self.deployment_name,  # type: ignore[call-arg]
            model_name=self.model_name,
            temperature=self.temperature,
        )
