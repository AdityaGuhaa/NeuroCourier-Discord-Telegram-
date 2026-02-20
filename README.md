# NeuroCourier (GuhaGPT) 
# A Multiplatform Multimodal AI Assistant

NeuroCourier (GuhaGPT) is a privacy‑first, multiplatform, multimodal AI assistant developed by Aditya Guha. It supports both Telegram and Discord simultaneously and is powered by locally hosted Large Language Models using Ollama.

NeuroCourier can understand text and images, generate intelligent responses, and operate across multiple communication platforms while sharing a single unified AI backend.

# Overview

NeuroCourier is designed with a modular architecture that separates the AI logic from platform-specific integrations. This allows the same AI brain to power multiple interfaces such as:

* Telegram Bot
* Discord Bot
* Future support: WhatsApp, Web UI, APIs, Slack, etc.

The assistant runs locally, ensuring:

* Full privacy
* No external API dependency
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
* Image input
* Image analysis
* Contextual reasoning

Powered by vision-capable LLMs such as:
Example:
* qwen3-vl:2b

## Local LLM Inference

Runs entirely locally using Ollama.

Benefits:

* Privacy‑first
* No cloud dependency
* No API costs
* Offline capability

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
Local LLM Model (qwen3-vl:2b)
```

# Project Structure

```
NeuroCourier/
│
├── bot.py
├── discord_bot.py
├── llm_backend.py
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
* Receiving Telegram images
* Sending responses
* Platform-specific formatting

Delegates AI tasks to llm_backend.py

Does NOT contain AI logic.

## discord_bot.py (Discord Interface)

Handles:

* Receiving Discord messages
* Receiving Discord image attachments
* Sending responses

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

Step 1:

User sends message via Telegram or Discord.

Step 2:

Platform bot receives message.

Step 3:

Bot calls:

```
run_llm()
```

from llm_backend.py

Step 4:

llm_backend communicates with Ollama.

Step 5:

Ollama runs the model and generates response.

Step 6:

Response is sent back to user.

# Concurrency Handling

Multiple users across platforms can send requests simultaneously.

The backend uses asynchronous execution.

Ollama safely queues requests.

System remains stable.

# Requirements

## Software

* Python 3.10+
* Ollama
* Telegram Bot Token
* Discord Bot Token

## Python Libraries

Install:

```
pip install python-telegram-bot discord.py ollama
```

# Setup Instructions

## Step 1 — Install Ollama

Install from:

[https://ollama.com](https://ollama.com)

## Step 2 — Pull Model

```
ollama pull qwen3-vl:2b
```

---

## Step 3 — Configure Tokens

In bot.py:

```
TELEGRAM_BOT_TOKEN = "YOUR_TOKEN"
```

In discord_bot.py:

```
DISCORD_TOKEN = "YOUR_TOKEN"
```

## Step 4 — Run Bots

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

NeuroCourier runs locally.

No external data sharing.

No cloud dependency.

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

Developer of NeuroCourier (GuhaGPT)

# License

This project is for educational and development purposes.

# Summary

NeuroCourier is a scalable, modular, privacy‑focused AI assistant capable of operating across multiple platforms using a unified local AI backend.

This architecture enables professional‑grade extensibility while maintaining simplicity and full local control.
