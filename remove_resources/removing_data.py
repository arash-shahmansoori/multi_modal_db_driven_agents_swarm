import subprocess
from typing import NoReturn


def remove_local_data(local_data: str) -> NoReturn:
    r = subprocess.run(["rm", "-rf", local_data], capture_output=True, text=True)


def remove_database(database: str) -> NoReturn:
    r = subprocess.run(["rm", "-rf", database], capture_output=True, text=True)
