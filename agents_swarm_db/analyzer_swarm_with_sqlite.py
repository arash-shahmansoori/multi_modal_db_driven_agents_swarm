import io
import json
import os
import re
import threading
from queue import Queue
from typing import Dict, NoReturn

from openai import OpenAI
from PIL import Image

from type_extensions import Analysis, Function


def analyzer_agent_swarm_sqlite(
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
    """Analyzer agent with thread-safe connection to sqlite database

    Args:
        client (OpenAI): Client instance
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
    session = kwargs["Session"]()
    try:
        # Query the database for the image
        content = (
            session.query(kwargs["Gen-Table"])
            .filter(kwargs["Gen-Table"].id == content_id)
            .one_or_none()
        )

        if content and content.data:
            # Convert binary data to a bytes object and use PIL to display
            image_data = io.BytesIO(content.data)
            image = Image.open(image_data)

            file_name = f"image_{content_id}.png"
            image.save(os.path.join(kwargs["local_file_path_image"], file_name))

            thread_name = threading.current_thread().name
            thread = client.beta.threads.create()

            edited_msg_anlys = anlys_image_user_prompt(
                file_name, kwargs["local_file_path_image"], subject
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
                file_name,
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

                try:
                    # Convert the string to a dictionary object
                    dict_obj = json.loads(dict_str)

                    # Access the summary and score keys
                    summary = dict_obj["summary"]
                    score = dict_obj["score"]

                    # Print the results
                    print("Summary:", summary)
                    print("Score:", score)

                except json.JSONDecodeError as e:
                    # Handle the JSONDecodeError
                    print(f"An error occurred while decoding JSON: {e.msg}")

                    summary_edited = f"{dict_str}"

                    # Manually create a dictionary
                    dic_str_edited = {"summary": summary_edited, "score": ""}

                    # Access the summary and score keys
                    summary = dic_str_edited["summary"]
                    score = dic_str_edited["score"]

                analysis_result = kwargs["Anlys-Table"](summary=summary, score=score)
                session.add(analysis_result)
                session.commit()

                comm.queues["anlys_to_cont"].put(result)
    finally:
        session.close()
