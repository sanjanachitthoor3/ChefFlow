import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

# Use OpenRouter endpoint
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

class CookingAssistant:
    def __init__(self, recipe_data):
        self.recipe_data = recipe_data
        self.steps = recipe_data.get("steps", [])
        self.current_step = 0
        self.history = []

    def get_system_prompt(self):
        numbered_steps = "\n".join([f"{i+1}. {s}" for i, s in enumerate(self.steps)])
        return (
            "You are a friendly cooking assistant. You know this recipe:\n\n"
            f"Title: {self.recipe_data.get('title')}\n\n"
            f"Steps:\n{numbered_steps}\n\n"
            "Your job is to help the user cook step by step. "
            "If they ask 'what now', 'next', or similar, give them the next step. "
            "If they say 'repeat', repeat the last step. "
            "If they greet you, greet them back warmly. "
            "Be conversational, natural, and helpful."
        )

    def respond(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": self.get_system_prompt()}] + self.history

        try:
            completion = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=messages,
                extra_headers={
                    "HTTP-Referer": "https://yourprojectsite.com",  # optional
                    "X-Title": "ChefFlow",                          # optional
                }
            )
            answer = completion.choices[0].message.content.strip()
        except Exception as e:
            answer = f"Error talking to OpenRouter: {str(e)}"

        self.history.append({"role": "assistant", "content": answer})
        return answer
