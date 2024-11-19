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


"""Provide an abstract interface for the domain service registry."""

from abc import ABC, abstractmethod
from typing import Any

from langchain_community.graphs import Neo4jGraph
from langchain_core.language_models.chat_models import BaseChatModel

from .response_agent import ResponseAgent


class DomainServiceRegistry(ABC):
    """Define the abstract interface for the domain service registry."""

    @abstractmethod
    def get_response_agent(
        self,
        agent_settings: Any,  # noqa: ANN401
        knowledge_graph: Neo4jGraph,
        chat_model: BaseChatModel,
        custom_prompt: str | None = None,
        **kwargs,
    ) -> ResponseAgent:
        """Return a fully configured response agent."""
