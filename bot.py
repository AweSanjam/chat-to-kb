import discord
import json
import os
import openai
import difflib
from datetime import datetime
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# === File paths ===
KB_FILE = "kb_output.json"
UNANSWERED_LOG = "unanswered.json"

# === Load the knowledge base ===
def load_kb():
    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

knowledge_base = load_kb()

# === Search KB for best match ===
def find_best_answer(question):
    questions = [entry["question"] for entry in knowledge_base]
    match = difflib.get_close_matches(question, questions, n=1, cutoff=0.5)
    if match:
        for entry in knowledge_base:
            if entry["question"] == match[0]:
                return entry["answer"], entry["tags"]
    return None, None

# === Use GPT to tag the new question ===
def gpt_tag_question(question):
    prompt = f"""
You are a support assistant. Categorize the user's question with 2–3 relevant tags.

Question: "{question}"

Respond with only a JSON list of tags.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Tagging error: {e}")
        return ["general"]

# === Log unknown questions to unanswered.json ===
def log_unanswered(question, tags):
    entry = {
        "question": question,
        "tags": tags,
        "timestamp": datetime.now().isoformat()
    }
    try:
        data = []
        if os.path.exists(UNANSWERED_LOG):
            with open(UNANSWERED_LOG, "r", encoding="utf-8") as f:
                data = json.load(f)
        data.append(entry)
        with open(UNANSWERED_LOG, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("📝 Logged unanswered question.")
    except Exception as e:
        print(f"Logging error: {e}")

# === Discord bot setup ===
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask"):
        question = message.content[5:].strip()
        if not question:
            await message.channel.send("❓ Ask a question after `!ask`.")
            return

        await message.channel.send("🔍 Searching the knowledge base...")
        answer, tags = find_best_answer(question)

        if answer:
            await message.channel.send(f"🧠 **Answer:** {answer}\n🏷️ Tags: {', '.join(tags)}")
        else:
            await message.channel.send("🤔 No match found. Tagging the question...")
            tags = gpt_tag_question(question)
            log_unanswered(question, tags)
            await message.channel.send(f"🏷️ Tagged as: {', '.join(tags)}\n📝 Logged for training.")
