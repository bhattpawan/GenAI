from ollama import chat

messages = [
    {
        "role": "user",
        "content": "Tell me something about Lionel Messi in 100 words",
    }
]


def generate_response(messages):
    response = chat(model="qwen3:1.7b", messages=messages, think=False)
    return response.message.content


def stream_response(messages):
    stream = chat(model="qwen3:1.7b", messages=messages, think=False, stream=True)
    for chunk in stream:
        print(chunk.message.content, end="", flush=True)


try:
    response_content = generate_response(messages)
    print(response_content)

    stream_response(messages)
except ConnectionError as e:
    print(f"Connection error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
