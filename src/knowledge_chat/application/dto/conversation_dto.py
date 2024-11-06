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


"""Provide a conversation data transfer object (DTO)."""

from __future__ import annotations

from typing import NamedTuple
from uuid import UUID  # noqa: TCH003

from knowledge_chat.domain.model import Conversation


class ConversationDTO(NamedTuple):
    """Define the conversation data transfer object (DTO)."""

    user_id: str
    conversation_id: str
    user_reference: UUID

    @classmethod
    def from_conversation(
        cls,
        user_id: str,
        conversation_id: str,
        conversation: Conversation,
    ) -> ConversationDTO:
        """Transform a conversation domain model into a DTO."""
        return cls(
            user_id=user_id,
            conversation_id=conversation_id,
            user_reference=conversation.user_reference,
        )

    def create(self) -> Conversation:
        """Create a new conversation instance."""
        return Conversation(user_reference=self.user_reference)
