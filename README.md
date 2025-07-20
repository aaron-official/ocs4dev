---
title: ocs4dev - Fintech API Integration Assistant
emoji: 🏦
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.31.0"
app_file: app.py
pinned: false
---

# 🏦 ocs4dev - Fintech API Integration Assistant

## Overview
ocs4dev is a specialized AI assistant designed to help developers integrate fintech APIs including MTN MoMo, Pesapal, Airtel,Sentezo etc. It provides code examples, implementation guidance, and best practices for payment gateway integration.

## Features
- 🔧 **Code-Focused**: Optimized for API integration tasks with practical examples
- 🤖 **Multi-Model Support**: Choose between local Qwen2.5-Coder or API models (OpenAI, Anthropic, Google)
- 🔒 **Secure**: No API keys stored permanently
- 📋 **Copy-Friendly**: Built-in code copying functionality
- 🚀 **Fast**: Multiple model options for optimal performance
- 🔄 **RAG-Powered**: Retrieves relevant documentation from vector database

## Supported APIs
- **MTN MoMo**: Mobile money integration
- **Airtel API**: Airtel api integration
- **Pesapal**: Payment gateway services
- **Sentezo**: Mobile payment platform
- And more fintech APIs...

## Model Options

### Local Model (Free)
- **Qwen2.5-Coder-7B-Instruct-AWQ**: Quantized model optimized for code generation
- Requires GPU for best performance
- No API key needed

### API Models
- **OpenAI**: GPT-4o-mini (budget) / O4-mini (premium)
- **Anthropic**: Claude-3.5-Sonnet / Claude-4-Sonnet
- **Google**: Gemini-2.0-Flash / Gemini-2.0-Flash-Thinking

## Quick Start
1. Visit the [Space URL](https://huggingface.co/spaces/YOUR_USERNAME/ocs4dev)
2. Choose your preferred model provider
3. Add API keys if using cloud models
4. Start asking questions about fintech API integration!

## Example Questions
- "How do I authenticate with MTN MoMo API?"
- "Show me a Pesapal payment integration example"
- "What are the required headers for Sentezo API?"
- "How do I handle payment webhooks?"
- "Best practices for API error handling"

## Environment Variables
For self-hosting, set these environment variables:
```bash
# Supabase (for vector store)
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-service-key

# API Keys (optional)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
```

## Technical Stack
- **Frontend**: Gradio
- **LLM Framework**: LangChain
- **Vector Store**: Supabase
- **Models**: Qwen2.5-Coder, OpenAI, Anthropic, Google
- **Embeddings**: OpenAI text-embedding-3-small

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.

## Support
For issues or questions, please open an issue on GitHub or contact me.

---
Built with ❤️ using Qwen2.5-Coder, LangChain, and Gradio