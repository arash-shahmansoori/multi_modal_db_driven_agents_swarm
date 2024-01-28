import re
import threading
from queue import Queue
from typing import Dict, NoReturn

from openai import OpenAI

from type_extensions import Analysis, Function


def analyzer_agent_swarm_s3(
    client: OpenAI,
    content_id: int,
    agent_id: str,
    subject: str,
    comm: Dict[str, Queue],
    anlys_image_user_prompt: Analysis,
    analyzer_fn: Function,
    analyzer_loop: Analysis,
    **kwargs,
) -> NoReturn:
    """Analyzer agent with connection to s3 bucket

    Args:
        client (OpenAI): Client instance
        path_gen (str): The path to generated contents
        content_id (int): The ID of conetent to analyze
        agent_id (str): Analyzer agent id
        subject (str): The subject of content to be analyzed
        sys_anlys (str): System prompt for analyzing the content
        msg_anlys (str): Prompt for analyzing the content
        analyzer_fn (Function): Analysis function
        analyzer_loop (Analysis): Analysis loop

    Returns:
        NoReturn:
    """
    base_name = kwargs["file_name"]

    file_name_image = f"{base_name}_{content_id}.png"
    file_name_text = f"{base_name}_{content_id}.txt"

    partition_name_image = kwargs["partition_name_image"]
    partition_name_text = kwargs["partition_name_text"]

    local_file_path_image = kwargs["local_file_path_image"] + file_name_image
    local_file_path_text = kwargs["local_file_path_text"] + file_name_text

    download_status = kwargs["download"](
        local_file_path_image,
        partition_name_image,
        file_name_image,
        s3_client=kwargs["s3_client"],
        bucket_name=kwargs["bucket_name"],
    )

    if download_status:
        thread_name = threading.current_thread().name
        thread = client.beta.threads.create()

        edited_msg_anlys = anlys_image_user_prompt(
            file_name_image, local_file_path_image, subject
        )

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=edited_msg_anlys
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=agent_id
        )

        # message_content = message.content[0].text.value
        # print(f"{thread_name} received message: {message_content}")

        result, response = analyzer_loop(
            client,
            kwargs["local_file_path_image"],
            file_name_image,
            thread.id,
            run.id,
            analyzer_fn,
        )

        # Define a pattern that matches the dictionary
        pattern = r"\{(.*?)\}"  # Non-greedy match of anything between curly braces
        # Use re.DOTALL to make dot match any character, including newlines
        match = re.search(pattern, result, re.DOTALL)

        print(response)

        if match:
            # Extract the captured group
            dict_str = match.group(1)

            dict_obj = f"{dict_str}"

            # First write the dict_obj to a local_file_path_text
            with open(local_file_path_text, "w") as f:
                f.write(dict_obj)

            # Then, upload the file from local directory to s3 partition
            _ = kwargs["upload"](
                local_file_path_text,
                partition_name_text,
                file_name_text,
                s3_client=kwargs["s3_client"],
                bucket_name=kwargs["bucket_name"],
            )

            comm.queues["anlys_to_cont"].put(result)
