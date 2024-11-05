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


"""Test the conversation aggregate."""

from uuid import UUID, uuid4

from knowledge_chat.domain.model import Conversation


def test_create():
    """Test that a conversation is correctly created."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    assert isinstance(conversation.id, UUID)
    assert conversation.user_reference == user_ref


def test_reconstruct():
    """Test that a conversation's state is reconstructed from its events."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    events = conversation.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], Conversation.Started)

    copy = events[0].mutate(None)
    assert copy.id == conversation.id
    assert copy.user_reference == conversation.user_reference
