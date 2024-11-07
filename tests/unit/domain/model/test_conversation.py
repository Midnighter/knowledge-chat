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

import pytest

from knowledge_chat.domain.error import KnowledgeChatError
from knowledge_chat.domain.model import Conversation, Query, Response, Thought


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


def test_no_latest_exchange():
    """Test that there is no exchange without adding one."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)

    assert conversation.latest_exchange is None


def test_raise_query():
    """Test that a new query can be raised on a fresh conversation."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    conversation.raise_query(Query(text="Me first?"))

    assert isinstance(conversation.collect_events()[-1], Conversation.QueryRaised)
    assert conversation.latest_exchange is not None


def test_cannot_query_twice():
    """Test that a new query cannot be raised on an open exchange."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    conversation.raise_query(Query(text="Me first?"))

    with pytest.raises(KnowledgeChatError):
        conversation.raise_query(Query(text="Who is second?"))


def test_add_thought():
    """Test that a new thought can be added to an open exchange."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    conversation.raise_query(Query(text="Me first?"))
    conversation.add_thought(Thought(subquery="Where am I?", context="You are here."))

    assert isinstance(conversation.collect_events()[-1], Conversation.ThoughtAdded)
    # TODO (Moritz): Train wreck?  # noqa: FIX002, TD003
    assert conversation.latest_exchange.lastest_thought.subquery == "Where am I?"
    assert conversation.latest_exchange.lastest_thought.context == "You are here."


def test_cannot_add_thought_without_exchange():
    """Test that a new thought cannot be added without an exchange."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)

    with pytest.raises(KnowledgeChatError):
        conversation.add_thought(
            Thought(subquery="Where am I?", context="You are here."),
        )


def test_respond():
    """Test that an open exchange can be responded to."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    conversation.raise_query(Query(text="Me first?"))
    conversation.add_thought(Thought(subquery="Where am I?", context="You are here."))
    conversation.respond(Response("Because!"))

    assert isinstance(conversation.collect_events()[-1], Conversation.QueryRespondedTo)
    assert conversation.latest_exchange.is_closed


def test_cannot_respond_without_exchange():
    """Test that a response cannot be added without an exchange."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)

    with pytest.raises(KnowledgeChatError):
        conversation.respond(Response("Doh!"))


def test_cannot_add_thought_on_closed():
    """Test that a new thought cannot be added to a closed exchange."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    conversation.raise_query(Query(text="Me first?"))
    conversation.add_thought(Thought(subquery="Where am I?", context="You are here."))
    conversation.respond(Response("Because!"))

    with pytest.raises(KnowledgeChatError):
        conversation.add_thought(
            Thought(subquery="Where am I?", context="You are here."),
        )


def test_cannot_respond_twice():
    """Test that a closed exchange cannot be responded to."""
    user_ref = uuid4()
    conversation = Conversation(user_reference=user_ref)
    conversation.raise_query(Query(text="Me first?"))
    conversation.add_thought(Thought(subquery="Where am I?", context="You are here."))
    conversation.respond(Response("Because!"))

    with pytest.raises(KnowledgeChatError):
        conversation.respond(Response("Really?!"))
