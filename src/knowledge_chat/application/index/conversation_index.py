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


"""Provide an index for the conversation domain model."""

from __future__ import annotations

from uuid import NAMESPACE_URL, UUID, uuid5

from eventsourcing.domain import Aggregate


class ConversationIndex(Aggregate):
    """Define a conversation index."""

    class Created(Aggregate.Created):
        """Define the creation event."""

        user_id: str
        conversation_id: str
        reference: UUID

    def __init__(
        self,
        *,
        user_id: str,
        conversation_id: str,
        reference: UUID,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.reference = reference

    @classmethod
    def create_id(cls, user_id: str, conversation_id: str) -> UUID:
        """Return a universally unique namespace identifier (UUID)."""
        return uuid5(NAMESPACE_URL, f"/users/{user_id}/conversations/{conversation_id}")

    @classmethod
    def create(
        cls,
        *,
        user_id: str,
        conversation_id: str,
        reference: UUID,
    ) -> ConversationIndex:
        """Create a conversation index entry."""
        return cls._create(
            event_class=cls.Created,
            id=cls.create_id(user_id=user_id, conversation_id=conversation_id),
            user_id=user_id,
            conversation_id=conversation_id,
            reference=reference,
        )
