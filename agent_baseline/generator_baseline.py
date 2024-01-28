from typing import Dict, NoReturn

from openai import OpenAI

from type_extensions import Function, Generation, T


def generator_agent_baseline(
    client: OpenAI,
    system_prompt: str,
    usr_prompt: str,
    generator_fn: Function,
    generator_loop: Generation,
    **create_params: Dict[str, T],
) -> NoReturn:
    """Baseline generator agent

    Args:
        client (OpenAI): Client instance
        system_prompt (str): System prompt for generator agent
        usr_prompt (str): User prompt for generator agent
        generator_fn (Function): Generation function
        generator_loop (Generation): Generation loop

    Returns:
        NoReturn:
    """

    assistant = client.beta.assistants.create(
        instructions=system_prompt, **create_params
    )
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=usr_prompt
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant.id
    )

    message_content = message.content[0].text.value
    print(f"Received message: {message_content}")

    response = generator_loop(client, thread.id, run.id, generator_fn)

    print(response)
