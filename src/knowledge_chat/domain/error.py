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


class KnowledgeChatError(Exception):
    """Define the basic knowledge-chat error."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class UserNotFoundError(KnowledgeChatError):
    """Define the error raised when a requested user is not found."""

    def __init__(self, *, user_id: str, message: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user_id = user_id
        if message is None:
            self.message = f"The requested user '/users/{user_id}' does not exist."
        else:
            self.message = message


class ConversationNotFoundError(KnowledgeChatError):
    """Define the error raised when a requested conversation is not found."""

    def __init__(
        self,
        *,
        user_id: str,
        conversation_id: str,
        message: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.user_id = user_id
        self.conversation_id = conversation_id
        if message is None:
            self.message = (
                f"The requested conversation '/users/{user_id}/conversations/"
                f"{conversation_id}' does not exist."
            )
        else:
            self.message = message
