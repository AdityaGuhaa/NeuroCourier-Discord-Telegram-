# NeuroCourier (GuhaGPT) 
# A Multiplatform Multimodal AI Assistant

NeuroCourier (GuhaGPT) is a privacy‑first, multiplatform, multimodal AI assistant developed by Aditya Guha. It supports both Telegram and Discord simultaneously and is powered by locally hosted or cloud hosted Large Language Models using Ollama.

NeuroCourier can understand text and images, generate intelligent responses, and operate across multiple communication platforms while sharing a single unified AI backend.

# Discord
<img width="600" alt="Screenshot 2026-05-09 at 10 17 53 PM" src="https://github.com/user-attachments/assets/f6d2241c-88ac-40e0-bcf2-3ee5b3176656" />

## Discord Backend
<img width="600" alt="Screenshot 2026-05-09 at 10 16 30 PM" src="https://github.com/user-attachments/assets/a69fb523-bf88-41bc-a444-815698de6346" />

# Telegram
<img width="600" alt="Screenshot 2026-05-09 at 10 17 28 PM" src="https://github.com/user-attachments/assets/09aab092-a336-4df8-9b58-fe88226addaa" />

## Telegram Backend
<img width="600" alt="Screenshot 2026-05-09 at 10 17 00 PM" src="https://github.com/user-attachments/assets/007ae222-6e2b-4c25-9983-59c3fcf365c6" />

# Overview

NeuroCourier is designed with a modular architecture that separates the AI logic from platform-specific integrations. This allows the same AI brain to power multiple interfaces such as:

* Telegram Bot
* Discord Bot
* Future support: WhatsApp, Web UI, APIs, Slack, etc.

The assistant runs locally or via cloud-routed Ollama models, ensuring:

* Full privacy
* Low latency
* Full control over models

# Key Features

## Multiplatform Support

Supports both Telegram and Discord simultaneously using a shared backend.

Users can interact with NeuroCourier from:

* Telegram chats
* Discord servers
* Discord direct messages

All platforms use the same AI instance.

## Multimodal Capabilities

Supports:

* Text input
* Image input with optional caption/question
* Image analysis
* Contextual reasoning

Powered by vision-capable LLMs via Ollama. Examples:

* `qwen3-vl:2b` (local)
* `qwen3-vl:235b-cloud` (cloud-routed)
* `gemma4:31b-cloud` (cloud-routed)
* `gpt-oss:120b-cloud` (cloud-routed)

## Local & Cloud LLM Inference

Runs via Ollama — supporting both local models and cloud-routed models.

Benefits:

* Privacy‑first
* Flexible model selection
* Offline capability with local models
* Access to larger models via cloud routing

## Unified Backend Architecture

Single backend handles all AI logic.

This ensures:

* Code reuse
* Clean architecture
* Easy scalability
* Platform independence

## Concurrent Platform Handling

Both Telegram and Discord bots can run simultaneously.

Requests are handled asynchronously and safely queued.

# Architecture

```
Users
  │
  ├── Telegram Bot (bot.py)
  │
  ├── Discord Bot (discord_bot.py)
  │
  ▼
Shared AI Backend (llm_backend.py)
  │
  ▼
Ollama
  │
  ▼
Local or Cloud LLM Model
```

# Project Structure

```
NeuroCourier/
│
├── bot.py
├── discord_bot.py
├── llm_backend.py
├── .env               (not committed — store your tokens here)
├── .env.example       (template)
├── data/
├── requirements.txt
└── README.md
```

# File Responsibilities

## llm_backend.py

Core AI brain.

Handles:

* Communication with Ollama
* Model inference
* Prompt handling
* Image handling
* Output processing
* Logging

This file is shared across all platforms.

This is the most important component.

## bot.py (Telegram Interface)

Handles:

* Receiving Telegram messages
* Receiving Telegram images with optional captions
* Sending responses with chunking for long replies
* Platform-specific formatting

Delegates AI tasks to llm_backend.py

Does NOT contain AI logic.

## discord_bot.py (Discord Interface)

Handles:

* Receiving Discord messages
* Receiving Discord image attachments with optional text
* Sending responses with chunking for Discord's 2000 character limit

Delegates AI tasks to llm_backend.py

Does NOT contain AI logic.

## data/

Stores temporary image files received from users.

Used for image analysis.

# Major Improvement Over Previous Telegram‑Only Bot

Previously:

```
Telegram Bot
   │
   ▼
Embedded AI logic inside bot.py
   │
   ▼
Ollama
```

Problems:

* AI logic tightly coupled to Telegram
* Difficult to add Discord
* Code duplication required
* Poor scalability
* Not modular

Now (Current Architecture):

```
Telegram Bot ─┐
              │
Discord Bot ──┼──► Shared Backend ───► Ollama
              │
Future Bots ──┘
```

Benefits:

* Clean separation of concerns
* Platform‑independent AI backend
* Easy to add new platforms
* No duplication
* Professional architecture

# Differences from Previous Telegram Bot

| Feature               | Old Telegram Bot    | NeuroCourier Current Version |
| --------------------- | ------------------- | ---------------------------- |
| Platform Support      | Telegram only       | Telegram + Discord           |
| Architecture          | Monolithic          | Modular                      |
| AI Logic Location     | Inside Telegram bot | Separate backend             |
| Scalability           | Poor                | Excellent                    |
| Code Maintainability  | Low                 | High                         |
| Extensibility         | Difficult           | Easy                         |
| Platform Independence | No                  | Yes                          |

# How It Works

Step 1: User sends message (text or image) via Telegram or Discord.

Step 2: Platform bot receives message.

Step 3: Bot calls `run_llm()` from llm_backend.py

Step 4: llm_backend communicates with Ollama.

Step 5: Ollama runs the model and generates response.

Step 6: Response is chunked if necessary and sent back to user.

# Concurrency Handling

Multiple users across platforms can send requests simultaneously.

The backend uses asynchronous execution.

Ollama safely queues requests.

System remains stable.

# Requirements

## Software

* Python 3.10+
* Ollama
* Telegram Bot Token (from @BotFather)
* Discord Bot Token (from Discord Developer Portal)

## Python Libraries

```
pip install -r requirements.txt
```

# Setup Instructions

## Step 1 — Install Ollama

Install from: [https://ollama.com](https://ollama.com)

## Step 2 — Pull a Model

```
ollama pull qwen3-vl:2b
```

## Step 3 — Configure Tokens

Create a `.env` file in the project root:

```
TELEGRAM_BOT_TOKEN=your_telegram_token_here
DISCORD_TOKEN=your_discord_token_here
```

Never commit this file. It is already listed in `.gitignore`.

## Step 4 — Configure Model

In `llm_backend.py`, set your preferred model:

```python
MODEL_NAME = "qwen3-vl:2b"
```

## Step 5 — Run Bots

Terminal 1:

```
python bot.py
```

Terminal 2:

```
python discord_bot.py
```

Both will run simultaneously.

# Security and Privacy

NeuroCourier runs locally via Ollama.

Tokens are stored in `.env` and never committed to version control.

No external data sharing unless a cloud-routed model is used.

User data remains private.

# Scalability

Current version supports:

* Multiple users
* Multiple platforms

Future upgrades possible:

* FastAPI backend
* Web interface
* WhatsApp integration
* vLLM backend
* GPU optimization

# Future Roadmap

Planned improvements:

* Mention‑based Discord responses
* Conversation memory
* Streaming responses
* Web dashboard
* Multi‑model support
* GPU acceleration via vLLM

# Author

Aditya Guha

AI & Machine Learning Developer

[linktr.ee/adityaguha](https://linktr.ee/adityaguha)

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Summary

NeuroCourier is a scalable, modular, privacy‑focused AI assistant capable of operating across multiple platforms using a unified local AI backend.

This architecture enables professional‑grade extensibility while maintaining simplicity and full local control.
