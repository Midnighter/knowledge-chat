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


"""Test the conversation index."""

from uuid import UUID, uuid4

from knowledge_chat.application.index import ConversationIndex


def test_create_id():
    """Test that the conversation index creates a UUID."""
    assert isinstance(ConversationIndex.create_id("1234", "5678"), UUID)


def test_create():
    """Test that a conversation index entry is correctly created."""
    user_id = "1234"
    conversation_id = "5678"
    ref = uuid4()
    index = ConversationIndex.create(
        user_id=user_id,
        conversation_id=conversation_id,
        reference=ref,
    )
    assert index.id == ConversationIndex.create_id(user_id, conversation_id)
    assert index.reference == ref
