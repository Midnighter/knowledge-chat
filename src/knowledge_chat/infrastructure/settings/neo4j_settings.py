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


"""Provide Neo4j connection settings."""

from __future__ import annotations

import warnings
from typing import Annotated

from langchain_community.graphs import Neo4jGraph
from pydantic import AnyUrl, Field, SecretStr  # noqa: TCH002
from pydantic_settings import BaseSettings, SettingsConfigDict


class Neo4jSettings(BaseSettings):
    """Define the Neo4j connection settings."""

    model_config = SettingsConfigDict(
        case_sensitive=True,
        populate_by_name=True,
        extra="ignore",
        env_file=".env",
        secrets_dir="/run/secrets",
    )

    connection_uri: Annotated[
        AnyUrl,
        Field(..., validation_alias="NEO4J_CONNECTION_URI"),
    ]
    username: Annotated[str, Field(default="neo4j", validation_alias="NEO4J_USERNAME")]
    password: Annotated[
        SecretStr,
        Field(..., validation_alias="NEO4J_PASSWORD"),
    ]
    timeout: Annotated[float, Field(default=30.0, validation_alias="NEO4J_TIMEOUT")]

    @classmethod
    def create(cls, **kwargs) -> Neo4jSettings:
        """Create a settings instance from environment variables or secrets."""
        with warnings.catch_warnings():
            warnings.filterwarnings(
                action="ignore",
                message='directory "/run/secrets" does not exist',
                category=UserWarning,
            )
            return cls(**kwargs)

    def create_graph(self) -> Neo4jGraph:
        """Return a Neo4j graph instance with a langchain interface."""
        return Neo4jGraph(
            url=str(self.connection_uri),
            username=self.username,
            password=self.password.get_secret_value(),
            timeout=self.timeout,
            enhanced_schema=True,
        )
