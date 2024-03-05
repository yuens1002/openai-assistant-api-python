# OpenAI assistants api Integration with Google Calendar

## Run Instructions

run as a module from the parent directory, execute the following command assuming the code lives in the directory named openai-assistant-api-python

```bash
python -m openai-assistant-api-python.main
```

## Expectations

- this is sample app for demonstration purposes only
- leverages the Large Language Model (LLM) to decide and process a structured data set from user input
- calls the google calendar api via function calling to create the event.
- the llm prompts the user to supply any required or optional fields.
