import queue
import re
import threading
from queue import Queue
from typing import Dict, NoReturn

import requests
from openai import OpenAI

from type_extensions import Function, Generation


def generator_agent_swarm_sqlite(
    client: OpenAI,
    content_id: int,
    agent_id: str,
    comm: Dict[str, Queue],
    gen_time_out: int,
    generator_fn: Function,
    generator_loop: Generation,
    **kwargs,
) -> NoReturn:
    """Generator agent with thread-safe connection to sqlite database

    Args:
        client (OpenAI): Client instance
        content_id (int): The ID of conetent to generate
        agent_id (str): Generator agent id
        comm (Dict[str, Queue]): Queues for communication between agents
        gen_time_out (int): Time out for the "cont_to_gen" queue
        generator_fn (Function): Generation function
        generator_loop (Generation): Generation loop

    Returns:
        NoReturn:
    """
    session = kwargs["Session"]()

    try:
        thread_name = threading.current_thread().name
        thread = client.beta.threads.create()

        try:
            msg_gen = comm.queues["cont_to_gen"].get(timeout=gen_time_out)

            message = client.beta.threads.messages.create(
                thread_id=thread.id, role="user", content=msg_gen
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=agent_id
            )

            message_content = message.content[0].text.value
            print(f"{thread_name} received message: {message_content}")

            content, url = generator_loop(client, thread.id, run.id, generator_fn)

            link = re.search("(?P<url>https?://[^\\s]+)", url).group("url")

            response_pre_process = requests.get(url)
            response = requests.get(link)
            response_post_process = requests.get(link.strip(")"))

            if response_pre_process.status_code == 200:
                image = kwargs["Gen-Table"](url=link, data=response_pre_process.content)

                session.add(image)
                session.commit()
            elif response.status_code == 200:
                image = kwargs["Gen-Table"](url=link, data=response.content)

                session.add(image)
                session.commit()
            elif response_post_process.status_code == 200:
                image = kwargs["Gen-Table"](
                    url=link, data=response_post_process.content
                )

                session.add(image)
                session.commit()
            else:
                print(f"image url: {url} not found for {content_id}")
                print(f"the completed results is: {content}")
        except queue.Empty:
            pass
        comm.queues["cont_to_gen"].task_done()
    except:
        session.rollback()
        raise
    finally:
        session.close()
