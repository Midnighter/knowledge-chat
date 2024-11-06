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


"""Test the error classes."""

from uuid import uuid4

from knowledge_chat.domain.error import KnowledgeChatError, NotFoundError


def test_basic_error():
    """Test that a basic error can be initialized and represented as a string."""
    msg = "This is not a test."
    error = KnowledgeChatError(message=msg)

    assert str(error) == msg


def test_default_not_found_error():
    """Test that a not found error can be raised only with a UUID."""
    uuid = uuid4()
    error = NotFoundError(uuid=uuid)

    assert isinstance(error, KnowledgeChatError)
    assert str(uuid) in str(error)


def test_custom_not_found_error():
    """Test that a not found error can be raised with a custom message."""
    uuid = uuid4()
    msg = "This is not a test."
    error = NotFoundError(uuid=uuid, message=msg)

    assert isinstance(error, KnowledgeChatError)
    assert str(error) == msg
    assert error.uuid == uuid
