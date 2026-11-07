from ollama import chat

messages = []

while True:
    user_input = input("You: ").strip()
    if not user_input:
        print("Please enter a valid input")
        continue
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot. Goodbye!")
        break

    if user_input.lower() == "reset":
        messages = []
        print("Conversation history has been reset.")
        continue

    messages.append({"role": "user", "content": user_input})

    assistant_response = ""

    try:
        response = chat(model="qwen3:1.7b", messages=messages, think=False, stream=True)
        print("Assistant: ", end="", flush=True)
        for chunk in response:
            content = chunk.message.content or ""
            print(content, end="", flush=True)
            assistant_response += content
        print()
        messages.append({"role": "assistant", "content": assistant_response})
    except ConnectionError as e:
        print(f"Connection error occurred: {e}")
        messages.pop()
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        messages.pop()
        break
