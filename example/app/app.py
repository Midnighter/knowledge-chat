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

from uuid import UUID

import chainlit as cl
import structlog

from knowledge_chat.application import KnowledgeChat, UserDTO
from knowledge_chat.infrastructure.domain.service import LangchainDomainServiceRegistry
from knowledge_chat.infrastructure.settings import Neo4jSettings, OllamaSettings


logger = structlog.get_logger()
neo4j_settings = Neo4jSettings.create()
ollama_settings = OllamaSettings.create()
chat_app = KnowledgeChat(
    domain_service_registry=LangchainDomainServiceRegistry(),
    knowledge_graph=neo4j_settings.create_graph(),
    chat_model=ollama_settings.create_model(),
)


@cl.on_chat_start
def init() -> None:
    """Initialize the user and chat."""
    logger.debug("CHAINLIT_ON_CHAT_STARTED")

    try:
        user_id = UUID(cl.user_session.get("user-id", None))
    except TypeError:
        user_id = chat_app.create_user(UserDTO(name="anon", email="anon@me"))
        cl.user_session.set("user-id", str(user_id))

    try:
        conversation_id = UUID(cl.user_session.get("conversation-id"))
    except TypeError:
        conversation_id = chat_app.start_conversation(user_id)
        cl.user_session.set("conversation-id", str(conversation_id))

    logger.debug("CHAINLIT_ON_CHAT_ENDED")


@cl.on_message
async def chat(message: cl.Message) -> None:
    """Chat with the user-specific agent."""
    conversation_id = UUID(cl.user_session.get("conversation-id"))

    async_respond_to = cl.make_async(chat_app.respond_to)
    exchange = await async_respond_to(
        query=message.content,
        conversation_id=conversation_id,
    )
    await cl.Message(content=exchange.response).send()
