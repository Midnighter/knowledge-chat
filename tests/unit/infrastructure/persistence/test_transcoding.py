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


"""Test the transcodings for the persistence module."""

from datetime import timedelta

import pytest

from knowledge_chat.infrastructure.persistence.transcoding import TimedeltaAsDict


@pytest.mark.parametrize("seconds", [400_000.24, 0.0000006, 1.002])
def test_timedelta_as_dict(seconds: float):
    """Test that a timedelta is correctly transccoded."""
    transcoding = TimedeltaAsDict()
    original = timedelta(seconds=seconds)

    data = transcoding.encode(original)
    copy = transcoding.decode(data)

    assert copy == original
