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

from collections.abc import Iterable
from uuid import UUID

from eventsourcing.domain import Aggregate, event


class User(Aggregate):
    """Define the user class."""

    class Created(Aggregate.Created):
        """Define the user creation event."""

        name: str
        email: str

    @event(Created)
    def __init__(self, *, name: str, email: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self._conversation_references = []

    @event("ConversationAdded")
    def add_conversation(self, conversation_reference: UUID) -> None:
        """Add a reference to a conversation this user is having."""
        self._conversation_references.append(conversation_reference)

    @property
    def conversation_references(self) -> Iterable[UUID]:
        """Return iterable conversation references."""
        return iter(self._conversation_references)
