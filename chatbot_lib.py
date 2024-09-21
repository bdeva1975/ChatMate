import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MAX_MESSAGES = 20

class ChatMessage:
    def __init__(self, role, text):
        self.role = role
        self.text = text

def convert_chat_messages_to_openai_format(chat_messages):
    return [{"role": msg.role, "content": msg.text} for msg in chat_messages]

def chat_with_model(message_history, new_text=None):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    new_text_message = ChatMessage('user', text=new_text)
    message_history.append(new_text_message)
    
    number_of_messages = len(message_history)
    
    if number_of_messages > MAX_MESSAGES:
        del message_history[0 : (number_of_messages - MAX_MESSAGES) * 2]
    
    messages = convert_chat_messages_to_openai_format(message_history)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can change this to "gpt-4" if you have access
        messages=messages,
        max_tokens=2000,
        temperature=0,
        top_p=0.9
    )
    
    output = response.choices[0].message.content
    
    response_message = ChatMessage('assistant', output)
    message_history.append(response_message)
    
    return output

# Example usage
if __name__ == "__main__":
    message_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_model(message_history, user_input)
        print("Assistant:", response)