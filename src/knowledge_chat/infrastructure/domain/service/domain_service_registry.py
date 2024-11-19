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

from knowledge_chat.domain.service import DomainServiceRegistry, ResponseAgent
from knowledge_chat.infrastructure.settings.agent_settings import AgentSettings


class LangchainDomainServiceRegistry(DomainServiceRegistry):
    """Define the abstract interface for the domain service registry."""

    def get_response_agent(
        self,
        agent_settings: AgentSettings,
        knowledge_graph: Neo4jGraph,
        chat_model: BaseChatModel,
        **kwargs,
    ) -> ResponseAgent:
        """Return a fully configured response agent."""
        agent_cls: type[ResponseAgent] = resolve_topic(agent_settings.topic)

        prompt: PromptTemplate | None = None
        if agent_settings.prompt is not None:
            prompt = PromptTemplate(
                input_variables=["schema", "query"],
                template=agent_settings.prompt,
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
