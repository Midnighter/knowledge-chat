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


"""Create a chainlit application for the example knowledge chat."""

from datetime import timedelta
from time import perf_counter
from uuid import UUID

import chainlit as cl
import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars

from knowledge_chat.application import UserDTO
from knowledge_chat.domain.error import NotFoundError
from knowledge_chat.infrastructure.application import KnowledgeChat
from knowledge_chat.infrastructure.domain.service import LangchainDomainServiceRegistry
from knowledge_chat.infrastructure.settings.agent_settings import AgentSettings
from knowledge_chat.infrastructure.settings.neo4j_settings import Neo4jSettings
from knowledge_chat.infrastructure.settings.ollama_settings import OllamaSettings


logger = structlog.get_logger()
agent_settings = AgentSettings.create()
neo4j_settings = Neo4jSettings.create()
ollama_settings = OllamaSettings.create()
chat_app = KnowledgeChat(
    domain_service_registry=LangchainDomainServiceRegistry(),
    knowledge_graph=neo4j_settings.create_graph(),
    chat_model=ollama_settings.create_model(),
    agent_settings=agent_settings,
)


@cl.on_chat_start
def init() -> None:
    """Initialize the user and chat."""
    logger.debug("CHAINLIT_ON_CHAT_STARTED")

    start = perf_counter()
    # We use the session ID as the user identifier.
    user_id = cl.user_session.get("id")
    clear_contextvars()
    bind_contextvars(user_id=user_id)

    try:
        chat_app.get_user(user_id)
        logger.debug("EXISTING_USER_RESTORED")
    except NotFoundError:
        chat_app.create_user(
            UserDTO(user_id=user_id, name="anon", email="anon@me"),
        )
        logger.debug("NEW_USER_CREATED")

    try:
        conversation_id = UUID(cl.user_session.get("conversation-id"))
        bind_contextvars(conversation_id=conversation_id)
        logger.debug("EXISTING_CONVERSATION_RESTORED")
    except TypeError:
        conversation_id = chat_app.start_conversation(user_id)
        bind_contextvars(conversation_id=conversation_id)
        cl.user_session.set("conversation-id", str(conversation_id))
        logger.debug("NEW_CONVERSATION_STARTED")

    logger.debug(
        "CHAINLIT_ON_CHAT_ENDED",
        duration=timedelta(seconds=perf_counter() - start),
    )


@cl.on_message
async def chat(message: cl.Message) -> None:
    """Chat with the user-specific agent."""
    start = perf_counter()

    # We use the session ID as the user identifier.
    user_id = cl.user_session.get("id")

    clear_contextvars()
    bind_contextvars(user_id=user_id)

    conversation_id = UUID(cl.user_session.get("conversation-id"))
    bind_contextvars(conversation_id=conversation_id)

    try:
        exchange = await cl.make_async(chat_app.respond_to)(
            query=message.content,
            conversation_id=conversation_id,
            callbacks=[cl.LangchainCallbackHandler()],
        )
    except Exception as error:
        await cl.Message(
            content="The bot ran into an error. Rephrase your query and try again.",
            elements=[cl.Text(name="Error", content=str(error))],
        ).send()
        raise
    await cl.Message(content=exchange.response).send()
    await logger.adebug(
        "MESSAGE_REPLIED",
        duration=timedelta(seconds=perf_counter() - start),
    )
