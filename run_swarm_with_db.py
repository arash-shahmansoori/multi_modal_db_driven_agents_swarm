import json
import os
import threading

from agent_funcs import img_analyzer, img_generator
from agent_loop import agent_loop, agent_loop_anlys_with_func, agent_loop_gen_with_func
from agents_build import agent_builder
from communication import ThreadCommunication, get_all_items
from configs import parse_kwargs_db
from prompts import (
    anlys_image_user_prompt,
    cont_image_user_prompt,
    gen_image_user_prompt,
)

# from remove_resources import remove_local_data
from shared_components import create_client


def main():
    comm = ThreadCommunication()

    params = parse_kwargs_db()

    client = create_client()

    agents_ids_dir_name = "agents_build/ids/"
    agents_ids_file_name = "agent_ids.json"

    file_path = os.path.join(agents_ids_dir_name, agents_ids_file_name)

    feedback = "# Feedback on Generations:\n"  # Initialize feedback from previous round

    for r in range(params["n_round"]):
        # Make directories to save generation and analysis outputs
        try:
            os.makedirs(agents_ids_dir_name)
            os.makedirs(params["kwargs_db"]["local_file_path_image"])
            if params["kwargs_name"] == "kwargs_s3":
                os.makedirs(params["kwargs_db"]["local_file_path_text"])
        except FileExistsError:
            # directory already exists
            pass

        agents_ids_json = []

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                agents_ids = json.load(f)

                cont_agent_id = agents_ids[0]["controller"]
                gen_agent_id = agents_ids[1]["generator"]
                anlys_agent_id = agents_ids[2]["analyzer"]

        else:
            _, agent_cont = agent_builder(
                client,
                params["sys_prompt_cont"],
                params["num_cont_agent"],
                **params["params_cont"],
            )

            cont_agent_id = agent_cont.id

            _, agent_gen = agent_builder(
                client,
                params["sys_prompt_gen"],
                params["num_gen_agent"],
                **params["params_gen"],
            )

            gen_agent_id = agent_gen.id

            _, agent_anlys = agent_builder(
                client,
                params["sys_prompt_anlys"],
                params["num_anlys_agent"],
                **params["params_anlys"],
            )

            anlys_agent_id = agent_anlys.id

            with open(file_path, "w") as file:
                agents_ids_json.append({"controller": cont_agent_id})
                agents_ids_json.append({"generator": gen_agent_id})
                agents_ids_json.append({"analyzer": anlys_agent_id})

                json.dump(agents_ids_json, file)

        generator_fn = img_generator
        analyzer_fn = img_analyzer

        subject = params["subject"]

        msg_cont = cont_image_user_prompt(subject, feedback)

        # Create threads
        controller_thread = threading.Thread(
            target=params["kwargs_db"]["controller"],
            args=(
                client,
                cont_agent_id,
                params["subject"],
                msg_cont,
                params["thread_count_gen"],
                comm,
                gen_image_user_prompt,
                agent_loop,
            ),
            name="Communication-Thread-Controller",
        )

        generator_threads = [
            threading.Thread(
                target=params["kwargs_db"]["generator"],
                args=(
                    client,
                    i + 1 + (r) * params["thread_count_gen"],
                    gen_agent_id,
                    comm,
                    params["gen_time_out"],
                    generator_fn,
                    agent_loop_gen_with_func,
                ),
                kwargs=params["kwargs_db"],
                name=f"Thread-Generator-{i}",
            )
            for i in range(params["thread_count_gen"])
        ]

        analyzer_threads = [
            threading.Thread(
                target=params["kwargs_db"]["analyzer"],
                args=(
                    client,
                    i + 1 + (r) * params["thread_count_gen"],
                    anlys_agent_id,
                    params["subject"],
                    comm,
                    anlys_image_user_prompt,
                    analyzer_fn,
                    agent_loop_anlys_with_func,
                ),
                kwargs=params["kwargs_db"],
                name=f"Thread-Analyzer-{i}",
            )
            for i in range(params["thread_count_anlys"])
        ]

        # Start the controller thread & Wait for thread to finish dispatching
        controller_thread.start()
        controller_thread.join()

        print("Dispatching completed.")

        # Start threads & Wait for threads to finish generation
        for generator_thread in generator_threads:
            generator_thread.start()

        for generator_thread in generator_threads:
            generator_thread.join()

        print("Generation completed.")

        # Start threads & Wait for threads to finish analysis
        for analyzer_thread in analyzer_threads:
            analyzer_thread.start()

        for analyzer_thread in analyzer_threads:
            analyzer_thread.join()

        print("Analysis completed.")

        # # Remove local data after each round
        # if params["kwargs_name"] == "kwargs_s3":
        #     remove_local_data("data_s3")
        # else:
        #     remove_local_data("data")

        assesments = get_all_items(comm.queues["anlys_to_cont"])

        feedback = f"""
                    {feedback}

                    ## Feedback
                    {assesments}

                    ## Round
                    {r}
                    """


if __name__ == "__main__":
    main()
