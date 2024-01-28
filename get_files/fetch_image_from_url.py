import requests


def fetch_image(url: str) -> bytes:
    response = requests.get(url)

    return response.content
