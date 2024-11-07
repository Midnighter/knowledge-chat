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


"""Test the exchange aggregate."""

import pytest

from knowledge_chat.domain.error import KnowledgeChatError
from knowledge_chat.domain.model import Exchange, Query, Response, Thought


def test_init_requires_query():
    """Test that creating an exchange requires a query."""
    with pytest.raises(TypeError):
        Exchange()


def test_init():
    """Test that an exchange can be created with a query."""
    Exchange(query=Query(text="What gives?"))


def test_add_thought():
    """Test that a thought can be added to an open exchange."""
    exchange = Exchange(query=Query(text="What gives?"))
    exchange.add_thought(Thought(subquery="provocation", context="cogito, ergo sum"))


def test_no_latest_thought():
    """Test that there is no thought without adding one."""
    exchange = Exchange(query=Query(text="What gives?"))

    assert exchange.lastest_thought is None


def test_thought_lineage():
    """Test that a thought has a parent set."""
    exchange = Exchange(query=Query(text="What gives?"))
    exchange.add_thought(Thought(subquery="provocation", context="first"))
    exchange.add_thought(Thought(subquery="provocation", context="second"))

    # TODO (Moritz): Train wreck?  # noqa: FIX002, TD003
    assert exchange.lastest_thought.parent.context == "first"


def test_close():
    """Test that a response closes an exchange."""
    exchange = Exchange(query=Query(text="What gives?"))
    exchange.add_thought(Thought(subquery="provocation", context="first"))
    exchange.close(Response(text="Therefore."))

    assert exchange.is_closed


def test_close_without_thought():
    """Test that closing an exchange without thoughts emits a warning."""
    exchange = Exchange(query=Query(text="What gives?"))
    with pytest.warns(UserWarning):
        exchange.close(Response(text="Accept it."))


def test_cannot_add_thought():
    """Test that a thought cannot be added to a closed exchange."""
    exchange = Exchange(query=Query(text="What gives?"))
    exchange.add_thought(Thought(subquery="provocation", context="first"))
    exchange.close(Response(text="Therefore."))

    with pytest.raises(KnowledgeChatError):
        exchange.add_thought(Thought(subquery="provocation", context="second"))


def test_cannot_respond_twice():
    """Test that a closed exchange cannot be responded to."""
    exchange = Exchange(query=Query(text="What gives?"))
    exchange.add_thought(Thought(subquery="provocation", context="first"))
    exchange.close(Response(text="Therefore."))

    with pytest.raises(KnowledgeChatError):
        exchange.close(Response(text="Oh no!"))
