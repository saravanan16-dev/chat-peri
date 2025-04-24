import os
import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_MODEL = "llama3-8b-8192"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class SimpleGroqChatbot:
    def __init__(self):
        self.chat_history = []

    def call_groq(self, user_input):
        print("🚀 Calling Groq API...")
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "❌ Groq API key not set."

        self.chat_history.append({
            "role": "user", "content": user_input, "timestamp": datetime.datetime.now()
        })

        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages += [{"role": m["role"], "content": m["content"]} for m in self.chat_history]

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": GROQ_MODEL, "messages": messages}

        try:
            res = requests.post(GROQ_API_URL, headers=headers, json=payload)
            if res.status_code == 200:
                reply = res.json()["choices"][0]["message"]["content"]
                self.chat_history.append({
                    "role": "assistant", "content": reply, "timestamp": datetime.datetime.now()
                })
                return reply
            return f"⚠ Groq error {res.status_code}: {res.text}"
        except Exception as e:
            return f"❌ Groq call failed: {e}"

    def chat(self):
        print("🤖 Hello! I'm your chatbot (Groq-powered). Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower().strip() == "bye":
                print("Chatbot: Goodbye! 👋")
                break
            print("Chatbot:", self.call_groq(user_input))


# Run It
if __name__ == "__main__":
    bot = SimpleGroqChatbot()
    bot.chat()
