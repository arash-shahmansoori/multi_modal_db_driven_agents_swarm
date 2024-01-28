from openai import OpenAI


def agent_loop(client: OpenAI, thread_id: str, run_id: str) -> str:
    """The loop for the agent

    Args:
        client (OpenAI): Client instance
        thread_id (str): Thread Id for the agent
        run_id (str): Run Id for the agent

    Returns:
        str: Response from the analyzer agent
    """
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        if run.status == "completed":
            message = client.beta.threads.messages.list(thread_id=thread_id)
            for datum in message.data:
                for content in datum.content:
                    return content.text.value
