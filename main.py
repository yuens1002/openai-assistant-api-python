from .helpers.general import (
    create_thread_and_run,
    wait_on_run,
    pretty_print,
    submit_tool_outputs,
    get_response,
    submit_message,
)
import json


print("hello, i'm your ai assistance, how can i help you?")

thread = None

# Main loop for the terminal chat
while True:
    try:
        # Get user input
        user_input = input("You: ")

        if user_input == "###":
            break  # Exit the chat if the user types ###

        try:
            if thread == None:
                # creates a new thread then run it
                thread, run = create_thread_and_run(user_input)
            else:
                # continue the conversation
                run = submit_message(thread.id, user_input)
        except Exception as e:
            print(f"Error generating thread_and_run: {e}")
            continue  # Skip the rest of the loop and prompt for user input again

        try:
            run = wait_on_run(run)
            if run.status == "requires_action":
                run = submit_tool_outputs(run)
            if run.status == "completed":
                messages = get_response(thread)
                pretty_print(messages)
        except Exception as e:
            print(f"An error occurred at wait_on_run: {e}")
            # Optionally, you can decide to break the loop or continue after handling the error
            # For this example, let's choose to continue
            continue

    except KeyboardInterrupt:
        print("\nExiting chat...")
        break  # Exit the chat if Ctrl+C is pressed
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, you can decide to break the loop or continue after handling the error
        # For this example, let's choose to continue
        continue
