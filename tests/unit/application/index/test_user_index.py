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


"""Test the user index."""

from uuid import UUID, uuid4

from knowledge_chat.application.index import UserIndex


def test_create_id():
    """Test that the user index creates a universally unique identifier (UUID)."""
    assert isinstance(UserIndex.create_id("1234"), UUID)


def test_create():
    """Test that a user index entry is correctly created."""
    user_id = "1234"
    ref = uuid4()
    index = UserIndex.create(user_id=user_id, reference=ref)
    assert index.id == UserIndex.create_id(user_id)
    assert index.reference == ref
