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


"""Provide knowledge-chat specific error classes."""

from uuid import UUID


class KnowledgeChatError(Exception):
    """Define the basic knowledge-chat error."""

    def __init__(self, *, message: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.message = message

    def __str__(self) -> str:
        """Return a string representation of the error."""
        return self.message


class NotFoundError(KnowledgeChatError):
    """Define the error raised when a requested aggregate is not found."""

    def __init__(self, *, uuid: UUID, message: str | None = None, **kwargs) -> None:
        if message is None:
            message = f"The requested aggregate '{uuid!s}' does not exist."
        super().__init__(message=message, **kwargs)
        self.uuid = uuid
