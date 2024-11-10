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


"""Provide an abstract interface for a response agent."""

from abc import ABC, abstractmethod

from langchain.chains.base import Chain
from langchain_core.tracers.base import BaseTracer

from knowledge_chat.domain.model import Conversation


class ResponseAgent(ABC):
    """Define the abstract interface for the response agent."""

    def __init__(self, *, chain: Chain, **kwargs) -> None:
        super().__init__(**kwargs)
        self._chain = chain

    @abstractmethod
    def generate_response(
        self,
        conversation: Conversation,
        callbacks: list[BaseTracer] | None = None,
        **kwargs,
    ) -> None:
        """Respond to the latest query in the conversation."""
