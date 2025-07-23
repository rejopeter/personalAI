import os
import time
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"🔑 Loaded API Key: {'Yes' if api_key else 'No'}")

client = OpenAI(api_key=api_key)

def chat():
    print("🤖 Your Personal Assistant (type 'exit' to quit)\n")

    messages = [{"role": "system", "content": "You are a helpful personal assistant."}]
    
    # Try models in this order
    models = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]
    model_index = 0

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        while model_index < len(models):
            model = models[model_index]
            try:
                if model == "text-davinci-003":
                    # Prepare a flat prompt
                    prompt = "\n".join([m["content"] for m in messages if m["role"] != "system"])
                    response = client.completions.create(
                        model=model,
                        prompt=prompt,
                        max_tokens=150,
                        temperature=0.7,
                    )
                    reply = response.choices[0].text.strip()
                else:
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=0.7,
                    )
                    reply = response.choices[0].message.content

                print(f"Assistant ({model}): {reply}\n")
                messages.append({"role": "assistant", "content": reply})
                break

            except OpenAIError as e:
                error_str = str(e)

                # Quota exceeded
                if "insufficient_quota" in error_str:
                    print(f"🚫 You've exceeded your quota for {model}. Trying fallback...\n")
                    model_index += 1
                    continue

                # Model not found
                elif "model_not_found" in error_str:
                    print(f"⚠️ Model {model} not available. Trying fallback...\n")
                    model_index += 1
                    continue

                # Rate limited
                elif "429" in error_str or "Too Many Requests" in error_str:
                    print(f"⏳ Rate limit hit for {model}. Waiting 10 seconds...\n")
                    time.sleep(10)
                    continue

                # Other OpenAI-related issues
                else:
                    print(f"❌ OpenAI error: {error_str}")
                    break

        else:
            print("💀 No available models or quota left to continue.")
            break

if __name__ == "__main__":
    chat()