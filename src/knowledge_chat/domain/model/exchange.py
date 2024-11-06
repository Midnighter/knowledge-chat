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


"""Provide an aggregate model for an exchange."""

from collections.abc import Iterable

from knowledge_chat.domain.error import KnowledgeChatError

from .query import Query
from .response import Response
from .thought import Thought


class Exchange:
    """
    Define an exchange.

    An exchange is part of a conversation. Essentially, it is the pair of query and
    response. Additionally, there may be any number of agent thoughts that connect the
    query and response.

    """

    def __init__(
        self,
        *,
        query: Query,
        thoughts: Iterable[Thought] | None = None,
        response: Response | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.query = query
        if thoughts is None:
            self._thoughts = []
        else:
            self._thoughts = list(thoughts)
        self.response = response

    @property
    def is_closed(self) -> bool:
        """Whether the exchange is closed, that means, it has a response."""
        return self.response is not None

    def get_last_thought(self) -> Thought:
        """Return the last thought."""
        if not self._thoughts:
            raise KnowledgeChatError(
                message="There are no thoughts part of this exchange.",
            )
        return self._thoughts[-1]

    def add_thought(self, thought: Thought) -> None:
        """Add another thought to the exchange."""
        if self.is_closed:
            raise KnowledgeChatError(message="This exchange is already closed.")

        if self._thoughts:
            thought = Thought(content=thought.content, parent=self._thoughts[-1])

        self._thoughts.append(thought)

    def close(self, response: Response) -> None:
        """Close the exchange by providing a response."""
        if self.is_closed:
            raise KnowledgeChatError(message="This exchange is already closed.")

        if not self._thoughts:
            msg = "No thoughts preceded this response."
            raise UserWarning(msg)

        self.response = response
