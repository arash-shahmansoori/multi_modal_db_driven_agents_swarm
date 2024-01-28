import base64
import os

import dotenv
import requests

dotenv.load_dotenv()


def encode_content(path_name: str) -> str:
    with open(path_name, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def img_analyzer(path_name, file_name, **kwargs) -> str:
    """Analyze the generated image based on user prompt"""

    file_path = os.path.join(path_name, file_name)

    # Getting the base64 string
    base64_content = encode_content(file_path)

    api_key = os.getenv("OPENAI_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": kwargs["prompt"]},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_content}"
                        },
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    return response.json()["choices"][0]["message"]["content"]
