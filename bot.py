# Personal AI Assistant - Phase 1: Terminal-based Python Bot

import json
import os
import datetime
import openai
import requests
from typing import Optional

# --- Configuration ---
CONFIG = {
    'openai_api_key': os.getenv("OPENAI_API_KEY"),
    'memory_file': 'memory.json'
}

# --- Memory Management ---
def load_memory():
    if os.path.exists(CONFIG['memory_file']):
        with open(CONFIG['memory_file'], 'r') as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(CONFIG['memory_file'], 'w') as f:
        json.dump(memory, f, indent=2)

# --- Basic Assistant Functions ---
def respond_to(prompt: str, memory: dict) -> str:
    openai.api_key = CONFIG['openai_api_key']
    chat_log = memory.get('chat_log', [])
    messages = [{'role': 'system', 'content': 'You are a helpful personal assistant.'}] + chat_log
    messages.append({'role': 'user', 'content': prompt})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    reply = response.choices[0].message['content']

    memory['chat_log'] = messages + [{'role': 'assistant', 'content': reply}]
    save_memory(memory)
    return reply

# --- Reminder & Schedule System ---
def add_reminder(task: str, time: Optional[str], memory: dict):
    reminder = {'task': task, 'time': time, 'created': str(datetime.datetime.now())}
    memory.setdefault('reminders', []).append(reminder)
    save_memory(memory)
    return f"Reminder added: {task} at {time if time else 'unspecified time'}"

# --- Main Loop ---
def main():
    print("Welcome to your personal AI assistant.")
    memory = load_memory()

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']: break

            if user_input.startswith("remind me to"):
                task = user_input[12:].strip()
                result = add_reminder(task, None, memory)
                print("Bot:", result)
            else:
                response = respond_to(user_input, memory)
                print("Bot:", response)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    main()# Personal AI Assistant - Phase 1: Terminal-based Python Bot

import json
import os
import datetime
import openai
import requests
from typing import Optional

# --- Configuration ---
CONFIG = {
    'openai_api_key': os.getenv("OPENAI_API_KEY"),
    'memory_file': 'memory.json'
}

# --- Memory Management ---
def load_memory():
    if os.path.exists(CONFIG['memory_file']):
        with open(CONFIG['memory_file'], 'r') as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(CONFIG['memory_file'], 'w') as f:
        json.dump(memory, f, indent=2)

# --- Basic Assistant Functions ---
def respond_to(prompt: str, memory: dict) -> str:
    openai.api_key = CONFIG['openai_api_key']
    chat_log = memory.get('chat_log', [])
    messages = [{'role': 'system', 'content': 'You are a helpful personal assistant.'}] + chat_log
    messages.append({'role': 'user', 'content': prompt})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    reply = response.choices[0].message['content']

    memory['chat_log'] = messages + [{'role': 'assistant', 'content': reply}]
    save_memory(memory)
    return reply

# --- Reminder & Schedule System ---
def add_reminder(task: str, time: Optional[str], memory: dict):
    reminder = {'task': task, 'time': time, 'created': str(datetime.datetime.now())}
    memory.setdefault('reminders', []).append(reminder)
    save_memory(memory)
    return f"Reminder added: {task} at {time if time else 'unspecified time'}"

# --- Main Loop ---
def main():
    print("Welcome to your personal AI assistant.")
    memory = load_memory()

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']: break

            if user_input.startswith("remind me to"):
                task = user_input[12:].strip()
                result = add_reminder(task, None, memory)
                print("Bot:", result)
            else:
                response = respond_to(user_input, memory)
                print("Bot:", response)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    main()