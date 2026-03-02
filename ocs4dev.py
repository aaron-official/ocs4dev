import os
import glob
import gradio as gr
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple, Optional
import uuid
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

# Modern LangChain chains
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Multi-provider LLM support
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint

# Supabase integration
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client

# Configuration
DEFAULT_FREE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
TOP_K_DOCUMENTS = 5

# Model configurations for each provider
MODEL_CONFIGS = {
    "openai": {
        "budget": "gpt-5.3-codex-mini",
        "premium": "gpt-5.3-codex"
    },
    "anthropic": {
        "budget": "claude-4.6-sonnet",
        "premium": "claude-4.6-opus"
    },
    "google": {
        "budget": "gemini-3.1-flash",
        "premium": "gemini-3.1-pro"
    }
}

# Load environment variables
load_dotenv(override=True)

class OCS4DevAssistant:
    def __init__(self):
        self.setup_environment()
        self.setup_vector_store()
        self.chat_history = []
        self.current_provider = "free"
        self.current_model_tier = "budget"

    def setup_environment(self):
        """Setup environment variables"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        self.hf_token = os.getenv('HF_TOKEN') # For Inference API

        # API keys (provided by users in UI)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')

    def setup_vector_store(self):
        """Initialize vector store for retrieval only"""
        if not self.supabase_url or not self.supabase_key:
            self.vector_store = None
            return

        try:
            self.supabase_client = create_client(self.supabase_url, self.supabase_key)
            
            # Use OpenAI embeddings for retrieval
            if self.openai_api_key:
                self.embeddings = OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    openai_api_key=self.openai_api_key
                )
            else:
                self.embeddings = OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    openai_api_key="dummy-key"
                )

            self.vector_store = SupabaseVectorStore(
                client=self.supabase_client,
                embedding=self.embeddings,
                table_name="fintech_api_docs",
                query_name="match_documents"
            )
        except Exception as e:
            print(f"❌ Vector store setup failed: {e}")
            self.vector_store = None

    def get_llm_instance(self, provider: str, tier: str, api_key: Optional[str] = None):
        """Get LLM instance based on provider and tier"""
        if provider == "free":
            return HuggingFaceEndpoint(
                repo_id=DEFAULT_FREE_MODEL,
                huggingfacehub_api_token=self.hf_token or api_key,
                temperature=0.3,
                max_new_tokens=1024,
                timeout=300
            )

        if not api_key:
            raise ValueError(f"API key required for {provider}")

        model_name = MODEL_CONFIGS[provider][tier]

        if provider == "openai":
            return ChatOpenAI(model=model_name, temperature=0.3, max_tokens=1000, openai_api_key=api_key)
        elif provider == "anthropic":
            return ChatAnthropic(model=model_name, temperature=0.3, max_tokens=1000, anthropic_api_key=api_key)
        elif provider == "google":
            return ChatGoogleGenerativeAI(model=model_name, temperature=0.3, max_output_tokens=1000, google_api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate_free_response(self, prompt: str, context: str = "") -> str:
        """Generate response using HF Inference API"""
        llm = self.get_llm_instance("free", "budget")
        
        system_prompt = f"""You are ocs4dev, a specialized fintech API integration assistant. You help developers integrate fintech APIs including MTN MoMo, Pesapal, and Sentezo.
Provide practical, code-focused responses with examples.
Context: {context}"""

        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        
        try:
            return llm.invoke(full_prompt)
        except Exception as e:
            return f"❌ Error from Inference API: {str(e)}"

    def get_retrieval_context(self, query: str) -> str:
        """Get relevant context from vector store"""
        if not self.vector_store:
            return ""
        try:
            docs = self.vector_store.similarity_search(query, k=TOP_K_DOCUMENTS)
            return "\n\n".join([doc.page_content for doc in docs])
        except:
            return ""

    def create_retrieval_chain(self, llm, provider: str):
        """Create retrieval chain for API models"""
        if not self.vector_store:
            return None

        retriever = self.vector_store.as_retriever(search_kwargs={"k": TOP_K_DOCUMENTS})

        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", "Formulate a standalone question based on history."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are ocs4dev, a fintech API expert. Context: {context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        return create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def chat(self, message: str, history: List[Tuple[str, str]], provider: str, tier: str, api_key: str = None) -> str:
        """Main chat function"""
        try:
            if provider == "free":
                context = self.get_retrieval_context(message)
                return self.generate_free_response(message, context)
            
            # Update API key
            if api_key:
                if provider == "openai": self.openai_api_key = api_key
                elif provider == "anthropic": self.anthropic_api_key = api_key
                elif provider == "google": self.google_api_key = api_key

            if not api_key and not getattr(self, f"{provider}_api_key"):
                return f"❌ No API key provided for {provider}."

            llm = self.get_llm_instance(provider, tier, api_key or getattr(self, f"{provider}_api_key"))
            rag_chain = self.create_retrieval_chain(llm, provider)

            if not rag_chain:
                context = self.get_retrieval_context(message)
                return llm.invoke(f"Context: {context}\n\nQuestion: {message}").content

            chat_history = []
            for human, assistant in history:
                chat_history.extend([HumanMessage(content=human), AIMessage(content=assistant)])

            response = rag_chain.invoke({"input": message, "chat_history": chat_history})
            return response["answer"]
        except Exception as e:
            return f"❌ Error: {str(e)}"

def create_gradio_interface():
    """Create the Gradio interface with a professional, modern layout."""
    print("🚀 Starting ocs4dev - Your Fintech API Integration Assistant")

    try:
        assistant = OCS4DevAssistant()
    except Exception as e:
        print(f"❌ Failed to initialize ocs4dev: {e}")
        return None

    custom_css = """
    #main-container { display: flex; flex-direction: row; width: 100%; height: 100vh; overflow: hidden; }
    #chat-container { flex: 3; display: flex; flex-direction: column; height: 100%; padding: 20px; box-sizing: border-box; }
    #sidebar-container { flex: 1; min-width: 350px; max-width: 400px; padding: 20px; border-left: 1px solid var(--border-color-primary); background: var(--background-fill-secondary); transition: all 0.3s ease; overflow-y: auto; height: 100%; box-sizing: border-box; }
    #header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    #chatbot { flex-grow: 1; overflow-y: auto; border: 1px solid var(--border-color-primary); border-radius: 8px; background-color: var(--background-fill-primary); box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    #chat-input-container { margin-top: 20px; }
    .gradio-container { background: var(--background-fill-primary) !important; }
    .footer { display: none !important; }
    .warning-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 12px; margin: 10px 0; color: #856404 !important; border-radius: 8px; }
    .dark .warning-box { background-color: #2d2d2d; border-color: #ffc107; color: #ffc107 !important; }
    """

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="slate", secondary_hue="blue"), css=custom_css, title="ocs4dev - Fintech API Assistant", fill_height=True) as interface:
        sidebar_state = gr.State(True)

        with gr.Row(elem_id="main-container"):
            with gr.Column(elem_id="chat-container"):
                with gr.Row(elem_id="header"):
                    with gr.Column():
                        gr.Markdown("# 🏦 ocs4dev")
                        gr.Markdown("Your Fintech API Integration Assistant")
                    toggle_sidebar_btn = gr.Button("⚙️ Settings", variant="secondary", size="sm")

                chatbot = gr.Chatbot(elem_id="chatbot", show_label=False)

                with gr.Column(elem_id="chat-input-container"):
                    msg = gr.Textbox(placeholder="e.g., How do I authenticate with the MTN MoMo API?", show_label=False, lines=3)
                    with gr.Row():
                        clear = gr.Button("Clear", variant="secondary")
                        submit = gr.Button("Send", variant="primary")

                with gr.Accordion("💡 Example Questions", open=False):
                    gr.Examples(examples=["How do I authenticate with MTN MoMo API?", "Show me a Pesapal payment integration example", "What are the required headers for Sentezo API?"], inputs=msg)

            with gr.Column(visible=True, elem_id="sidebar-container") as sidebar:
                gr.Markdown("## Configuration")
                with gr.Group():
                    provider = gr.Radio(choices=["free", "openai", "anthropic", "google"], value="free", label="Model Provider", info="Free tier uses HF Serverless Inference API.")
                    tier = gr.Radio(choices=["budget", "premium"], value="budget", label="Model Tier", info="Budget models are faster, Premium are more capable.")

                with gr.Accordion("🔑 API Keys", open=True):
                    gr.HTML('<div class="warning-box">⚠️ Never share production keys. For the free tier, you can provide an HF Token for higher rate limits.</div>')
                    hf_token = gr.Textbox(placeholder="hf_...", label="Hugging Face Token (Optional)", type="password")
                    openai_key = gr.Textbox(placeholder="sk-...", label="OpenAI API Key", type="password")
                    anthropic_key = gr.Textbox(placeholder="sk-ant-...", label="Anthropic API Key", type="password")
                    google_key = gr.Textbox(placeholder="AI...", label="Google API Key", type="password")

        def respond(message, history, provider, tier, hf_token, openai_key, anthropic_key, google_key):
            if not message: return history, ""
            history = history or []
            # Map keys to the chat function
            api_key = hf_token if provider == "free" else (openai_key if provider == "openai" else (anthropic_key if provider == "anthropic" else google_key))
            bot_message = assistant.chat(message, history, provider, tier, api_key)
            history.append((message, bot_message))
            return history, ""

        submit.click(respond, inputs=[msg, chatbot, provider, tier, hf_token, openai_key, anthropic_key, google_key], outputs=[chatbot, msg])
        msg.submit(respond, inputs=[msg, chatbot, provider, tier, hf_token, openai_key, anthropic_key, google_key], outputs=[chatbot, msg])
        clear.click(lambda: ([], ""), outputs=[chatbot, msg])

        def toggle_sidebar(is_visible): return gr.update(visible=not is_visible), not is_visible
        toggle_sidebar_btn.click(toggle_sidebar, inputs=[sidebar_state], outputs=[sidebar, sidebar_state])
        
        gr.Markdown("---")
        gr.Markdown("Built by Repol | Powered by OpenClaw")

    return interface

def main():
    interface = create_gradio_interface()
    if interface:
        interface.launch(server_name="0.0.0.0", server_port=7860, share=True, show_error=True)

if __name__ == "__main__":
    main()
