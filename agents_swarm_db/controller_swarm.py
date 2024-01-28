import threading
from queue import Queue
from typing import Dict, NoReturn

from asteval import Interpreter
from openai import OpenAI

from type_extensions import Control, Generation


def controller_agent_swarm(
    client: OpenAI,
    agent_id: str,
    subject: str,
    msg_cont: str,
    thread_count_gen: int,
    comm: Dict[str, Queue],
    gen_image_user_prompt: Generation,
    controller_loop: Control,
) -> NoReturn:
    """Controller agent

    Args:
        client (OpenAI): Client instance
        agent_id (str): Controller agent id
        subject (str): The subject of content to be generated
        msg_cont (str): The task message to the controller
        comm (Dict[str, Queue]): Queues for communication between agents
        gen_image_user_prompt (Generation): Callable for generation user prompt
        controller_loop (Control): Control loop function

    Returns:
        NoReturn:
    """
    thread_name = threading.current_thread().name
    thread = client.beta.threads.create()

    user_prompt = msg_cont

    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_prompt
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=agent_id)

    message_content = message.content[0].text.value
    print(f"{thread_name} received message: {message_content}")

    response = controller_loop(client, thread.id, run.id)
    aeval = Interpreter()

    try:
        cont_msg = aeval(response)

        for k, _ in cont_msg.items():
            if k == "gen":
                gen_user_prompt = gen_image_user_prompt(subject)
                for _ in range(thread_count_gen):
                    comm.queues["cont_to_gen"].put(gen_user_prompt)

    except AttributeError as e:
        print(f"The following error occured: {e}")
