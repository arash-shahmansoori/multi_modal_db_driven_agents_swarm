import json
from json.decoder import JSONDecodeError

from openai import OpenAI

from type_extensions import Function


def agent_loop_gen_with_func(
    client: OpenAI, thread_id: str, run_id: str, func: Function
) -> str:
    """The generation loop for the agent

    Args:
        client (OpenAI): Client instance
        thread_id (str): Thread Id for the agent
        run_id (str): Run Id for the agent
        func (Function): Function for the agent

    Returns:
        str: Response from the analyzer agent
    """
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        if run.status == "requires_action":
            outputs = []
            submitOutput = True
            for action in run.required_action.submit_tool_outputs.tool_calls:
                function_name = action.function.name

                try:
                    arguments = json.loads(action.function.arguments)

                    match function_name:
                        case func.__name__:
                            new_arguments = {
                                key: value
                                for key, value in arguments.items()
                                if key not in ["client"]
                            }

                            response = func(client, **new_arguments)
                            output = {"tool_call_id": action.id, "output": response}

                        case _:
                            response = (
                                f"There is no function with the name {function_name}"
                            )
                            output = {
                                "tool_call_id": action.id,
                                "output": "Unkown function",
                            }

                except JSONDecodeError:
                    print("JSON Decode error")
                except TypeError as e:
                    print(f"TypeError of {e} occured.")
                except UnboundLocalError as ue:
                    print(f"Unbound error of {ue} occured.")

                    response = "Unkown function"
                    output = {
                        "tool_call_id": "unknown",
                        "output": response,
                    }

                outputs.append(output)
            if submitOutput:
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id, run_id=run_id, tool_outputs=outputs
                )

        if run.status == "completed":
            message = client.beta.threads.messages.list(thread_id=thread_id)
            for datum in message.data:
                for content in datum.content:
                    return content.text.value, response
