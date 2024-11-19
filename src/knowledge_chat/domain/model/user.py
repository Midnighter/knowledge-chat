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


"""Provide a user aggregate root domain model."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import NAMESPACE_URL, UUID, uuid5

from eventsourcing.domain import Aggregate, event


if TYPE_CHECKING:
    from collections.abc import Iterable


class User(Aggregate):
    """Define the user class."""

    def __init__(self, *, user_id: str, name: str, email: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user_id = user_id
        self.name = name
        self.email = email
        self._conversation_references: list[UUID] = []

    class Created(Aggregate.Created):
        """Define the user creation event."""

        user_id: str
        name: str
        email: str

    @classmethod
    def create_id(cls, user_id: str) -> UUID:
        """Return an internal UUID for an external user identifier."""
        return uuid5(NAMESPACE_URL, f"/users/{user_id}")

    @classmethod
    def create(cls, *, user_id: str, name: str, email: str, **kwargs) -> User:
        """Create a new user instance."""
        return cls._create(
            event_class=cls.Created,
            id=cls.create_id(user_id),
            user_id=user_id,
            name=name,
            email=email,
            **kwargs,
        )

    @event("ConversationAdded")
    def add_conversation(self, conversation_reference: UUID) -> None:
        """Add a reference to a conversation this user is having."""
        self._conversation_references.append(conversation_reference)

    @property
    def conversation_references(self) -> Iterable[UUID]:
        """Return iterable conversation references."""
        return iter(self._conversation_references)
