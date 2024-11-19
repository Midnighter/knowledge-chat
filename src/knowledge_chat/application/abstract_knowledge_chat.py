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


"""Provide a high-level application interface for the knowledge chat."""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from .dto import ConversationDTO, ExchangeOutputDTO, UserDTO


class AbstractKnowledgeChat(ABC):
    """Define the high-level application interface for the knowledge chat."""

    @abstractmethod
    def create_user(self, user: UserDTO) -> UUID:
        """Create a new user instance and persist it."""

    @abstractmethod
    def get_user(self, user_id: str) -> UserDTO:
        """Get user data by their identifier."""

    @abstractmethod
    def start_conversation(self, user_id: str) -> UUID:
        """Add a new conversation to the user."""

    @abstractmethod
    def get_conversation(self, conversation_id: UUID) -> ConversationDTO:
        """Get conversation data by its identifier."""

    @abstractmethod
    def respond_to(
        self,
        query: str,
        conversation_id: UUID,
        callbacks: list[Any] | None = None,
    ) -> ExchangeOutputDTO:
        """Use a configured agent to respond to the given query."""
