from shared_components import create_client

client = create_client()

query = "Description of the proposed method for the README.md file of my repository on github"
additional_requirement = ""  # Use for Title
# additional_requirement = "The abstract should be maximum 200 words. DO NOT INCLUDE TITLE ONLY OUTPUT THE ABSTRACT."  # Use for abstract
# additional_requirement = "You need to specifically mention the main contributions of the blog including: the concurrency for generation and analysis, efficient composite task decomposition, efficient communication between agents, integration of database with AWS S3 bucket and sqlite support, multi-generation and multi-analysis in one go using the concurrency in generation and concurrency in analysis as well as multi-modal capabilities demonstrated for the application of image generation and analysis. The proposed method provides a general framework for multi-generation and multi analysis in hirarchical swarm of agents that can be of crucial importants for accuracte and high quality conent generation in different applications ranging from code generation, audio, summarization and so on. However, here we propose the method for image generation and analysis to emphasize on the multi-modal capabilities. It is ideal to use the bulletpoints to emphasize on the novel aspects of the blog at the end of the introduction. Make sure that each bulletpoint points out a semantically different aspect of the research contributions. DO NOT INCLUDE TITLE AND ABSTRACT ONLY OUTPUT THE INTRODUCTION."  # Use for introduction
# additional_requirement = "The main method should include a pictorial viewpoint of the proposed approach to clearly describe the proposed method. In particular, the pictorial viewpoint of the proposed method should describe clearly and easily all the steps in the proposed method using a descriptive and easy to read block diagram using Mermaid Markdown DIAGRAM. Subsequently, you describe the proposed algorithm based on the block diagram in details and easy to follow way. DO NOT INCLUDE TITLE, ABSTRACT, AND INTRODUCTION ONLY OUTPUT THE MAIN METHOD. Finally, revise the main method section and make sure that it follows the mermaid markdown workflow for the proposed method and all the above description provided regarding the proposed method. Make sure the diagram and the scientific workflow of the proposed method are coherent and match each other conceptually."  # Use for the main method
# additional_requirement = """The results section should include the following subsections. First, the setup including the types of models used for each agent. In particular, all the agents in the swarm use: "gpt-4-1106-preview" as the main LLM model. Additionally, the generator agent has access to "dall-e-3" model through function calling, and the analyzer agent has access to "gpt-4-vision-preview" through function calling. Second, the baseline includes the naive text to image generation using "dall-e-3" model. In the result section, the main aim is to emphasize the fact that using concurrent generation and concurrent analysis, database to search the best generated content in terms of highest average stipulated requirements, and the refinement as a result of cuclying the generation and analysis iteratiively, results a more aligned generated content with highest average stipulated score, in this case image. We also want to emphasize that this is just a building block for the future research in the context of swarm of mulyi-modal agents and a path towards the artificial general inteligence."""

# system_prompt = """you are the best artist and philosopher and painter in the world. You create the best prompts based on philosophical concepts to generate images. The user provide you the concept that you are supposed to use to generate the prompt to be used for text to image generation, your task is to provide the best prompt considering all the nuances for text to image generation based on the philosophical concept. You create the prompt such that the potential generated image is unique, outstanding art form with deep philosophical concepts."""


# system_prompt = """You are the best scientific artificial (general) intelligence researcher and blogger in the world. You provide the best suggestions for writing scientific papers related to artificial (general) intelligence, machine learning, and deep learning. You will be asked questions by the user for generating scientific suggestions for writing papers. The user asks your suggestions for writing different parts of a scientific paper, i.e., title, abstract, introduction, main methods, results, and conclusions. You only respond to what the user asks for and do not try to provide additional responses that are not related to the original user query."""

system_prompt = """You are the best scientific artificial (general) intelligence researcher and blogger in the world. You provide the best suggestions for writing scientific blogs related to artificial (general) intelligence, machine learning, and deep learning. You will be asked questions by the user for generating scientific suggestions for writing blogs. The user asks your suggestions for writing different parts of a scientific blog, i.e., title, introduction, main methods, results, and conclusions. You only respond to what the user asks for and do not try to provide additional responses that are not related to the original user query."""

user_prompt = f"""
I have designed a hirarchical swarm of agents including a controller agent, a generator agent, an analyzer agent, and a database. The controller agent is in charge of breaking down a composite task to two subtasks, one for generator agent and another for analyzer agent. The generator agent is in charge of the generation of content according to the subtask assigned by the controller agent. The generator agent generates content concurrently and efficiently and add the generated contents to a database for robust interaction with the analyzer agent. The analyzer agent is in charge of analyzing the generated content according to the generated content retrieved from the database and the assigned dubtask from the controller agent. The analyzer agent analyzes the generated contents from the database concurrently, writes the corresponding analysis of the generated content to the database, and sends back the assesment according to the provided requirements for the sub-task provided by the controller to the controller agent for each concurrently analyzed generated content. For the database, both sqlite and AWS s3 bucket are supported.

The work flow of the communication between agents is as follows.

(1) Controller Agent -> Creates subtasks from a composite task and sends messages to both Generator and Analyzer Agents.
(2) Generator Agent -> Generates contents according to subtask assigned by the Controller Agent concurrently and writes the generated contents to a database for analysis.
(3) Analyzer Agent -> Concurrently analyzes the generated contents by the Generator Agent and writes the results of the corresponding analysis of the generated contents to the database. The analyzer agent sends back the summary of the analysis for each generated content and the corresponding average stipulated score to the controller agent.
(4) Controller Agent -> For the next round controller agent pulls the necessary information from analysis, e.g., the image with highest score and corresponding analysis, and creates subtasks from a composite task and sends messages to both Generator and Analyzer Agents for further refinement and improvement of any stipulated requrements that need more improvement to achieve higher average stipulated score.
(5) The process (2) to (4) is repeated so that the generated content reach the highest possible average stipulated score.

Please note that since the generation and analysis are concurrent processes, I want the Mermaid Markdown Diagram to showcase this concurrency. The diagram should also specify the order in the proposed method according to the steps above. It should also emphasize the support for both AWS S3 bucket and SQLITE database for a robust interaction between Generator and Analyzer agents.

According to the above information, provide the best possible {query} for this blog. The {query} should be smart, unique, concise, and capture all the key novel aspects of the aforementioned process above as much as possible. It should emphasize on the concurrency for generation and analysis, database, efficient composite task decomposition, efficient communication between agents, and multi-generation and multi-analysis in one go using the concurrency in generation and concurrency in analysis as well as multi-modal capabilities demonstrated for the application of image generation and analysis and robust interaction between Generator and Analyzer agents using database. Finally, it should emphasize on the use of databse (both AWS S3 bucket and SQLITE are suppoorted for our implementation) to make communication between generator and analyzer agents more robust and efficient. The proposed method provides a general framework for multi-generation and multi-analysis in hirarchical swarm of agents that can be of crucial importants for accuracte and high quality multi-modal conetn generation in different applications ranging from code generation, audio, summarization and so on. However, here we propose the method for image generation and analysis to emphasize on the multi-modal capabilities. 

{additional_requirement}
"""

extra = """
Include the following mermaid diagram in your description of the process for my READ.md file. DO NOT CHANGE THE MERMAID DIAGRAM JUST INCLUDE IT TO MY README.MD FILE DESCRIPTION OF THE PROCEDURE AS IT IS.

```mermaid
sequenceDiagram
    participant CA as Controller Agent
    participant GA as Generator Agent
    participant DB as Database (SQLite/AWS S3)
    participant AA as Analyzer Agent

    Note over CA: Initialization
    CA->>GA: Assign generation subtask
    CA->>AA: Assign analysis subtask

    par Generation Process
        loop Concurrent Generation
            GA->>DB: Write generated content
            Note over GA: Content Generation
        end
    and Analysis Process
        loop Concurrent Analysis
            AA->>DB: Read generated content
            DB-->>AA: Provide generated content
            AA->>DB: Write analysis result
            Note over AA: Content Analysis
        end
    end
    CA->>AA: Request summary and average score
    AA->>CA: Send summary and average score

    loop Evaluation and Refinement
        CA->>DB: Pull analysis information for decision making
        CA->>GA: Assign refined generation subtask
        CA->>AA: Assign refined analysis subtask
        Note over CA: Processing feedback for content improvement
    end
```

"""

# extra = """
# Explain the following python code for the entire process in this blog post:

# python code for the entire process:


# import json
# import os
# import threading

# from agent_funcs import img_analyzer, img_generator
# from agent_loop import agent_loop, agent_loop_anlys_with_func, agent_loop_gen_with_func
# from agents_build import agent_builder
# from communication import ThreadCommunication
# from configs import parse_kwargs_db
# from prompts import (
#     anlys_image_user_prompt,
#     cont_image_user_prompt,
#     gen_image_user_prompt,
# )

# # from remove_resources import remove_local_data
# from shared_components import create_client


# def main():
#     comm = ThreadCommunication()

#     params = parse_kwargs_db()

#     client = create_client()

#     agents_ids_dir_name = "agents_build/ids/"
#     agents_ids_file_name = "agent_ids.json"

#     file_path = os.path.join(agents_ids_dir_name, agents_ids_file_name)

#     for r in range(params["n_round"]):
#         # Make directories to save generation and analysis outputs
#         try:
#             os.makedirs(agents_ids_dir_name)
#             os.makedirs(params["kwargs_db"]["local_file_path_image"])
#             if params["kwargs_name"] == "kwargs_s3":
#                 os.makedirs(params["kwargs_db"]["local_file_path_text"])
#         except FileExistsError:
#             # directory already exists
#             pass

#         agents_ids_json = []

#         if os.path.exists(file_path):
#             with open(file_path, "r") as f:
#                 agents_ids = json.load(f)

#                 cont_agent_id = agents_ids[0]["controller"]
#                 gen_agent_id = agents_ids[1]["generator"]
#                 anlys_agent_id = agents_ids[2]["analyzer"]

#         else:
#             _, agent_cont = agent_builder(
#                 client,
#                 params["sys_prompt_cont"],
#                 params["num_cont_agent"],
#                 **params["params_cont"],
#             )

#             cont_agent_id = agent_cont.id

#             _, agent_gen = agent_builder(
#                 client,
#                 params["sys_prompt_gen"],
#                 params["num_gen_agent"],
#                 **params["params_gen"],
#             )

#             gen_agent_id = agent_gen.id

#             _, agent_anlys = agent_builder(
#                 client,
#                 params["sys_prompt_anlys"],
#                 params["num_anlys_agent"],
#                 **params["params_anlys"],
#             )

#             anlys_agent_id = agent_anlys.id

#             with open(file_path, "w") as file:
#                 agents_ids_json.append({"controller": "cont_agent_id"})
#                 agents_ids_json.append({"generator": "gen_agent_id"})
#                 agents_ids_json.append({"analyzer": "anlys_agent_id"})

#                 json.dump(agents_ids_json, file)

#         generator_fn = img_generator
#         analyzer_fn = img_analyzer

#         subject = params["subject"]

#         msg_cont = cont_image_user_prompt(subject)

#         # Create threads
#         controller_thread = threading.Thread(
#             target=params["kwargs_db"]["controller"],
#             args=(
#                 client,
#                 cont_agent_id,
#                 params["subject"],
#                 msg_cont,
#                 params["thread_count_gen"],
#                 comm,
#                 gen_image_user_prompt,
#                 agent_loop,
#             ),
#             name="Communication-Thread-Controller",
#         )

#         generator_threads = [
#             threading.Thread(
#                 target=params["kwargs_db"]["generator"],
#                 args=(
#                     client,
#                     i + 1 + (r) * params["thread_count_gen"],
#                     gen_agent_id,
#                     comm,
#                     params["gen_time_out"],
#                     generator_fn,
#                     agent_loop_gen_with_func,
#                 ),
#                 kwargs=params["kwargs_db"],
#                 name=f"Thread-Generator-i",
#             )
#             for i in range(params["thread_count_gen"])
#         ]

#         analyzer_threads = [
#             threading.Thread(
#                 target=params["kwargs_db"]["analyzer"],
#                 args=(
#                     client,
#                     i + 1 + (r) * params["thread_count_gen"],
#                     anlys_agent_id,
#                     params["subject"],
#                     comm,
#                     anlys_image_user_prompt,
#                     analyzer_fn,
#                     agent_loop_anlys_with_func,
#                 ),
#                 kwargs=params["kwargs_db"],
#                 name=f"Thread-Analyzer-i",
#             )
#             for i in range(params["thread_count_anlys"])
#         ]

#         # Start the controller thread & Wait for thread to finish dispatching
#         controller_thread.start()
#         controller_thread.join()

#         print("Dispatching completed.")

#         # Start threads & Wait for threads to finish generation
#         for generator_thread in generator_threads:
#             generator_thread.start()

#         for generator_thread in generator_threads:
#             generator_thread.join()

#         print("Generation completed.")

#         # Start threads & Wait for threads to finish analysis
#         for analyzer_thread in analyzer_threads:
#             analyzer_thread.start()

#         for analyzer_thread in analyzer_threads:
#             analyzer_thread.join()

#         print("Analysis completed.")

#         # # Remove local data after each round
#         # if params["kwargs_name"] == "kwargs_s3":
#         #     remove_local_data("data_s3")
#         # else:
#         #     remove_local_data("data")

#     assesments = comm.queues["anlys_to_cont"].get()
#     print(assesments)


# if __name__ == "__main__":
#     main()


# """

# sub_prompt = """
# # MISSION
# As the Generator Agent within a hierarchical agent network, you receive generation tasks from the Controller Agent and communicate with the Analyzer Agent to ensure alignment with task requirements. Follow the process in the METHODOLOGY to generate content step by step.

# # METHODOLOGY
# - User query: Generate an image of [topic]. The image should include the following [task requirements provided if any]:
# - Form a generic set of attributes as bullet points based on:
#     [topic], [task requirements provided if any], and [additional generic requirements for high quality content creation].
# - Make sure that generated content meets ALL the specifications in the previous step.
# - output: Return the output based on the following OUTPUT FORMAT.


# # OUTPUT FORMAT
# Returns the generated content and save the generated file.
# """
# sub_prompt = """
# # MISSION
# As the analyzer agent within a hierarchical network, your role is to scrutinize content created by the generator agent upon assignments from the controller agent. Post-analysis, you are responsible for succinctly conveying the essence of your analysis and the compliance level to the controller agent. Additionally, you must transmit a confirmation signal back to the generator agent. For each stipulated requirement you provide an integer score between 0 and 10 for 10 being the best and 0 being the worst in terms of satisfaction level, e.g., Score: 10 -> means fully satisfied; Score: 5 -> means partially satisfied; Score: 0 -> not satisfied at all. For the overall assessment you provide an average score of all stipulated requirements, e.g., Average Score: mean(Scores) where mean(.) computes the average of all stipulated requirements Scores. Note: v_i denotes an integer score between 0 and 10 for the i-th stipulated requirement.

# # METHODOLOGY
# - user query: Analyze [type of content, e.g., image, text] related to [topic]. Ensure every listed [task requirement provided if any] is fully met.
# - Form a generic set of stipulated requirements for analysis as bullet points based on:
#     [topic], [task requirement provided if any], and [additional generic set of stipulated requirements for high quality content analysis]
#     * Note you are allowed to add any additional generic set of stipulated requirements according to the [topic] and [task requirements provided if any]
# - scrutinize generated content: Make sure that ALL the stipulated requirements in the previous step have been thoroughly met with a given score v_i provided.
# - Compute the average score based on all stipulated requirements scores above, v_i, and provide a concise summary of your analysis.
# - output: Return the output dictionary based on the following OUTPUT FORMAT.

# # OUTPUT FORMAT
# Construct the output as a dictionary with two key-value pairs. The key "summary" corresponds to a concise summary of your analysis, and "score" pertains to the Average Score based on all stipulated requirements Scores.

# Expected output structure:
# {
#     "summary": "a concise summary of your analysis",
#     "score": "Average Score"
# }
# """

# sub_prompt = """
# # MISSION
# As the Controller agent within a hierarchical network of agents, your role encompasses overseeing the generation and analysis workflow. Your specific duties include delegating responsibilities to a Generator agent and an Analyzer agent by breaking down a composite task into two focused sub-tasks: one for content generation and the other for subsequent content analysis.

# # INSTRUCTIONS
# Upon receiving a user query, partition it into a generation sub-task and an analysis sub-task. The generation sub-task instructs the Generator agent on what content to create, while the analysis sub-task guides the Analyzer agent on how to evaluate the generated content.

# # OUTPUT FORMAT
# Construct the output as a dictionary with two key-value pairs. The key "gen" corresponds to the content generation sub-task, and "anlys" pertains to the content analysis sub-task. Each associated value should be a precise segment of the user's query relevant to each agent's task.

# Expected output structure:
# {
#     "gen": "[generation sub-task from user query]",
#     "anlys": "[analysis sub-task from user query]"
# }

# # EXAMPLES
# User query: "Generate a detailed report on current market trends. Analyze the implications for our sales strategy."
# Output queries:
# {
#     "gen": "Generate a detailed report on current market trends.",
#     "anlys": "Analyze the implications for our sales strategy."
# }
# """

# agent_name, responsibility = "generator", "generation"
# agent_name, responsibility = "analyzer", "analysis"


# user_prompt = f"""
# I want to have a generic system prompt for content {responsibility}. The system prompt should be generic, cover wide range of requirements, and have a way to makes sure of quality, diversity, originality, and uniqueness of content. Please note that the {agent_name} is part of the {responsibility} process within a hierarchical agent network.

# The system prompt should be formatted as follows:

# ```system prompt
# {sub_prompt}
# ```

# Please use the same format above and use the best practices for prompt engineering in LLMs. Additionally, provide Two sets of examples under the # EXAMPLES after # METHODOLOGY in the system prompt. You can use image and text generations as two sets of examples. In the # EXAMPLES make sure to follow the sturcture provided in the METHODOLOGY.
# """

# user_prompt = f"""
# I want to have a generic system prompt for a controller agent. Please note that the controller agent is part of a hierarchical network of agents. Your role encompasses overseeing the generation and analysis workflow. Your specific duties include delegating responsibilities to a Generator agent and an Analyzer agent by breaking down a composite task into two focused sub-tasks: one for content generation and the other for subsequent content analysis.

# The system prompt should be formatted as follows:

# ```system prompt
# {sub_prompt}
# ```

# Please use the same format above and use the best practices for prompt engineering in LLMs. Additionally, provide Two sets of examples under the # EXAMPLES in the system prompt. You can use image and text generations as two sets of examples. In the # EXAMPLES make sure to follow the guidlines provided in the # INSTRUCTIONS and format the output as described in # OUTPUT FORMAT.
# """

# user_prompt = """
# edit the following text, that is going to be placed in author's acknowledgment on the use of AI generated content for the blog post:

# Sections of this manuscript were drafted with the assistance of the GPT-4-1106-preview model and underwent prompt engineering to refine research suggestions and textual content. The prompts and code utilized in generating this content have been made transparent and are available for review alongside the supplementary materials provided with this submission. It is imperative to highlight that the GPT-4 model acted under the explicit guidance of the main author, Arash Shahmansoori, functioning in a capacity akin to that of a research assistant. Its role was to aid in editing, rephrasing, and suggesting corrections to improve the English language usage and paper structuring per the contributions supplied by the human author. Every scientific claim, hypothesis, method, result, and conclusion were originated and vetted by Arash Shahmansoori to ensure authenticity, scientific integrity, and adherence to arXiv's guidelines pertaining to AI-generated content. Ultimately, the responsibility for the content and any inadvertent errors remains with the human author.

# Arash Shahmansoori conceived and designed the study, executed the research, and provided the initial content. The AI system was employed as a tool for suggesting editorial changes, refining the paper's structure, and ensuring language clarity under the supervision of Arash Shahmansoori. Arash Shahmansoori also evaluated the AI's output for accuracy and relevancy to the scientific narrative, retaining full authorial responsibility for the final manuscript.

# Please note that the blog post is a blog intended for publishing in towards data science. Please do not use the word manuscript and modify terms so that it refers to the blog not paper or manuscript accordingly.
# """

# user_prompt = """
# How can I efficiently mention in a journal paper, to be placed in arxiv, that it is carefully generated by the "gpt-4-1106-preview" model, prompt engineering, and the generated content is fully assessed by the author for its validity, correctness, and alignment with the guidlines for AI generated content on arxiv. Also, please suggest under which section in the journal paper I have to disclose this. I want to also specify that All the prompts and code for generating the content have been also made available together with the aforementioned provided software. I want to emphasize that AI was prompted to act like a research scientist suggesting content based on the initial content  provided by the human author, i.e., AI acted as an editor to edi, rephrase, and suggest corrections and modofications for the use of English and formation of the paper according to the conetnts provided by the human author. The entire scientific contirbutions in this paper is cretaed by the human author, Arash Shahmansoori, and AI was only prompted to help editing the original content provided by the human author.
# """

# user_prompt = """
# I want to create a prompt for image generation using DALLE 3 OPENAI model. I want to create a photo-realistic image of a natural scenary with a lot of details including: trees, river, a boat, mountain, and sunset. The composition, lighting,  details, subject, style, and all the other necessary details should be included in the prompt. Please create the optimal prompt to achieve the maximum accuracy using the aforementioned text to image model. Please provide both system prompt and user prompt.
# """

# sys_prompt = You are the best Data Since blogger in the world. You are the best scientific artificial (general) intelligence researcher in the world. You provide the best suggestions for writing a blog related to artificial (general) intelligence, machine learning, and deep learning for ``Towards Data Science'' blog. You will be asked questions by the user for generating scientific suggestions for writing the blog. The user asks your suggestions for writing the best engaging and unique and outstanding scientific blog to be submitted to ``Towards Data Science'' blog for publication. You only respond to what the user asks for and do not try to provide additional responses that are not related to the original user query. The user also provide you with the scientific content he authored and you are supposed to write the blog for.

# usr_prompt= I am the author of the attached PDF file containing a scientific paper that I recently have written. I want to submit a blog post to be published in ``Towards Data Science''. Considering the fact that you are a great data science blogger in the world and the best artificial general intelligence researcher, write my the most engaging blog using the bets practices and taking into account ALL the key scientific contents in the provided PDF document. The blog should be engaging, easy to follow, unique, and use appropriate English vocabulary and style for writing top tier scientific blogs for ``Towards Data Science''.

# user_prompt = """
# I want to save the results of image in a url in a mongodb databse using python. Note that I do not want to save the result of image in url locally in a directory and want to directly save the generated image from a url into the mongodb database using python. Please provide the best solution using the best practices for doing so. Please provide a simple working example including all the steps explained clearly and in simple words. The images are of siwe less than 16 MB so we dont need Gridfs at this point.

# I want to retrieve the stored image in mongodb above in python, provide a simple code snippet to do so using the best practices.

# The above tasks were fulfilled succesfully, now do the following:


# I want to repeat the same process for sqlalchemy database in python which is easier to implement and work with specially for python development. Please provide the entire process and code snippets for doing so using the best practices.
# """

# user_prompt = """
# Please teach me how to use sqlalchemy database in python step by step in simple language.

# explain this : engine = create_engine('sqlite:///mydatabase.db')  # Replace with your database URI

# and tell me how to Replace with your database URI in very simple language and step by step
# """

# user_prompt = """
#     Below is the prompt for analyzing images i want to compress and make it shorter without losing any necessary information about the content, mission, methodology, output format or anny necessary informatio.

#     Analyze the generated image in the file: [file_name] and the path name: [path_gen]

#     # MISSION
#     As the analyzer agent within a hierarchical network, your role is to scrutinize content created by the generator agent upon assignments from the controller agent. Post-analysis, you are responsible for succinctly conveying the essence of your analysis and the compliance level to the controller agent. Additionally, you must transmit a confirmation signal back to the generator agent. For each stipulated requirement you provide an integer score between 0 and 10 for 10 being the best and 0 being the worst in terms of satisfaction level, e.g., Score: 10 -> means fully satisfied; Score: 5 -> means partially satisfied; Score: 0 -> not satisfied at all. For the overall assessment, you provide an average score of all stipulated requirements, e.g., Average Score: mean(Scores) where mean(.) computes the average of all stipulated requirements' Scores. Note: v_i denotes an integer score between 0 and 10 for the i-th stipulated requirement.

#     # METHODOLOGY
#     - user query: Analyze [type of content, e.g., image, text] related to [topic]. Ensure every listed [task requirement provided if any] is fully met.
#     - Form a generic set of stipulated requirements for analysis as bullet points based on:
#         [topic], [task requirement provided if any], and [additional generic set of stipulated requirements for high-quality content analysis]
#         * Note: You are allowed to add any additional generic set of stipulated requirements according to the [topic] and [task requirements provided if any].
#     - Scrutinize generated content: Make sure that ALL the stipulated requirements in the previous step have been thoroughly met and provide a score v_i for each.
#     - Compute the average score based on all stipulated requirements scores, v_i, and provide a concise summary of your analysis.
#     - Output: Return the output dictionary based on the following OUTPUT FORMAT.

#     # OUTPUT FORMAT
#     Construct the output as a dictionary with two key-value pairs together with detailed description and scores of every stipulated requirements. The key "summary" corresponds to a concise summary of your analysis, and "score" pertains to the Average Score based on all stipulated requirements' Scores.

#     Expected output structure:
#     Scores for every stipulated requirements +
#     {
#         "summary": "a concise summary of your analysis",
#         "score": "Average Score"
#     }

#     Example: Image Analysis
#     - user query: Analyze image related to climate change effects on polar fauna. Ensure the image is original and conveys a strong message.
#     - Stipulated requirements:
#     * Is the subject relevant to climate change impacts on polar fauna? (Relevance)
#     * Does the image possess originality, with no copyright infringement issues? (Originality)
#     * Is the visual message compelling and clear? (Message Clarity)
#     * Is the quality of the image high definition without artifacts? (Image Quality)
#     * Does it provoke thought and emotional engagement? (Engagement)
#     - Scores:
#     * Relevance: 9
#     * Originality: 8
#     * Message Clarity: 10
#     * Image Quality: 7
#     * Engagement: 9
#     - Average Score: mean([9, 8, 10, 7, 9]) = 8.6
#     - Summary: The image effectively depicts the effects of climate change on polar fauna with high relevance and emotional engagement. It is original and conveys a clear message. Image quality could be improved for better clarity.
#     - Output:
#     Scores for every stipulated requirements +
#     {
#         "summary": "The image effectively depicts the effects of climate change on polar fauna with high relevance and emotional engagement. It is original and conveys a clear message. Image quality could be improved for better clarity.",
#         "score": "8.6"
#     }
#     """

response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": user_prompt + extra},
    ],
    stream=True,
)

# print(response.choices[0].message.content)


for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
