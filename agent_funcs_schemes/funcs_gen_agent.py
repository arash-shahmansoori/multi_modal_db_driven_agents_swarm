img_generator_fn = {
    "type": "function",
    "function": {
        "name": "img_generator",
        "description": "Generate image based on user prompt",
        "parameters": {
            "type": "object",
            "properties": {
                "client": {
                    "type": "string",
                    "description": "The LLM openai client.",
                },
                "prompt": {
                    "type": "string",
                    "description": "The user prompt to generate an image, e.g., a nice waterfall.",
                },
            },
            "required": ["client", "prompt"],
        },
    },
}
