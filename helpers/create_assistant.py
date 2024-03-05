import os
from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def create_assistant(name: str, instructions: str, model: str, **kwargs):
    return client.beta.assistants.create(name, instructions, model, **kwargs)


# use when necessary to update the assistant programmatically
def update_assistant(assistant_id: str, **kwargs):
    return client.beta.assistants.update(assistant_id=assistant_id, **kwargs)
