import json

# from json import JSONDecodeError
from typing import Dict, NoReturn

from openai import OpenAI

from type_extensions import Analysis, Function, T


def analyzer_agent_baseline(
    client: OpenAI,
    system_prompt: str,
    usr_prompt: str,
    file_name: str,
    analyzer_fn: Function,
    analyzer_loop: Analysis,
    **create_params: Dict[str, T],
) -> NoReturn:
    """Baseline generator agent

    Args:
        client (OpenAI): Client instance
        system_prompt (str): System prompt for generator agent
        usr_prompt (str): User prompt for generator agent
        file_name (str): File name to analyze
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

    response = analyzer_loop(client, thread.id, run.id, analyzer_fn)

    # try:
    #     resp = json.loads(response)
    #     final_resp = resp | {"file_name": file_name}
    # except JSONDecodeError as e:
    #     print(f"JSON decoder error {e} occured.")

    #     final_resp = {response} | {"file_name": file_name}

    final_resp = {"response": f"{response}"} | {"file_name": file_name}

    # Store the JSON data in a file
    with open(f"data/analysis/anlys_{file_name}.json", "w") as file:
        json.dump(final_resp, file)

        print(f"Analysis stored for {file_name} successfully.")
