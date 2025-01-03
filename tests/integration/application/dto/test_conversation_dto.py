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


"""Test the conversation DTO."""

from uuid import uuid4

from knowledge_chat.application.dto import ConversationDTO
from knowledge_chat.domain.model import Conversation


def test_from_conversation():
    """Test that a DTO created from a conversation is valid."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    dto = ConversationDTO.from_conversation(conversation=conversation)
    assert isinstance(dto, ConversationDTO)
