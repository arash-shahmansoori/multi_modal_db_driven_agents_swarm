from typing import Dict

import dotenv
from sqlalchemy import Column, Integer, LargeBinary, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from agent_funcs_schemes import img_analyzer_fn, img_generator_fn
from agents_swarm_db import (
    analyzer_agent_swarm_s3,
    analyzer_agent_swarm_sqlite,
    controller_agent_swarm,
    generator_agent_swarm_s3,
    generator_agent_swarm_sqlite,
)
from prompts import system_prompt_anlys, system_prompt_cont, system_prompt_gen
from s3_operations import (  # check_and_create_bucket,
    create_s3_client,
    download_file_from_s3_partition,
    save_image_to_s3_partition,
    upload_file_to_s3_partition,
)
from type_extensions import T

dotenv.load_dotenv()

# Create an instance of the declarative base class for defining the ORM models
Base = declarative_base()


# Model definition
class GeneratedImage(Base):
    __tablename__ = "generated-images"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    data = Column(LargeBinary)


class AnalyzedImage(Base):
    __tablename__ = "analyzed-images"

    id = Column(Integer, primary_key=True)
    summary = Column(String)
    score = Column(String)


def parse_kwargs_db() -> Dict[str, T]:
    model_name = "gpt-4-turbo-preview"

    params_cont = {"name": "Controller", "model": model_name}

    num_cont_agent = 1
    cont_time_out = 100

    sys_prompt_cont = system_prompt_cont

    # The subject structure is formed as follows: [main subject]. [More details about the main subject].
    # subject = "A futuristic cityscape. The image should include flying cars and tall skyscrapers with holographic advertisements."
    # subject = "2 dogs and 1 cat. The cat is in the middle and in the forground and the dogs are in the background."
    subject = "Visualize an ancient, colossal tree rooted at the precipice between two contrasting worlds, one bathed in a radiant, ethereal light symbolizing enlightenment and the inherent seeking of truth that exists within all beings. The other world is draped in shadows, representing the unknown, uncertainty, and the often obscured nature of reality that challenges our perceptions. The tree itself, a gargantuan embodiment of wisdom and timelessness, stretches its vast branches across both realms, interweaving the light and darkness into its bark and leaves, suggesting that truth and understanding thrive at the convergence of knowledge and mystery. Upon its sturdy, intertwining roots, ethereal figures are seated in thoughtful meditation, embodying the philosophic quest of humanity to grasp the absolute truth, their forms partially illuminated, partly in shadow, illustrating the continual striving towards understanding amidst the inherent limitations of human cognition. The sky above transitions smoothly from a vivid sunrise to the starlit darkness, echoing the eternal cycle of questioning and insight that propels the human spirit towards enlightenment. This scene encapsulates the philosophical exploration of the absolute truth in life, suggesting it is a journey rather than a destination, a ceaseless pursuit through the harmonious interplay of light and darkness, knowledge and mystery."

    sys_prompt_gen = system_prompt_gen

    params_gen = {"name": "Generator", "model": model_name, "tools": [img_generator_fn]}

    num_gen_agent = 1
    thread_count_gen = 2
    gen_time_out = 1

    sys_prompt_anlys = system_prompt_anlys
    params_anlys = {"name": "Analyzer", "model": model_name, "tools": [img_analyzer_fn]}

    num_anlys_agent = 1
    thread_count_anlys = 2
    anlys_time_out = 90

    # Number of rounds
    n_round = 2

    # Select the name of the db kwargs
    kwargs_name = "kwargs_sqlite"  # Now we support sqlite and aws s3

    if kwargs_name == "kwargs_sqlite":
        # Define the connection string
        DATABASE_URI = "sqlite:///images.db"

        # Create the SQLAlchemy engine
        engine = create_engine(DATABASE_URI)

        # Create a scoped session factory. This is thread-safe by design.
        Session = scoped_session(sessionmaker(bind=engine))

        # Create the table in the database
        Base.metadata.create_all(engine)

        path_gen_image_sqlite = "./data/images/"
        path_gen_text_sqlite = "./data/analysis/"

        kwargs_db = {
            "Session": Session,
            "Gen-Table": GeneratedImage,
            "Anlys-Table": AnalyzedImage,
            "local_file_path_image": path_gen_image_sqlite,
            "local_file_path_text": path_gen_text_sqlite,
            "controller": controller_agent_swarm,
            "generator": generator_agent_swarm_sqlite,
            "analyzer": analyzer_agent_swarm_sqlite,
        }

    else:
        # Create s3 client
        # Make sure to create a bucket with partitions for image and text
        s3_client = create_s3_client()
        base_file_name = "cityscape"

        bucket_name = "gen-content-openai"  # Name of  the s3 bucket
        region = "eu-west-1"  # Name of the default region

        # Check if the bucket exists else create it and partition it for images and analysis
        # check_and_create_bucket(s3_client, bucket_name, region)

        path_gen_image_s3 = "./data_s3/images/"
        path_gen_text_s3 = "./data_s3/analysis/"

        kwargs_db = {
            "s3_client": s3_client,
            "bucket_name": bucket_name,
            "region": region,
            "file_name": base_file_name,
            "partition_name_image": "images",
            "partition_name_text": "analysis",
            "local_file_path_image": path_gen_image_s3,
            "local_file_path_text": path_gen_text_s3,
            "download": download_file_from_s3_partition,
            "save": save_image_to_s3_partition,
            "upload": upload_file_to_s3_partition,
            "controller": controller_agent_swarm,
            "generator": generator_agent_swarm_s3,
            "analyzer": analyzer_agent_swarm_s3,
        }

    return {
        "params_cont": params_cont,
        "num_cont_agent": num_cont_agent,
        "sys_prompt_cont": sys_prompt_cont,
        "cont_time_out": cont_time_out,
        "params_gen": params_gen,
        "num_gen_agent": num_gen_agent,
        "thread_count_gen": thread_count_gen,
        "sys_prompt_gen": sys_prompt_gen,
        "gen_time_out": gen_time_out,
        "params_anlys": params_anlys,
        "num_anlys_agent": num_anlys_agent,
        "thread_count_anlys": thread_count_anlys,
        "sys_prompt_anlys": sys_prompt_anlys,
        "anlys_time_out": anlys_time_out,
        "subject": subject,
        "n_round": n_round,
        "kwargs_db": kwargs_db,
        "kwargs_name": kwargs_name,
    }
