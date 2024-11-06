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

from knowledge_chat.domain.model import Conversation  # noqa: TCH001


class ConversationDTO(NamedTuple):
    """Define the conversation data transfer object (DTO)."""

    user_id: str
    conversation_id: str

    @classmethod
    def from_conversation(
        cls,
        user_id: str,
        conversation_id: str,
        conversation: Conversation,  # noqa: ARG003
    ) -> ConversationDTO:
        """Transform a conversation domain model into a DTO."""
        return cls(
            user_id=user_id,
            conversation_id=conversation_id,
        )
