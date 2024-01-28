from typing import List, Tuple

from openai import OpenAI
from openai.types.beta import Assistant


def agent_builder(
    client: OpenAI, system_prompt: str, num_agent: int, **create_params
) -> Tuple[List[Assistant], Assistant]:
    """Build agent

    Args:
        client (OpenAI): Client instance
        system_prompt (str): System prompt for generator agent
        num_agent (int): Number of agents to build

    Returns:
        Tuple[List[Assistant], Assistant]: Initialized list of agents and a single agent
    """
    agents = []
    for _ in range(num_agent):
        # Initialize agent
        agent = client.beta.assistants.create(
            instructions=system_prompt, **create_params
        )
        agents.append(agent)

    return agents, agent
