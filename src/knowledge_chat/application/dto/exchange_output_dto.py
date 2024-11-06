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


"""Provide an exchange output data transfer object (DTO)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from knowledge_chat.domain.model import Exchange


class ExchangeOutputDTO(BaseModel):
    """Define the exchange output data transfer object (DTO)."""

    query: str
    response: str

    @classmethod
    def from_exchange(cls, exchange: Exchange) -> ExchangeOutputDTO:
        """Transform an exchange object into a DTO object."""
        # We bypass model validation because we trust our data on the way out.
        return cls.model_construct(
            query=exchange.query.text,
            email=exchange.response.text,
        )
