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


"""Provide a user data transfer object (DTO)."""

from __future__ import annotations

from typing import NamedTuple

from knowledge_chat.domain.model import User


class UserDTO(NamedTuple):
    """Define the user data transfer object (DTO)."""

    user_id: str
    name: str
    email: str

    @classmethod
    def from_user(cls, user_id: str, user: User) -> UserDTO:
        """Transform a user domain model into a DTO."""
        return cls(
            user_id=user_id,
            name=user.name,
            email=user.email,
        )

    def create(self) -> User:
        """Create a new user instance."""
        return User(name=self.name, email=self.email)
