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


"""Provide a conversation aggregate."""

from uuid import UUID

from eventsourcing.domain import Aggregate, event


class Conversation(Aggregate):
    """Define the conversation aggregate."""

    class Started(Aggregate.Created):
        """Define the conversation creation event."""

        user_reference: UUID

    @event(Started)
    def __init__(self, *, user_reference: UUID, **kwargs) -> None:
        super().__init__(**kwargs)
        self._user_reference = user_reference
        self._exchanges = []

    @property
    def user_reference(self) -> UUID:
        """Return the reference to the user having this conversation."""
        return self._user_reference
