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


"""Provide the knowledge chat application."""

from uuid import UUID

from eventsourcing.application import AggregateNotFoundError, Application

from knowledge_chat.domain.error import NotFoundError
from knowledge_chat.domain.model import Conversation, User

from .dto import ConversationDTO, UserDTO


class KnowledgeChat(Application):
    """Define the knowledge chat application."""

    def create_user(self, user: UserDTO) -> UUID:
        """Create a new user instance and persist it."""
        domain_user = user.create()
        self.save(domain_user)
        return domain_user.id

    def _get_user(self, user_id: UUID) -> User:
        """Get a user's state by their identifier."""
        try:
            result: User = self.repository.get(user_id)
        except AggregateNotFoundError as error:
            raise NotFoundError(uuid=user_id) from error

        return result

    def get_user(self, user_id: UUID) -> UserDTO:
        """Get user data by their identifier."""
        user = self._get_user(user_id)
        return UserDTO.from_user(user=user)

    def start_conversation(self, user_id: UUID) -> UUID:
        """Add a new conversation to the user."""
        user = self._get_user(user_id)
        conversation = Conversation(user_reference=user.id)
        user.add_conversation(conversation_reference=conversation.id)
        self.save(user, conversation)
        return conversation.id

    def _get_conversation(self, conversation_id: UUID) -> Conversation:
        """Get a conversation's state by its identifier."""
        try:
            result: Conversation = self.repository.get(conversation_id)
        except AggregateNotFoundError as error:
            raise NotFoundError(uuid=conversation_id) from error

        return result

    def get_conversation(self, conversation_id: UUID) -> ConversationDTO:
        """Get conversation data by its identifier."""
        conversation = self._get_conversation(conversation_id)
        return ConversationDTO.from_conversation(conversation=conversation)
