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


"""Test the thought value object."""

import pytest

from knowledge_chat.domain.model import Thought


def test_init_requires():
    """Test that creating a thought requires a sub-query and a context."""
    with pytest.raises(TypeError):
        Thought()


def test_init():
    """Test that a thought can be created with a sub-query and a context."""
    Thought(subquery="Who am I?", context={})


def test_add_parent():
    """Test that a thought can be added as a parent to another thought."""
    parent = Thought(subquery="Who are you?", context={})
    child = Thought(subquery="Who am I?", context={})
    copy = child.with_parent(parent)

    assert copy.parent == parent
    assert copy.subquery == child.subquery
    assert copy.context == child.context
