import subprocess

from remove_resources import remove_agents
from shared_components import create_client


def remove_all_agents():
    client = create_client()
    remove_agents(client, 100)


def remove_remaining_resources():
    # Remove all residual resources
    r0 = subprocess.run(["rm", "-rf", "data_s3"], capture_output=True, text=True)
    r1 = subprocess.run(["rm", "-rf", "data"], capture_output=True, text=True)
    r2 = subprocess.run(["rm", "-rf", "images.db"], capture_output=True, text=True)
    r3 = subprocess.run(
        ["rm", "-rf", "agents_build/ids/"], capture_output=True, text=True
    )
    print("All remaining resources are deleted.")


def main():
    remove_all_agents()
    # remove_remaining_resources()


if __name__ == "__main__":
    main()
