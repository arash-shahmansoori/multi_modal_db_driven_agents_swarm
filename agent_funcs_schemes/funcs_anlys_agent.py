img_analyzer_fn = {
    "type": "function",
    "function": {
        "name": "img_analyzer",
        "description": "Analyze the generated image based on user prompt",
        "parameters": {
            "type": "object",
            "properties": {
                "path_name": {
                    "type": "string",
                    "description": "The path to the generated image to analyze.",
                },
                "file_name": {
                    "type": "string",
                    "description": "The file name of the generated image to analyze.",
                },
                "prompt": {
                    "type": "string",
                    "description": "The user prompt to analyze the generated image.",
                },
            },
            "required": ["path_name", "file_name", "prompt"],
        },
    },
}
