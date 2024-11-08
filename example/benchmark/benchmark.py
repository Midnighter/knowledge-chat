from datetime import timedelta
from time import perf_counter

import structlog
from humanize import precisedelta

from knowledge_chat.domain.model import Conversation, Query
from knowledge_chat.infrastructure.domain.service import LangchainDomainServiceRegistry
from knowledge_chat.infrastructure.settings.neo4j_settings import Neo4jSettings
from knowledge_chat.infrastructure.settings.ollama_settings import OllamaSettings


logger = structlog.get_logger()


def main():
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
            text="What is the name of the person who acted in the least number of movies?",
        ),
    )
    start = perf_counter()
    agent.respond_to(convo)
    duration = timedelta(seconds=perf_counter() - start)
    logger.info(
        "RESPONSE_GENERATED",
        duration=precisedelta(duration, minimum_unit="microseconds", format="%0.3f"),
    )

    convo.raise_query(
        Query(
            text="What is the name of the person who acted in the least number of movies?",
        ),
    )
    start = perf_counter()
    agent.respond_to(convo)
    duration = timedelta(seconds=perf_counter() - start)
    logger.info(
        "RESPONSE_GENERATED",
        duration=precisedelta(duration, minimum_unit="microseconds", format="%0.3f"),
    )


if __name__ == "__main__":
    main()
