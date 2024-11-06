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


"""Test the user DTO."""

from knowledge_chat.application.dto import UserDTO
from knowledge_chat.domain.model import User


def test_create():
    """Test that the user instance created by the DTO is valid."""
    dto = UserDTO(name="Richard Daniel Sanchez", email="rick@multiverse.brain")
    user = dto.create()
    assert isinstance(user, User)
    assert user.name == dto.name
    assert user.email == dto.email


def test_from_user():
    """Test that a DTO created from a user is valid."""
    user = User(name="Richard Daniel Sanchez", email="rick@multiverse.brain")
    dto = UserDTO.from_user(user=user)
    assert isinstance(dto, UserDTO)
    assert dto.name == user.name
    assert dto.email == user.email
