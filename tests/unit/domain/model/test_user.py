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


"""Test the user aggregate."""

from uuid import UUID, uuid4

import pytest

from knowledge_chat.domain.model import User


@pytest.fixture
def user() -> User:
    """Return a user aggregate instance."""
    return User.create(
        user_id="numero uno",
        name="Richard Daniel Sanchez",
        email="rick@multiverse.brain",
    )


def test_create():
    """Test that a user is correctly created."""
    user = User.create(
        user_id="numero uno",
        name="Richard Daniel Sanchez",
        email="rick@multiverse.brain",
    )
    assert isinstance(user.id, UUID)
    assert user.name == "Richard Daniel Sanchez"
    assert user.email == "rick@multiverse.brain"


def test_add_conversation(user: User):
    """Test that a conversation reference can be added."""
    conversation_ref = uuid4()
    user.add_conversation(conversation_ref)
    assert len(list(user.conversation_references)) == 1


def test_reconstruct(user: User):
    """Test that a user's state is reconstructed from its events."""
    events = user.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], User.Created)

    copy = events[0].mutate(None)
    assert copy.id == user.id
    assert copy.name == user.name
    assert copy.email == user.email
