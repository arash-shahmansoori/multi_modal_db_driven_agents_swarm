import subprocess
from typing import NoReturn

import openai
from openai import OpenAI


def remove_agents(client: OpenAI, limits: int) -> NoReturn:
    """Remove agents

    Args:
        client (OpenAI): OpenAI LLM
        limits (int): Max number of agents to be removed

    Returns:
        NoReturn: No return
    """
    max_limits = 100
    limit = max_limits if limits >= max_limits else limits

    if len(client.beta.assistants.list(limit=limit).data) == 0:
        print("There is no more agents to delete.")

    try:
        for assistant in client.beta.assistants.list(limit=limit):
            if assistant.id:
                client.beta.assistants.delete(assistant.id)
                print(f"Assistant {assistant.id} deleted.")
    except openai.NotFoundError:
        print("There are no more agents to remove.")


def remove_agents_ids(agents_ids_path: str) -> NoReturn:
    r = subprocess.run(["rm", "-rf", agents_ids_path], capture_output=True, text=True)
