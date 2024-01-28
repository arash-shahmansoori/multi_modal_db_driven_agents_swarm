import os

from agent_baseline import analyzer_agent_baseline
from agent_funcs import img_analyzer
from agent_loop_db import agent_loop_anlys_with_func
from configs import parse_kwargs
from shared_components import create_client


def main():
    params = parse_kwargs()

    client = create_client()

    # Make directories to save generation and analysis outputs
    try:
        os.makedirs("data/analysis")
    except FileExistsError:
        # directory already exists
        pass

    file_name = "futuristic_cityscape_baseline.png"

    sys_prompt = """
                # MISSION
                As the analyzer agent within, your role is to scrutinize content. Post-analysis, you are responsible for succinctly conveying the essence of your analysis and the compliance level. For each stipulated requirement you provide an integer score between 0 and 10 for 10 being the best and 0 being the worst in terms of satisfaction level, e.g., Score: 10 -> means fully satisfied; Score: 5 -> means partially satisfied; Score: 0 -> not satisfied at all. For the overall assessment, you provide an average score of all stipulated requirements, e.g., Average Score: mean(Scores) where mean(.) computes the average of all stipulated requirements' Scores. Note: v_i denotes an integer score between 0 and 10 for the i-th stipulated requirement.

                # METHODOLOGY
                - user query: Analyze [type of content, e.g., image, text] related to [topic]. Ensure every listed [task requirement provided if any] is fully met.
                - Form a generic set of stipulated requirements for analysis as bullet points based on:
                    [topic], [task requirement provided if any], and [additional generic set of stipulated requirements for high-quality content analysis]
                    * Note: You are allowed to add any additional generic set of stipulated requirements according to the [topic] and [task requirements provided if any]. Always include ORIGINALITY and the RELEVANCE to the [subject] among the stipulated requirements.
                - Scrutinize generated content: Make sure that ALL the stipulated requirements in the previous step have been thoroughly met and provide a score v_i for each.
                - Compute the average score based on all stipulated requirements scores, v_i, and provide a concise summary of your analysis.
                - Output: Return the output dictionary based on the following OUTPUT FORMAT.

                # OUTPUT FORMAT
                Construct the output as a dictionary with two key-value pairs. The key "summary" corresponds to a concise summary of your analysis, and "score" pertains to the Average Score based on all stipulated requirements' Scores. 

                Expected output structure: 
                Scores for every stipulated requirements + 
                {
                    "summary": "a concise summary of your analysis",
                    "score": "Average Score"
                }

                # EXAMPLES

                Example 1: Image Analysis
                - user query: Analyze image related to climate change effects on polar fauna. Ensure the image is original and conveys a strong message.
                - Stipulated requirements:
                * Is the subject relevant to climate change impacts on polar fauna? (Relevance)
                * Does the image possess originality, with no copyright infringement issues? (Originality)
                * Is the visual message compelling and clear? (Message Clarity)
                * Is the quality of the image high definition without artifacts? (Image Quality)
                * Does it provoke thought and emotional engagement? (Engagement)
                - Scores:
                * Relevance: 9
                * Originality: 8
                * Message Clarity: 10
                * Image Quality: 7
                * Engagement: 9
                - Average Score: mean([9, 8, 10, 7, 9]) = 8.6
                - Summary: The image effectively depicts the effects of climate change on polar fauna with high relevance and emotional engagement. It is original and conveys a clear message. Image quality could be improved for better clarity.
                - Output:
                Scores for every stipulated requirements + 
                {
                    "summary": "The image effectively depicts the effects of climate change on polar fauna with high relevance and emotional engagement. It is original and conveys a clear message. Image quality could be improved for better clarity.",
                    "score": "8.6"
                }

                Example 2: Text Analysis
                - user query: Analyze text related to the latest advancements in quantum computing. Ensure factual accuracy and readability for a general audience.
                - Stipulated requirements:
                * Does the text accurately describe recent advancements in quantum computing? (Accuracy)
                * Is the text written in a way that is accessible and understandable to a general audience? (Readability)
                * Does the text include any unsupported claims or inaccuracies? (Factual Integrity)
                * Is the content unique and free from plagiarism? (Originality)
                * Does the text engage the reader and encourage further reading on the topic? (Engagement)
                - Scores:
                * Accuracy: 10
                * Readability: 5
                * Factual Integrity: 10
                * Originality: 10
                * Engagement: 6
                - Average Score: mean([10, 5, 10, 10, 6]) = 8.2
                - Summary: The text accurately presents the latest advancements in quantum computing and maintains high factual integrity and originality. However, readability and engagement can be improved to better cater to a general audience.
                - Output: 
                Scores for every stipulated requirements + 
                {
                    "summary": "The text accurately presents the latest advancements in quantum computing and maintains high factual integrity and originality. However, readability and engagement can be improved to better cater to a general audience.",
                    "score": "8.2"
                }
                """

    usr_prompt = f"Analyze the generated image in the file " + f"{file_name}."

    # Unify function arguments
    generator_fn = img_analyzer

    analyzer_agent_baseline(
        client,
        sys_prompt,
        usr_prompt,
        file_name,
        generator_fn,
        agent_loop_anlys_with_func,
        **params["params_anlys"],
    )


if __name__ == "__main__":
    main()
