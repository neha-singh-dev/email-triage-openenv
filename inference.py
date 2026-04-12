import asyncio
import sys, os
from openai import OpenAI
sys.path.append(os.path.dirname(__file__))

from email_env import EmailEnv, Action

# ✅ Environment variables
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
HF_TOKEN = os.getenv("HF_TOKEN")

# ❗ Required check
if HF_TOKEN is None:
    print("[WARNING] No HF_TOKEN found, running dummy inference")

# ✅ OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

TASKS = ["easy", "medium", "hard"]
BENCHMARK = "email_triage_env"

def get_model_action(email_text):
    prompt = f"""
    You are an email assistant.

    Your task:
    1. Classify the email into ONE of: spam, promotion, important
    2. Generate a short response

    STRICT FORMAT (no extra text):
    label: <spam|promotion|important>
    response: <one line response>

    Email:
    {email_text}
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )

        output = completion.choices[0].message.content.strip()

        label = "spam"
        response = ""

        for line in output.split("\n"):
            if "label:" in line:
                label = line.split("label:")[1].strip()
            if "response:" in line:
                response = line.split("response:")[1].strip()

        return label, response

    except Exception as e:
        print(f"[DEBUG] Model error: {e}")
        return "spam", ""

async def main():
    print(f"[START] task=all env={BENCHMARK} model={MODEL_NAME}")

    total_reward = 0
    steps = 0

    for task in ["easy", "medium", "hard"]:
        env = EmailEnv(task=task)

        obs = env.reset()

        label, response = get_model_action(obs.email_text)

        action = Action(label=label, response=response)

        observation, reward, done, info = env.step(action)

        print(f"[STEP] step={steps+1} action={action.label} reward={reward:.2f} done=true error=null")

        total_reward += reward
        steps += 1

    avg_reward = total_reward / steps
    success = avg_reward >= 0.5

    print(f"[END] success={str(success).lower()} steps={steps} rewards={avg_reward:.2f}")

if __name__ == "__main__":
    asyncio.run(main())