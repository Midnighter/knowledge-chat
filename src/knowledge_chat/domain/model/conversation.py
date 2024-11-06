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

from knowledge_chat.domain.error import KnowledgeChatError

from . import Thought
from .exchange import Exchange
from .query import Query
from .response import Response


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

    @property
    def latest_exchange(self) -> Exchange | None:
        """Return the latest exchange of this conversation if any."""
        if not self._exchanges:
            return None

        return self._exchanges[-1]

    class QueryRaised(Aggregate.Event):
        """Define the event when a new query was raised."""

        query: Query

    @event(QueryRaised)
    def raise_query(self, query: Query) -> None:
        """
        Raise a new query.

        We expect well conducted conversations where each query is responded to before
        proceeding to the next exchange.

        """
        if self._exchanges and not self.latest_exchange.is_closed:
            raise KnowledgeChatError(message="The latest exchange was never closed.")

        self._exchanges.append(Exchange(query=query))

    class ThoughtAdded(Aggregate.Event):
        """Define the event when a new thought was added."""

        thought: Thought

    @event(ThoughtAdded)
    def add_thought(self, thought: Thought) -> None:
        """Add a new thought."""
        if not self._exchanges:
            raise KnowledgeChatError(
                message="There is no exchange; raise a query first.",
            )

        if self._exchanges and self.latest_exchange.is_closed:
            raise KnowledgeChatError(message="The latest exchange is already closed.")

        self.latest_exchange.add_thought(thought)

    class QueryRespondedTo(Aggregate.Event):
        """Define the event when a response was added."""

        response: Response

    @event(QueryRespondedTo)
    def respond(self, response: Response) -> None:
        """Add a new thought."""
        if not self._exchanges:
            raise KnowledgeChatError(
                message="There is no exchange; raise a query first.",
            )

        if self._exchanges and self.latest_exchange.is_closed:
            raise KnowledgeChatError(message="The latest exchange is already closed.")

        self.latest_exchange.close(response)
