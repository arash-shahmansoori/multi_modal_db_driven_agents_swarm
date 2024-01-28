def cont_image_user_prompt(subject: str, feedback: str) -> str:
    prompt = f"Generate a photo-realistic image of {subject} Analyze the generated image. The following is your feedback from the previous round(s). {feedback}"

    return prompt


def gen_image_user_prompt(subject: str) -> str:
    main_prompt = f"Generate a photo-realistic image of {subject}"
    additional_details = """
    # MISSION
    Create a photo-realistic image in line with specific prompts by coordinating with the Controller and Analyzer Agents. Adhere to and execute the following streamlined process for content generation.

    # METHODOLOGY
    - Receive image generation prompt with details.
    - Compile key attributes list based on:
    - Theme, user's specific requirements, and standards for quality.
    - Ensure all specifications are met.
    - Provide generated image URL per the following format.

    # OUTPUT FORMAT
    - Image content: deliver as an image URL.

    # Example: Futuristic Cityscape Image
    - Query: Image with flying cars, tall skyscrapers with holographic ads.
    - Attributes: Futuristic, technologically advanced skyline, flying cars, holographic ads, neon color palette.
    - Output: Image URL of the futuristic cityscape.
    """
    prompt = main_prompt + additional_details
    return prompt


def anlys_image_user_prompt(file_name: str, path_gen: str, subject: str) -> str:
    main_prompt = f"Analyze the content in {file_name} at {path_gen}"
    requirements = f"Always include ORIGINALITY and the RELEVANCE to the {subject} among the stipulated requirements."
    additional_details = """
    # MISSION
    Your role as an analyzer agent is to evaluate generated content for quality and compliance with the controller agent's assignments, reporting to it succinctly. Send a confirmation signal to the generator agent after analysis. Assign an integer score (0-10) for each requirement to express satisfaction level. Provide an average score of these as the overall assessment.

    # METHODOLOGY
    - user query: Analyze [content type] regarding [topic], ensure all [task requirements] are met.
    - Define a set of analysis criteria based on the content type, topic, and task requirements, including additional criteria as necessary.
    - Evaluate the content, scoring each criterion.
    - Summarize the analysis and calculate the average score.
    - Deliver the results in the specified output format.

    # OUTPUT FORMAT
    Provide a dictionary with “summary” and “score” entries, detailing the analysis and the calculated average score.

    Example:
    - user query: Analyze image about polar fauna under climate change, confirm originality and message delivery.
    - Criteria and Scores:
    * Relevance: 9
    * Originality: 8
    * Message Clarity: 10
    * Image Quality: 7
    * Engagement: 9
    - Average Score: 8.6
    - Summary: High relevance and emotional impact are achieved in the analyzed image. It accurately informs on climate change effects on polar wildlife. Some concerns on image quality, suggest enhancement.
    - Output: 
    {
        "summary": "High relevance and emotional impact are achieved in the analyzed image. It accurately informs on climate change effects on polar wildlife. Some concerns on image quality, suggest enhancement.",
        "score": "8.6"
    }
    """
    prompt = main_prompt + additional_details + requirements
    return prompt
