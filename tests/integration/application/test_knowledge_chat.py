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


"""Test the expected functionality of the knowledge chat application."""

import pytest

from knowledge_chat.application import KnowledgeChat
from knowledge_chat.application.dto import ConversationDTO, UserDTO


@pytest.fixture
def application() -> KnowledgeChat:
    """Return an application instance per test unit."""
    return KnowledgeChat()


@pytest.mark.parametrize(
    "user",
    [
        UserDTO(
            name="Richard Daniel Sanchez",
            email="rick@multiverse.brain",
        ),
    ],
)
def test_create_get_user(user: UserDTO, application: KnowledgeChat):
    """Test that a user can be created and retrieved."""
    user_id = application.create_user(user=user)
    result = application.get_user(user_id=user_id)
    assert result == user


@pytest.mark.parametrize(
    "user",
    [
        UserDTO(
            name="Richard Daniel Sanchez",
            email="rick@multiverse.brain",
        ),
    ],
)
def test_start_get_conversation(user: UserDTO, application: KnowledgeChat):
    """Test that a user can be created and retrieved."""
    user_id = application.create_user(user=user)
    conversation_id = application.start_conversation(user_id=user_id)
    notifications = application.notification_log.select(start=0, limit=10)
    assert len(notifications) == 3

    result = application.get_conversation(conversation_id=conversation_id)
    assert result == ConversationDTO()
