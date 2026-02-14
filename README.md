# NeuroCourier powered by GuhaGPTbot
# A Telegram AI Agent (Local LLM / Gemini Backend)

<img width="1365" height="1000" alt="Screenshot 2026-02-14 at 8 38 43 PM" src="https://github.com/user-attachments/assets/e534bdb6-8e10-4e3b-b3e4-d9766b7707c8" />
<img width="1479" height="396" alt="Screenshot 2026-02-14 at 8 38 09 PM" src="https://github.com/user-attachments/assets/6e91239e-9296-4549-8e6c-5631bf1220ae" />

## Overview

GuhaGPTbot is a fully functional Telegram-based AI agent that connects Telegram messaging with a Large Language Model backend running either locally (via Ollama) or remotely (via Google's Gemini API). The bot receives messages from Telegram, forwards them to an LLM backend, and replies with intelligent responses in real time.

This project demonstrates how to build a production-grade personal AI assistant integrated with messaging platforms, while maintaining full control over the backend inference.

---

## Aim of the Project

The primary goal of this project is to create a personal AI agent that:

* Runs locally on your machine for privacy and control
* Responds to Telegram messages in real time
* Uses modern Large Language Models
* Supports both local inference (Ollama) and cloud inference (Gemini API)
* Provides a foundation for building advanced autonomous agents

---

## What Has Been Achieved

Successfully implemented:

* Telegram bot creation via BotFather
* Python-based Telegram message handler
* Integration with local LLM using Ollama
* Fully functional message-response loop
* Virtual environment isolation for dependency management
* Production-ready async-safe Telegram bot architecture

System workflow:

```
Telegram User
     │
     ▼
Telegram Bot API
     │
     ▼
Python Bot Backend (bot.py)
     │
     ├── Local LLM via Ollama
     │        OR
     └── Gemini API
     │
     ▼
Response returned to Telegram user
```

---

## Technologies Used

### Core Technologies

* Python 3.13
* Telegram Bot API
* Ollama (Local LLM runtime)
* Google Gemini API (optional cloud backend)

### Python Libraries

* python-telegram-bot
* ollama
* google-generativeai

### Platform

* macOS (development environment)
* Compatible with Linux and Windows

---

## Project Structure

```
telegram-agent/
│
├── bot.py              # Main Telegram bot script
├── venv/               # Python virtual environment
└── README.md          # Project documentation
```

---

## Environment Setup Details

A dedicated Python virtual environment was created to isolate dependencies.

### Virtual Environment Creation

Command used:

```
python3 -m venv venv
```

Activation:

```
source venv/bin/activate
```

This ensures:

* No conflicts with system Python
* Clean dependency management
* Reproducible environment

### Installed Dependencies

Installed inside the virtual environment:

```
pip install python-telegram-bot
pip install ollama
pip install google-generativeai
```

### Environment Isolation Achieved

Environment ensures:

* Controlled package versions
* Safe experimentation
* Clean deployment capability

---

## Ollama Setup

Ollama provides local LLM inference.

Installed and used model:

```
qwen2.5:7b
```

Model pull command:

```
ollama pull qwen2.5:7b
```

Ollama server started using:

```
ollama serve
```

This runs a local LLM server accessible via Python.

---

## Telegram Bot Setup

Bot created using BotFather.

Steps performed:

1. Open Telegram
2. Search: BotFather
3. Run command:

```
/newbot
```

4. Set bot name and username
5. Received API token
6. Integrated token into bot.py

---

## Bot Execution

Run the bot using:

```
source venv/bin/activate
python bot.py
```

Expected output:

```
Bot is running...
```

Bot then listens for Telegram messages continuously.

---

## Backend Options Supported

### Option 1 — Local LLM (Current Implementation)

Advantages:

* Fully private
* No API cost
* Offline capability
* Full control

Uses Ollama runtime.

### Option 2 — Gemini API (Optional)

Advantages:

* Faster responses
* No local GPU required
* Higher model capability

Switch configurable inside bot.py.

---

## Architecture Details

Polling-based Telegram integration used.

Flow:

1. Telegram user sends message
2. Bot receives message
3. Python handler processes input
4. Message sent to LLM
5. Response generated
6. Response returned to Telegram

---

## Key Features Implemented

* Real-time Telegram integration
* Local LLM inference
* Modular backend support
* Secure token-based authentication
* Virtual environment isolation
* Async-safe architecture

---

## Challenges Solved

Resolved issues with:

* Python 3.13 asyncio loop conflicts
* Telegram async execution
* Virtual environment dependency isolation
* Ollama Python client integration

---

## Current Capabilities

GuhaGPTbot can:

* Answer questions
* Explain concepts
* Assist with coding
* Act as personal assistant
* Run fully locally

---

## Future Improvements

Planned enhancements:

* Conversation memory
* Tool execution capability
* File processing
* Voice message support
* Multi-model switching
* Web dashboard
* Autonomous agent functionality

---

## Security and Privacy

Local LLM mode ensures:

* No data leaves your machine
* Complete privacy
* Offline operation possible

---

## How This Helps in AI Engineering

This project demonstrates practical implementation of:

* AI agent architecture
* LLM integration
* Backend development
* API integration
* Real-time messaging systems

---

## Author

Aditya Guha

AI & ML Engineer

---

## Status

Working and fully functional.

Ready for further extension into a full autonomous AI agent.

---

## License

Open for personal and educational use.

---


