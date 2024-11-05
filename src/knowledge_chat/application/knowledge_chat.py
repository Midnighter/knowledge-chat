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

from eventsourcing.application import Application

from knowledge_chat.domain.model import User

from .dto import UserDTO
from .index import UserIndex


class KnowledgeChat(Application):
    """Define the knowledge chat application."""

    def create_user(self, user: UserDTO) -> None:
        """Create a new user instance and persist it."""
        domain_user = User(name=user.name, email=user.email)
        index = UserIndex.create(user_id=user.user_id, reference=domain_user.id)
        self.save(domain_user, index)

    def _get_user(self, user_id: str) -> User:
        """Get a user's state by their external identifier."""
        index: UserIndex = self.repository.get(UserIndex.create_id(user_id=user_id))
        return self.repository.get(index.reference)

    def get_user(self, user_id: str) -> UserDTO:
        """Get user data by their external identifier."""
        user = self._get_user(user_id)
        return UserDTO(user_id=user_id, name=user.name, email=user.email)
