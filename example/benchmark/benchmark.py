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


"""
Provide extremely simple benchmarking.

Should be moved into the test suite.

"""

from datetime import timedelta
from time import perf_counter

import structlog
from humanize import precisedelta

from knowledge_chat.domain.model import Conversation, Query
from knowledge_chat.infrastructure.domain.service import LangchainDomainServiceRegistry
from knowledge_chat.infrastructure.settings.neo4j_settings import Neo4jSettings
from knowledge_chat.infrastructure.settings.ollama_settings import OllamaSettings


logger = structlog.get_logger()


def main() -> None:
    """Run benchmarks."""
    neo4j_settings = Neo4jSettings.create()
    ollama_settings = OllamaSettings.create()
    service_registry = LangchainDomainServiceRegistry()

    start = perf_counter()
    model = ollama_settings.create_model()
    duration = timedelta(seconds=perf_counter() - start)
    logger.info(
        "MODEL_INTERFACE_CREATED",
        duration=precisedelta(duration, minimum_unit="microseconds", format="%0.3f"),
    )

    start = perf_counter()
    graph = neo4j_settings.create_graph()
    duration = timedelta(seconds=perf_counter() - start)
    logger.info(
        "GRAPH_INTERFACE_CREATED",
        duration=precisedelta(duration, minimum_unit="microseconds", format="%0.3f"),
    )

    start = perf_counter()
    agent = service_registry.get_response_agent(
        "knowledge_chat.infrastructure.domain.service:LangchainKShotResponseAgent",
        graph,
        model,
    )
    duration = timedelta(seconds=perf_counter() - start)
    logger.info(
        "AGENT_CREATED",
        duration=precisedelta(duration, minimum_unit="microseconds", format="%0.3f"),
    )

    convo = Conversation(user_reference=None)

    convo.raise_query(
        Query(
            text="What is the name of the person who acted in the least number of "
            "movies?",
        ),
    )
    start = perf_counter()
    agent.generate_response(convo)
    duration = timedelta(seconds=perf_counter() - start)
    logger.info(
        "RESPONSE_GENERATED",
        duration=precisedelta(duration, minimum_unit="microseconds", format="%0.3f"),
    )

    convo.raise_query(
        Query(
            text="What is the name of the person who acted in the least number of "
            "movies?",
        ),
    )
    start = perf_counter()
    agent.generate_response(convo)
    duration = timedelta(seconds=perf_counter() - start)
    logger.info(
        "RESPONSE_GENERATED",
        duration=precisedelta(duration, minimum_unit="microseconds", format="%0.3f"),
    )


if __name__ == "__main__":
    main()
