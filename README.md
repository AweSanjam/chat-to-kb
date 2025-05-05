# 💬 GPT-Powered Knowledge Base Discord Bot

This project is a smart, self-improving **Discord support bot** that uses OpenAI’s GPT models to answer user questions, tag issues, and build a living knowledge base over time. It is built for **technical support teams**, **communities**, and anyone who handles repeat questions.

> ⚡ Automatically learns from unknown questions  
> 🤖 Replies with answers from a JSON-based knowledge base  
> 🏷️ Tags issues using GPT when no answer is found  
> 🧠 Trains itself with `chat_to_kb.py` to grow smarter

---

## 🔧 Key Features

### ✅ Discord Bot (`bot.py`)
- Accepts user questions via `!ask your question here`
- Checks for the best match from `kb_output.json`
- If found, responds with:
  - 🧠 Answer
  - 🏷️ Tags
- If **not** found:
  - Uses GPT to **auto-tag** the question
  - Logs it to `unanswered.json` for future learning
  - Notifies the user it's being "trained"

### 🧠 Knowledge Base Trainer (`chat_to_kb.py`)
- Reads `unanswered.json`
- Uses GPT to generate:
  - Clean answers
  - Tags
- Appends new Q&A entries to `kb_output.json`
- Clears the log to avoid duplicates

---

## 📦 Project Structure

```
chat-to-kb/
├── bot.py                # Discord bot script
├── chat_to_kb.py         # GPT-based knowledge base generator
├── support_chat.txt      # Optional raw logs for manual KB seeding
├── kb_output.json        # Active knowledge base (used by the bot)
├── unanswered.json       # Log of new questions (auto-cleared after training)
├── .env                  # Stores API keys (not committed)
├── .gitignore
├── requirements.txt
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

```
OPENAI_API_KEY=your_openai_key
DISCORD_TOKEN=your_discord_bot_token
```

### 3. Start the Discord bot

```bash
python bot.py
```

Ask a question in any channel:

```
!ask How do I reset my password?
```

### 4. Train on new questions

Run this periodically to update your KB from `unanswered.json`:

```bash
python chat_to_kb.py
```

---

## 🧠 Example Use Case

User asks:

```
!ask Why am I getting a 403 error when logging in?
```

Bot responds (if found in KB):

```
🧠 Answer: This usually means your IP address was blocked. Try restarting your router.
🏷️ Tags: login, 403, network
```

If it's **not found**, bot says:

```
🤔 No match found. Tagging the question...
🏷️ Tagged as: login, permissions
📝 Logged for future training!
```

---

## 💬 Discord Capabilities

- 💬 **Real-time Q&A** inside any Discord server
- 🔍 GPT-enhanced **search and tagging**
- 🧠 Learns from unanswered questions
- 🧰 Can be easily integrated into **community support**, **IT channels**, or **student help desks**
- 🔁 Fully customizable knowledge base (`kb_output.json`)

---

## 🔄 Slack Integration Potential

This architecture can easily be extended to Slack:

- Replace `discord.py` with `slack_bolt` or `slack_sdk`
- Trigger responses based on channel messages
- Reuse the same GPT logic and KB structure
- Slack-compatible version coming soon 😉

---

## 🛡️ Security Notes

- Store API keys safely in `.env`
- `.env` is included in `.gitignore`
- Do **not** commit your OpenAI or Discord tokens

---

## 📜 License

MIT – open to use, share, remix, and enhance.

---

## 🤝 Contributions Welcome!

Want to add:
- A web dashboard?
- Slack or Telegram support?
- Markdown/Notion export for the KB?

Feel free to fork and PR — or open an issue!

---

## 🌟 Final Thoughts

This project blends **LLM power + automation + real-world support workflows**. It’s designed to impress recruiters, automate support channels, and grow with your users.  
You're not just answering questions. You're training your own AI helpdesk. 🧠💼
