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


"""Provide an abstract interface for the domain service registry."""

from eventsourcing.utils import resolve_topic
from langchain.prompts.prompt import PromptTemplate
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.language_models.chat_models import BaseChatModel

from knowledge_chat.application.dto import Neo4jSettings
from knowledge_chat.domain.service import DomainServiceRegistry, ResponseAgent


class LangchainDomainServiceRegistry(DomainServiceRegistry):
    """Define the abstract interface for the domain service registry."""

    def create_knowledge_graph(
        self,
        knowledge_graph_settings: Neo4jSettings,
    ) -> Neo4jGraph:
        """Return a knowledge graph service instance with a langchain interface."""
        return Neo4jGraph(
            url=str(knowledge_graph_settings.connection_uri),
            username=knowledge_graph_settings.username,
            password=knowledge_graph_settings.password.get_secret_value(),
            database=knowledge_graph_settings.database,
            timeout=knowledge_graph_settings.timeout,
            enhanced_schema=True,
        )

    def get_response_agent(
        self,
        agent_topic: str,
        knowledge_graph: Neo4jGraph,
        chat_model: BaseChatModel,
        custom_prompt: str | None = None,
        **kwargs,
    ) -> ResponseAgent:
        """Return a fully configured response agent."""
        agent_cls: type[ResponseAgent] = resolve_topic(agent_topic)

        prompt: PromptTemplate | None = None
        if custom_prompt is not None:
            prompt = PromptTemplate(
                input_variables=["schema", "query"],
                template=custom_prompt,
            )

        return agent_cls(
            chain=GraphCypherQAChain.from_llm(
                llm=chat_model,
                graph=knowledge_graph,
                verbose=True,
                cypher_prompt=prompt,
                return_intermediate_steps=True,
                validate_cypher=True,
                allow_dangerous_requests=True,
                **kwargs,
            ),
        )
