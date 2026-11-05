from ollama import chat

messages = [
    {
        "role": "user",
        "content": "Tell me something about Lionel Messi in 100 words",
    }
]

response = chat(model="qwen3:1.7b", messages=messages, think=False)

print(response.message.content)
