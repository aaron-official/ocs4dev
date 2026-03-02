import os
import glob
import gradio as gr
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple, Optional
import uuid
import torch
from huggingface_hub import hf_hub_download
import warnings
warnings.filterwarnings("ignore")

# Updated imports to avoid deprecation warnings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Modern LangChain chains (replacing deprecated ConversationalRetrievalChain)
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Multi-provider LLM support
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Supabase integration (pre-configured by admin)
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client

# Hugging Face Transformers for local Qwen model
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import accelerate

# Configuration
DEFAULT_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct-AWQ"  # Quantized version for better performance on free tier
TOP_K_DOCUMENTS = 5

# Model configurations for each provider
MODEL_CONFIGS = {
    "openai": {
        "budget": "gpt-5.3-codex-mini",
        "premium": "gpt-5.3-codex"
    },
    "anthropic": {
        "budget": "claude-4-6-sonnet",
        "premium": "claude-4-6-opus"
    },
    "google": {
        "budget": "gemini-3-1-flash",
        "premium": "gemini-3-1-pro"
    }
}

# Load environment variables
load_dotenv(override=True)

class OCS4DevAssistant:
    def __init__(self):
        self.setup_environment()
        self.setup_local_model()
        self.setup_vector_store()
        self.chat_history = []
        self.current_provider = "local"
        self.current_model_tier = "budget"

    def setup_environment(self):
        """Setup environment variables - only Supabase required for vector store"""
        # Supabase credentials (pre-configured by admin)
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_KEY')

        if not self.supabase_url or not self.supabase_key:
            print("⚠️  Supabase not configured. Vector search will be disabled.")
            self.supabase_url = None
            self.supabase_key = None

        # API keys (provided by users in UI)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')

    def setup_local_model(self):
        """Initialize the local Qwen2.5-Coder model"""
        print(f"🚀 Loading {DEFAULT_MODEL}...")

        try:
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                DEFAULT_MODEL,
                trust_remote_code=True
            )

            # Load quantized model
            self.local_model = AutoModelForCausalLM.from_pretrained(
                DEFAULT_MODEL,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )

            # Create pipeline for easier inference
            self.local_pipeline = pipeline(
                "text-generation",
                model=self.local_model,
                tokenizer=self.tokenizer,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None,
                max_new_tokens=2048,  # Increased context window
                temperature=0.3,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

            print(f"✅ Local {DEFAULT_MODEL} loaded successfully!")

        except Exception as e:
            print(f"❌ Error loading local model: {e}")
            print("Model will be downloaded on first use...")
            self.local_model = None
            self.local_pipeline = None
            self.tokenizer = None

    def setup_vector_store(self):
        """Initialize vector store for retrieval only"""
        if not self.supabase_url or not self.supabase_key:
            self.vector_store = None
            print("⚠️  Supabase credentials not found. Vector store disabled.")
            print("    To enable, set SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables.")
            return

        try:
            self.supabase_client = create_client(self.supabase_url, self.supabase_key)

            # Test connection and check if data exists
            response = self.supabase_client.table("fintech_api_docs").select("count").execute()
            doc_count = len(response.data) if response.data else 0

            if doc_count == 0:
                print("⚠️  Supabase connected but no documents found in the database.")
                print("    Run the populate_supabase.py tool to add documents first.")
            else:
                print(f"✅ Supabase connected! Documents available: {doc_count}")

            # Use OpenAI embeddings for retrieval
            # Note: This requires a valid OpenAI API key for similarity search
            if self.openai_api_key:
                self.embeddings = OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    openai_api_key=self.openai_api_key
                )
            else:
                print("⚠️  No OpenAI API key found. Using fallback embeddings.")
                print("    For best results, provide an OpenAI API key.")
                # Fallback: still create embeddings object but searches may not work properly
                self.embeddings = OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    openai_api_key="dummy-key"
                )

            # Initialize vector store as retriever only
            self.vector_store = SupabaseVectorStore(
                client=self.supabase_client,
                embedding=self.embeddings,
                table_name="fintech_api_docs",
                query_name="match_documents"
            )

            print("✅ Vector store initialized as retriever!")

        except Exception as e:
            print(f"❌ Vector store setup failed: {e}")
            print("    Ensure your Supabase table 'fintech_api_docs' exists with proper schema.")
            print("    Run the populate_supabase.py tool to set up the database.")
            self.vector_store = None

    def get_llm_instance(self, provider: str, tier: str, api_key: Optional[str] = None):
        """Get LLM instance based on provider and tier"""
        if provider == "local":
            return self.local_pipeline

        if not api_key:
            raise ValueError(f"API key required for {provider}")

        model_name = MODEL_CONFIGS[provider][tier]

        if provider == "openai":
            return ChatOpenAI(
                model=model_name,
                temperature=0.3,
                max_tokens=1000,
                openai_api_key=api_key
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model_name,
                temperature=0.3,
                max_tokens=1000,
                anthropic_api_key=api_key
            )
        elif provider == "google":
            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.3,
                max_output_tokens=1000,
                google_api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate_local_response(self, prompt: str, context: str = "") -> str:
        """Generate response using local Qwen model"""
        if not self.local_pipeline or not self.tokenizer:
            # Try to load model if not loaded
            self.setup_local_model()

        if not self.local_pipeline or not self.tokenizer:
            return "❌ Local model not available. Please use API providers or check your setup."

        # Format prompt for Qwen2.5-Coder
        system_prompt = f"""You are ocs4dev, a specialized fintech API integration assistant. You help developers integrate fintech APIs including MTN MoMo, Pesapal, and Sentezo.

Your expertise includes:
- API authentication and security
- Code examples and implementation
- Error handling and debugging
- Testing and best practices
- Payment gateway integration

Always provide practical, code-focused responses with examples.

Context: {context}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        # Apply chat template
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        try:
            # Generate response
            outputs = self.local_pipeline(
                formatted_prompt,
                max_new_tokens=2048,
                temperature=0.3,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

            # Extract generated text
            response = outputs[0]["generated_text"]

            # Remove the input prompt from response
            if formatted_prompt in response:
                response = response.replace(formatted_prompt, "").strip()

            return response

        except Exception as e:
            return f"❌ Error generating response: {str(e)}"

    def get_retrieval_context(self, query: str) -> str:
        """Get relevant context from vector store"""
        if not self.vector_store:
            return ""

        try:
            docs = self.vector_store.similarity_search(query, k=TOP_K_DOCUMENTS)
            context = "\n\n".join([doc.page_content for doc in docs])
            return context
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return ""

    def create_retrieval_chain(self, llm, provider: str):
        """Create retrieval chain for API models"""
        if not self.vector_store:
            return None

        # Create retriever
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": TOP_K_DOCUMENTS}
        )

        # Contextualize question prompt
        contextualize_q_system_prompt = """
        You are ocs4dev, a fintech API integration expert. Given a chat history and the latest user question
        which might reference context in the chat history, formulate a standalone question
        which can be understood without the chat history. Focus on fintech API integration.

        Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
        """

        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        # Question answering prompt
        qa_system_prompt = """
        You are ocs4dev, a specialized fintech API integration assistant. Use the following context
        to help developers integrate fintech APIs (MTN MoMo, Pesapal, Sentezo, etc.).

        Your responses should:
        1. Be technically accurate and detailed
        2. Include relevant code examples and snippets
        3. Provide step-by-step implementation guidance
        4. Include error handling best practices
        5. Reference specific API endpoints and parameters
        6. Suggest testing approaches

        Format code blocks properly with language specification for syntax highlighting.
        Always provide practical, actionable advice.

        Context: {context}
        """

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # Create document chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        # Create final RAG chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        return rag_chain

    def update_model_config(self, provider: str, tier: str, api_key: str = None):
        """Update current model configuration"""
        self.current_provider = provider
        self.current_model_tier = tier

        if provider != "local" and api_key:
            if provider == "openai":
                self.openai_api_key = api_key
            elif provider == "anthropic":
                self.anthropic_api_key = api_key
            elif provider == "google":
                self.google_api_key = api_key

    def chat(self, message: str, history: List[Tuple[str, str]], provider: str, tier: str, api_key: str = None) -> str:
        """Main chat function - returns full response (streaming handled by Gradio)"""
        try:
            # Update model configuration
            self.update_model_config(provider, tier, api_key)

            if provider == "local":
                # Use local model with context
                context = self.get_retrieval_context(message)
                return self.generate_local_response(message, context)
            else:
                # Use API model
                api_key_map = {
                    "openai": self.openai_api_key,
                    "anthropic": self.anthropic_api_key,
                    "google": self.google_api_key
                }

                current_api_key = api_key or api_key_map.get(provider)
                if not current_api_key:
                    return f"❌ No API key provided for {provider}. Please enter your API key in the settings."

                # Get LLM instance
                llm = self.get_llm_instance(provider, tier, current_api_key)

                # Create retrieval chain
                rag_chain = self.create_retrieval_chain(llm, provider)

                if not rag_chain:
                    # Fallback to simple context if no vector store
                    context = self.get_retrieval_context(message)
                    simple_prompt = f"Context: {context}\n\nQuestion: {message}\n\nProvide a detailed response about fintech API integration."
                    return llm.invoke(simple_prompt).content

                # Convert Gradio history to LangChain format
                chat_history = []
                for human, assistant in history:
                    chat_history.append(HumanMessage(content=human))
                    chat_history.append(AIMessage(content=assistant))

                # Invoke RAG chain
                response = rag_chain.invoke({
                    "input": message,
                    "chat_history": chat_history
                })

                return response["answer"]

        except Exception as e:
            return f"❌ Error processing request: {str(e)}"

def create_gradio_interface():
    """Create the Gradio interface optimized for HuggingFace Spaces"""
    print("🚀 Starting ocs4dev - Your Fintech API Integration Assistant")

    # Initialize assistant
    try:
        assistant = OCS4DevAssistant()
        print("✅ ocs4dev initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize ocs4dev: {e}")
        return None

    # Custom CSS for better styling and copy buttons
    custom_css = """
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
        font-size: 14px;
        color: #856404 !important;
    }
    .model-info {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #1565c0 !important;
    }
    .feature-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #212529 !important;
    }
    .code-block {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 12px;
        margin: 8px 0;
        position: relative;
        font-family: 'Courier New', monospace;
        color: #212529 !important;
    }
    .copy-button {
        position: absolute;
        top: 8px;
        right: 8px;
        background: #007bff;
        color: white;
        border: none;
        padding: 4px 8px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
    }
    .copy-button:hover {
        background: #0056b3;
    }
    /* Hide Gradio footer */
    .footer {
        display: none !important;
    }

    /* Overlay backdrop */
    .sidebar-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
        display: none;
    }

    .sidebar-backdrop.show {
        display: block;
    }

    /* Sidebar as overlay */
    .sidebar-container {
        position: fixed;
        left: 0;
        top: 0;
        height: 100vh;
        width: 400px; /* Wider sidebar for better text display */
        max-width: 90vw; /* Responsive on mobile */
        background: var(--background-fill-primary);
        border-right: 1px solid var(--border-color-primary);
        transform: translateX(-100%);
        transition: transform 0.3s ease;
        z-index: 1000;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 20px;
        padding-top: 60px; /* Space for close button */
        box-sizing: border-box;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }

    .sidebar-container.open {
        transform: translateX(0);
    }

    /* Fix white spaces in sidebar */
    .sidebar-container .gr-form {
        gap: 0 !important;
    }

    .sidebar-container .gr-box {
        border: none !important;
        background: transparent !important;
    }

    .sidebar-container .gr-padded {
        padding: 8px !important;
    }

    .sidebar-container .gr-panel {
        background: var(--background-fill-secondary) !important;
        padding: 12px !important;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    /* Style sidebar content */
    .sidebar-container h2 {
        color: var(--body-text-color) !important;
        margin-bottom: 20px;
        font-size: 1.5rem;
    }

    .sidebar-container .gr-markdown h2 {
        color: var(--body-text-color) !important;
        margin-top: 0;
    }

    /* Remove unwanted white borders and backgrounds */
    .sidebar-container .gradio-container {
        background: transparent !important;
        border: none !important;
    }

    .sidebar-container .gr-form {
        background: transparent !important;
        border: none !important;
        gap: 12px !important;
    }

    .sidebar-container .gr-input-wrapper {
        margin: 0 !important;
    }

    .sidebar-container .gr-group {
        background: var(--background-fill-secondary) !important;
        border: 1px solid var(--border-color-primary) !important;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
    }

    /* Ensure text visibility in sidebar */
    .sidebar-container * {
        color: var(--body-text-color) !important;
    }

    .sidebar-title {
        font-size: 1.5rem !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
        color: var(--body-text-color) !important;
    }

    .sidebar-toggle {
        position: fixed;
        left: 20px;
        top: 20px;
        z-index: 998;
        background: var(--button-primary-background-fill);
        color: var(--button-primary-text-color);
        border: none;
        padding: 12px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 18px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .sidebar-toggle:hover {
        background: var(--button-primary-background-fill-hover);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    .sidebar-close {
        position: absolute;
        right: 20px;
        top: 20px;
        background: transparent;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: var(--body-text-color);
        padding: 5px;
        border-radius: 4px;
        transition: background 0.2s ease;
        z-index: 1001;
    }

    .sidebar-close:hover {
        background: var(--background-fill-secondary);
    }

    /* Main content stays in place */
    .main-content {
        min-height: 100vh;
        padding-left: 70px; /* Space for menu button */
    }

    /* Custom chat styling */
    .chat-container {
        max-width: 100%;
        margin: 0 auto;
        padding: 20px;
    }

    /* Dark mode specific fixes */
    .dark .sidebar-container {
        background: var(--background-fill-primary);
    }

    .dark .warning-box {
        background-color: #2d2d2d;
        border: 1px solid #ffc107;
        color: #ffc107 !important;
    }
    .dark .model-info {
        background-color: #1a1a1a;
        border-left: 4px solid #64b5f6;
        color: #64b5f6 !important;
    }
    .dark .feature-box {
        background-color: #2d2d2d;
        border: 1px solid #495057;
        color: #e9ecef !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .sidebar-container {
            width: 85vw;
        }
        .main-content {
            padding-left: 60px;
        }
    }
    """

    # Create the interface
    def chat_with_config(message, history, provider, tier, openai_key, anthropic_key, google_key):
        """Chat function with configuration"""
        api_key = None
        if provider == "openai":
            api_key = openai_key
        elif provider == "anthropic":
            api_key = anthropic_key
        elif provider == "google":
            api_key = google_key

        return assistant.chat(message, history, provider, tier, api_key)

    # Create interface
    with gr.Blocks(
        title="ocs4dev - Fintech API Assistant",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="gray",
            neutral_hue="slate",
        ),
        css=custom_css,
        fill_height=True,
        js="""
        function() {
            // Add sidebar toggle functionality with backdrop
            const backdrop = document.createElement('div');
            backdrop.className = 'sidebar-backdrop';
            document.body.appendChild(backdrop);

            const toggleButton = document.createElement('button');
            toggleButton.innerHTML = '☰';
            toggleButton.className = 'sidebar-toggle';
            toggleButton.title = 'Open Settings';

            const sidebar = document.querySelector('.sidebar-container');

            // Add close button to sidebar
            const closeButton = document.createElement('button');
            closeButton.innerHTML = '✕';
            closeButton.className = 'sidebar-close';
            closeButton.title = 'Close Settings';
            sidebar.insertBefore(closeButton, sidebar.firstChild);

            function openSidebar() {
                sidebar.classList.add('open');
                backdrop.classList.add('show');
                document.body.style.overflow = 'hidden';
            }

            function closeSidebar() {
                sidebar.classList.remove('open');
                backdrop.classList.remove('show');
                document.body.style.overflow = '';
            }

            toggleButton.onclick = openSidebar;
            closeButton.onclick = closeSidebar;
            backdrop.onclick = closeSidebar;

            // ESC key to close
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                    closeSidebar();
                }
            });

            document.body.appendChild(toggleButton);
        }
        """
    ) as interface:

        # Header
        with gr.Column(elem_classes="main-content"):
            gr.Markdown("# 🏦 ocs4dev - Your Fintech API Integration Assistant")
            gr.Markdown("*Specialized AI assistant for integrating fintech APIs including MTN MoMo, Airtel, Pesapal etc*")

            # Main chat interface
            chatbot = gr.Chatbot(
                height=500,
                placeholder="Ask me about fintech API integration, authentication, code examples, or best practices...",
                label="ocs4dev Assistant",
                show_copy_button=True,  # Enable copy button for chat messages
                render_markdown=True,
                elem_classes="chat-container"
            )

            msg = gr.Textbox(
                placeholder="How do I authenticate with MTN MoMo API?",
                label="Your Question",
                lines=2,
                show_copy_button=True  # Enable copy button for input
            )

            with gr.Row():
                clear = gr.Button("Clear", variant="secondary")
                submit = gr.Button("Send", variant="primary")

            # Example questions
            gr.Examples(
                examples=[
                    "How do I authenticate with MTN MoMo API?",
                    "Show me a Pesapal payment integration example",
                    "What are the required headers for Sentezo API?",
                    "How do I handle payment webhooks?",
                    "Best practices for API error handling",
                    "How to test API integrations in sandbox mode?",
                    "Show me a complete payment flow implementation",
                    "How to secure API keys in production?",
                    "What's the difference between sandbox and production?",
                    "How do I implement payment status callbacks?"
                ],
                inputs=msg,
                label="💡 Example Questions"
            )

        # Sidebar (hidden by default)
        with gr.Column(elem_classes="sidebar-container", elem_id="settings-sidebar"):
            gr.Markdown("## ⚙️ Configuration", elem_classes="sidebar-title")

            # Model provider selection
            with gr.Group():
                provider = gr.Radio(
                    choices=["local", "openai", "anthropic", "google"],
                    value="local",
                    label="Model Provider",
                    info="Local model is free but requires GPU. API models need keys.",
                    elem_classes="provider-selector"
                )

                tier = gr.Radio(
                    choices=["budget", "premium"],
                    value="budget",
                    label="Model Tier",
                    info="Budget models are faster/cheaper, Premium models are more capable",
                    elem_classes="tier-selector"
                )

            # API Keys Section
            with gr.Accordion("🔑 API Keys", open=True, elem_classes="api-keys-section"):
                gr.HTML('<div class="warning-box">⚠️ <strong>Security Warning:</strong> Create test API keys for this app and delete them after use. Never share production keys.</div>')

                with gr.Group():
                    openai_key = gr.Textbox(
                        placeholder="sk-...",
                        label="OpenAI API Key",
                        type="password",
                        info="Budget: gpt-5.3-codex-mini | Premium: gpt-5.3-codex",
                        elem_classes="api-key-input"
                    )

                    anthropic_key = gr.Textbox(
                        placeholder="sk-ant-...",
                        label="Anthropic API Key",
                        type="password",
                        info="Budget: claude-4.6-sonnet | Premium: claude-4.6-opus",
                        elem_classes="api-key-input"
                    )

                    google_key = gr.Textbox(
                        placeholder="AI...",
                        label="Google API Key",
                        type="password",
                        info="Budget: gemini-3.1-flash | Premium: gemini-3.1-pro",
                        elem_classes="api-key-input"
                    )

            # Updated model information
            gr.HTML('<div class="model-info">🚀 <strong>Pro Tip:</strong> Add your API keys above for faster and better responses. Local model works but API models provide superior performance!</div>')

            # Features
            with gr.Accordion("✨ Features", open=False, elem_classes="features-section"):
                gr.HTML('''
                <div class="feature-box">
                    <strong>🔧 Code-Focused:</strong> Optimized for API integration tasks<br>
                    <strong>🔒 Secure:</strong> No API keys stored permanently<br>
                    <strong>📋 Copy-Friendly:</strong> Easy code copying with built-in buttons<br>
                    <strong>🚀 Fast:</strong> Multiple model options for best performance<br>
                    <strong>🔄 Multi-Provider:</strong> Switch between AI models seamlessly
                </div>
                ''')

        # Chat functionality with simple response
        def respond(message, history, provider, tier, openai_key, anthropic_key, google_key):
            """Handle chat responses with simulated streaming"""
            if not message:
                return history, ""

            # Add user message to history
            history = history or []

            # Get the full response
            bot_message = chat_with_config(message, history, provider, tier, openai_key, anthropic_key, google_key)

            # Simulate streaming by yielding partial responses
            partial = ""
            words = bot_message.split(" ")

            # Stream words in chunks for smooth appearance
            chunk_size = 3  # Words per chunk
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i+chunk_size])
                partial += chunk + " "
                yield history + [(message, partial.strip())], ""

            # Final update with complete response
            yield history + [(message, bot_message)], ""

        # Connect the interface
        submit.click(
            respond,
            inputs=[msg, chatbot, provider, tier, openai_key, anthropic_key, google_key],
            outputs=[chatbot, msg]
        )

        msg.submit(
            respond,
            inputs=[msg, chatbot, provider, tier, openai_key, anthropic_key, google_key],
            outputs=[chatbot, msg]
        )

        clear.click(lambda: ([], ""), outputs=[chatbot, msg])

        # Footer
        gr.Markdown("---")
        gr.Markdown("Built with ❤️ by Aaron | Using Qwen2.5-Coder, LangChain, and Gradio | [GitHub](https://github.com/aaron-official/ocs4dev.git)")

    return interface

def populate_knowledge_base_standalone():
    """[DEPRECATED] Use the separate populate_supabase.py tool instead"""
    print("⚠️  This function is deprecated!")
    print("    Please use the separate 'populate_supabase.py' tool to populate the vector database.")
    print("    ")
    print("    Usage:")
    print("    $ python populate_supabase.py --knowledge-base ./knowledge-base")
    print("    ")
    print("    The tool will:")
    print("    1. Load all markdown files from your knowledge base directory")
    print("    2. Split them into chunks for better retrieval")
    print("    3. Generate embeddings using OpenAI")
    print("    4. Store everything in your Supabase vector database")
    print("    ")
    print("    Make sure you have set these environment variables:")
    print("    - SUPABASE_URL")
    print("    - SUPABASE_SERVICE_KEY")
    print("    - OPENAI_API_KEY")
    return False

def main():
    """Main function optimized for HuggingFace Spaces"""
    interface = create_gradio_interface()
    if interface:
        # HuggingFace Spaces optimized launch
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,  # Enable public URL for HF Spaces
            inbrowser=False,  # Don't open browser in server environment
            show_error=True,
            quiet=False,
            max_threads=10  # Limit concurrent requests
        )

if __name__ == "__main__":
    main()