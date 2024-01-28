import openai
from openai import OpenAI


def img_generator(client: OpenAI, **kwargs) -> str:
    """Generate image based on user prompt"""

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=kwargs["prompt"],
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

    except openai.OpenAIError as e:
        image_url = e

    return image_url
