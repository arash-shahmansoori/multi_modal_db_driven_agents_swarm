import os

from agent_baseline import generator_agent_baseline
from agent_funcs import img_generator
from agent_loop import agent_loop_gen_with_func
from configs import parse_kwargs
from shared_components import create_client


def main():
    params = parse_kwargs()

    client = create_client()

    # Make directories to save generation and analysis outputs
    try:
        os.makedirs("data/generation")
    except FileExistsError:
        # directory already exists
        pass

    subject = params["subject"]

    file_name = "futuristic_cityscape_baseline.png"

    sys_prompt = """
                # MISSION
                As the Generator Agent, you receive generation tasks from the user. Your role is to generate content based on user query. 
                """

    usr_prompt = (
        f"Generate a photo-realistic Image of {subject}"
        + f" Save the file as: {file_name}."
    )

    # Unify function arguments
    generator_fn = img_generator

    generator_agent_baseline(
        client,
        sys_prompt,
        usr_prompt,
        generator_fn,
        agent_loop_gen_with_func,
        **params["params_gen"],
    )


if __name__ == "__main__":
    main()
