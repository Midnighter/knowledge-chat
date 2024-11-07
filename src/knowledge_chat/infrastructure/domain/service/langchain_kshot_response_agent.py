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


"""Provide a concrete chat agent implementation using langchain."""

import structlog

from knowledge_chat.domain.model import Conversation, Response, Thought
from knowledge_chat.domain.service import ResponseAgent


logger = structlog.get_logger(__name__)


class LangchainKShotResponseAgent(ResponseAgent):
    """
    Define the concrete langchain response agent implementation.

    It is called k-shot because depending on the chain's embedded prompt, there may be
    zero or more examples available to the chat model.

    """

    def respond_to(
        self,
        conversation: Conversation,
        callbacks: list | None = None,
        **_,
    ) -> None:
        """Ask a question to the agent and return a response."""
        result = self._chain.invoke(
            # TODO (Moritz): Careful, this is a train wreck.  # noqa: FIX002, TD003
            {"query": conversation.latest_exchange.query.text},
            callbacks=callbacks,
        )
        logger.debug("LANGCHAIN_RESULT_GENERATED", result=result)
        assert len(result["intermediate_steps"]) == 2  # noqa: PLR2004, S101
        for obj in result["intermediate_steps"]:
            conversation.add_thought(Thought(content=obj))
        conversation.respond(Response(text=result["result"]))
