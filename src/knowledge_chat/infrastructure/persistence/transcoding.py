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


"""Provide transcoding for custom data types."""

from datetime import timedelta

from eventsourcing.persistence import Transcoding


class TimedeltaAsDict(Transcoding):
    """Provide transcoding for a timedelta as a dictionary."""

    type = timedelta
    name = "timedelta"

    def encode(self, obj: timedelta) -> dict:
        """Encode a timedelta as a dictionary."""
        return {
            "days": obj.days,
            "seconds": obj.seconds,
            "microseconds": obj.microseconds,
        }

    def decode(self, data: dict) -> timedelta:
        """Decode a dictionary as a timedelta."""
        return timedelta(**data)
