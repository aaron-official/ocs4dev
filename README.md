---
title: ocs4dev - Fintech API Integration Assistant
emoji: 🏦
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "6.8.0"
app_file: app.py
pinned: false
---

# 🏦 ocs4dev — Fintech API Integration Assistant

Your AI-powered fintech integration partner. Specialized AI for **Stripe, PayPal, Square, Adyen, MTN MoMo, Pesapal, Sentezo (Ssentezo)** and more. Powered by **local FAISS RAG** — no cloud database required.

## Features

- 🔍 **Local RAG** — FAISS vector search over bundled documentation
- 🤖 **Multi-Model** — Support for OpenAI GPT-5, Anthropic Claude 4, Google Gemini 2.5, and local Qwen 1.5B
- 📋 **Code-Focused** — Senior-level engineering answers with copy-paste-ready code
- 🔒 **Secure** — API keys entered at runtime, never stored on the server
- 🚀 **HF Spaces Ready** — CPU-optimized deployment for the free tier

## Supported Ecosystems

- **Global**: Stripe, PayPal, Square, Adyen, Mollie, Razorpay
- **African**: MTN MoMo, Pesapal, Ssentezo, Airtel Money, Flutterwave, Paystack

## Model Options (March 2026)

| Provider | Budget | Premium |
|---|---|---|
| **Google** ⭐ | Gemini 2.0 Flash | Gemini 2.5 Pro |
| **OpenAI** | GPT-5 mini | GPT-5.2 |
| **Anthropic** | Claude Haiku 4.5 | Claude Opus 4.6 |
| **Local** | Qwen2.5-Coder-1.5B | — |

## Quick Start

1. Visit the Space URL
2. Choose a model in the **⚙️ Settings** panel
3. Add your API key (or use the free local model)
4. Start asking questions!

## Self-Hosting / Development

```bash
# Install dependencies (using uv recommended)
uv pip install -r requirements.txt

# Start the app
uv run python app.py
```

## Technical Stack

- **Frontend**: Gradio 6.8.0
- **LLM Framework**: LangChain (LCEL)
- **Vector Store**: FAISS (local index)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Local Model**: Qwen2.5-Coder-1.5B-Instruct

---
Built with ❤️ by Aaron