import json
import os
import time
from ..functions.calendar_event_api import calendar_api
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

ASSISTANT_ID = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def submit_message(thread_id, user_message):
    print("submit message with: ", thread_id, user_message)
    # append a message on a thread
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )
    # associate the created thread to the assistant
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )


def submit_tool_outputs(run):
    tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
    name = tool_call.function.name
    print("name of the function being called: ", name)
    args = json.loads(tool_call.function.arguments)
    too_call_id = tool_call.id

    # Extract start_date_time and end_date_time and remove them from args
    start_date_time = args.pop("start_date_time")
    end_date_time = args.pop("end_date_time")

    try:
        response = calendar_api[name](start_date_time, end_date_time, **args)
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=run.thread_id,
            run_id=run.id,
            tool_outputs=[
                {"tool_call_id": too_call_id, "output": json.dumps(response)}
            ],
        )
        # wait until submit completes
        return wait_on_run(run)
    except Exception as e:
        print(f"An error occurred during calendar_api call: {e}")
        # Optionally, you can decide to break the loop or continue after handling the error
        # For this example, let's choose to continue


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


def create_thread_and_run(user_input):
    run = client.beta.threads.create_and_run(
        assistant_id=ASSISTANT_ID,
        thread={"messages": [{"role": "user", "content": user_input}]},
    )
    thread = client.beta.threads.retrieve(run.thread_id)
    return thread, run


# Pretty printing helper
def pretty_print(messages):
    # message = client.beta.threads.messages.retrieve(
    #     message_id=messages.last_id,
    #     thread_id=messages.thread_id,
    # )
    print(f"Assistant: {messages.data[-1].content[0].text.value}")
    # print("# Messages")
    # for m in messages:
    #     print(f"{m.role}: {m.content[0].text.value}")
    print()


# Waiting in a loop
def wait_on_run(run):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=run.thread_id,
            run_id=run.id,
        )
        print("run: ", run.status)
        time.sleep(0.5)
    return run


def upload_file(file_path):
    return client.files.create(file=open(file_path, "rb"), purpose="assistants")


def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))
