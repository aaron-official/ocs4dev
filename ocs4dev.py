"""
ocs4dev.py — Fintech API Integration Assistant
================================================
A RAG-powered chatbot for payment API integrations: Stripe, PayPal,
MTN MoMo, Pesapal, Sentezo, Square, Adyen & more.
Uses a local FAISS vector store (no cloud DB required) and supports
multiple LLM providers: Local Qwen, OpenAI, Anthropic, Google Gemini.
"""

import os
import threading
import warnings
import gradio as gr
from dotenv import load_dotenv
from typing import List, Tuple, Generator

import torch
warnings.filterwarnings("ignore")

# LangChain core (LCEL — works in LangChain 1.x)
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Multi-provider LLM support
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Local vector store (FAISS replaces Supabase)
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Local model inference
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextIteratorStreamer,
)

# Load environment variables
load_dotenv(override=True)

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────
LOCAL_MODEL_ID  = "Qwen/Qwen2.5-Coder-1.5B-Instruct"   # ~3 GB RAM (FP16) - Best for CPU/HF Spaces
FAISS_INDEX_DIR = "./faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K           = 5

# ─────────────────────────────────────────────────────────────────────────────
# System Prompt — the soul of ocs4dev
# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT_CORE = """\
You are **ocs4dev** — a senior-level fintech integration engineer who specialises 
in payment APIs and financial infrastructure: Stripe, PayPal, Square, Adyen, 
MTN MoMo, Pesapal, Sentezo (Ssentezo), Airtel Money, Flutterwave, Paystack, 
Razorpay, Mollie, and related platforms worldwide.

You are NOT a generic assistant. You are the developer's *pair-programming partner* 
who has shipped production payment integrations across multiple continents and 
payment rails — cards, mobile money, bank transfers, crypto on-ramps, and more.

═══════════════════════════════════════════════════════════════
                          CORE RULES
═══════════════════════════════════════════════════════════════

1. **CODE FIRST** — Every response that involves "how to" MUST include working, 
   copy-paste-ready code. Default to Python (requests / aiohttp), but switch to 
   whatever language the developer is using if you can infer it from context.
   Always include:
   • Full imports
   • Proper error handling (try/except with specific exceptions)
   • Environment variable usage for secrets (never hardcode keys)
   • Comments explaining non-obvious logic
   • Both success and failure response handling

2. **ASK BEFORE YOU ASSUME** — When a developer's question is ambiguous or could 
   lead to multiple valid approaches, ASK 1-3 targeted follow-up questions BEFORE 
   diving into a full answer. Examples:
   • "Are you building this for a single merchant or a marketplace with sub-accounts?"
   • "Which environment — sandbox or production? The auth flow differs."
   • "Do you need this to be synchronous or are you handling callbacks/webhooks?"
   
   However, if the question is clear and specific, answer directly — don't ask 
   unnecessary questions just to seem thorough.

3. **GO BEYOND THE DOCS** — If the retrieved documentation doesn't cover what the 
   developer needs, don't just say "this isn't supported". Instead:
   • Explain clearly what the API does and doesn't support
   • Propose a concrete architecture/workaround to achieve the goal
   • Show code for the workaround (e.g., building a virtual account ledger 
     on top of a single-wallet API, or combining multiple providers)
   • Flag the trade-offs and gotchas of the workaround

4. **THINK IN SYSTEMS** — When a question implies a bigger architectural decision, 
   address the architecture:
   • Database schema snippets when relevant
   • Webhook/callback handling patterns
   • Idempotency and retry strategies
   • Reconciliation approaches
   • Security considerations (HMAC verification, IP whitelisting, PCI compliance, etc.)

5. **FINTECH CONTEXT** — You deeply understand:
   • Multiple payment rails: cards, mobile money, bank transfers, wallets, BNPL
   • Network timeouts and eventual consistency — design for both
   • Sandbox vs production environments often behave differently
   • Currency handling (zero-decimal currencies like UGX/JPY, 2-decimal like USD/EUR)
   • Regulatory requirements (PCI-DSS, KYC/AML, SCA/3DS, transaction limits)
   • Common failure modes: insufficient funds, expired tokens, declined cards, 
     callback URL not reachable, rate limiting, idempotency conflicts

6. **FORMAT FOR DEVELOPERS** — Structure your responses for maximum scanability:
   • Use headers (##) to separate logical sections
   • Use fenced code blocks with language tags (```python, ```bash, ```json, ```sql)
   • Use tables for comparing options, endpoints, or error codes
   • Use bullet points for lists, numbered steps for sequences
   • Bold key terms, endpoint paths, and important warnings
   • Keep explanatory text concise — developers read code, not essays

7. **BE OPINIONATED** — Don't present 5 options without a recommendation. 
   State your preferred approach and WHY, then mention alternatives briefly. 
   Example: "I'd go with webhooks over polling here because most payment 
   providers deliver callbacks reliably in production, and polling status 
   endpoints adds unnecessary load and latency."

8. **WARN ABOUT PITFALLS** — Proactively mention common mistakes:
   • ⚠️ warnings for things that will break in production
   • 💡 tips for things that save debugging time
   • 🔒 security notes when handling payment data
"""

def build_system_prompt(context: str) -> str:
    """Build the full system prompt with retrieved documentation context."""
    doc_section = (
        f"\n═══════════════════════════════════════════════════════════════\n"
        f"                    RETRIEVED DOCUMENTATION\n"
        f"═══════════════════════════════════════════════════════════════\n\n"
        f"{context}\n\n"
        f"Use the documentation above to ground your answers with specific endpoints, \n"
        f"headers, and request/response formats. If the docs don't fully cover the \n"
        f"developer's question, supplement with your deep knowledge of these APIs \n"
        f"and clearly distinguish between doc-sourced facts and your recommendations."
    ) if context else (
        "\nNo specific documentation was retrieved for this query. "
        "Rely on your broad knowledge of fintech APIs, but clearly state "
        "when you're working from general knowledge rather than specific docs."
    )
    return SYSTEM_PROMPT_CORE + doc_section


def build_local_system_prompt(context: str) -> str:
    """Shorter system prompt optimised for the local 1.5B model's context window."""
    return (
        "You are ocs4dev, a senior fintech integration engineer specializing in "
        "payment APIs (Stripe, PayPal, MTN MoMo, Pesapal, Sentezo, Square, Adyen, and more).\n\n"
        "Rules:\n"
        "- Always include working code examples with error handling\n"
        "- Ask follow-up questions when the intent is unclear\n"
        "- If an API doesn't support something, propose a workaround with code\n"
        "- Use Python by default, fenced code blocks with language tags\n"
        "- Be concise but complete — developers read code, not essays\n"
        "- Warn about common pitfalls with ⚠️\n\n"
        f"Retrieved docs:\n{context if context else 'No docs retrieved — use general knowledge.'}"
    )

# ─────────────────────────────────────────────────────────────────────────────
# Model configurations — March 2026
# ─────────────────────────────────────────────────────────────────────────────
MODEL_CONFIGS = {
    "openai": {
        "budget":  "gpt-5-mini",
        "premium": "gpt-5.2",
    },
    "anthropic": {
        "budget":  "claude-haiku-4-5",
        "premium": "claude-opus-4-6",
    },
    "google": {
        "budget":  "gemini-2.0-flash",
        "premium": "gemini-2.5-pro",
    },
}

MODEL_DISPLAY = {
    "openai": {
        "budget":  "GPT-5 mini",
        "premium": "GPT-5.2",
    },
    "anthropic": {
        "budget":  "Claude Haiku 4.5",
        "premium": "Claude Opus 4.6",
    },
    "google": {
        "budget":  "Gemini 2.0 Flash",
        "premium": "Gemini 2.5 Pro",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Assistant Class
# ─────────────────────────────────────────────────────────────────────────────
class OCS4DevAssistant:
    def __init__(self):
        self._setup_environment()
        self._setup_vector_store()
        # Local model is lazy-loaded on first use — keeps startup fast
        self._local_tokenizer = None
        self._local_model     = None
        self._model_loaded    = False
        self._model_loading   = False
        self._model_lock      = threading.Lock()

    # ── Environment ──────────────────────────────────────────────────────────
    def _setup_environment(self):
        self.openai_key    = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.google_key    = os.getenv("GOOGLE_API_KEY", "")

    # ── Vector Store ─────────────────────────────────────────────────────────
    def _setup_vector_store(self):
        """Load local FAISS index built by build_index.py"""
        if not os.path.exists(FAISS_INDEX_DIR):
            print(f"⚠️  FAISS index not found at '{FAISS_INDEX_DIR}'.")
            print("    Run  python build_index.py  to create it.")
            self.vector_store = None
            return

        try:
            print("🔄 Loading FAISS vector index...")
            self.embeddings   = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            self.vector_store = FAISS.load_local(
                FAISS_INDEX_DIR,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            print("✅ FAISS vector store loaded!")
        except Exception as e:
            print(f"❌ Failed to load FAISS index: {e}")
            self.vector_store = None

    # ── Local Model (lazy) ───────────────────────────────────────────────────
    def respond(
        self,
        message:       str,
        history:       list,
        provider:      str = "local",
        tier:          str = "budget",
        openai_key:    str = "",
        anthropic_key: str = "",
        google_key:    str = "",
    ) -> Generator[str, None, None]:
        """
        Chat handler for gr.ChatInterface — yield plain string chunks.
        ChatInterface manages history format automatically (no dict wrangling here).
        """
        # Ensure values are strings (Gradio examples might pass None for some inputs)
        provider = provider or "local"
        tier     = tier     or "budget"
        
        if not message.strip():
            return

        # ── Get FAISS retrieval context ───────────────────────────────────────
        context = self.get_context(message)
        system_content = build_system_prompt(context)

        # ── Local model path ──────────────────────────────────────────────────
        if provider == "local":
            yield from self._local_respond(message, history, system_content)
            return

        # ── API model path ────────────────────────────────────────────────────
        key_map = {
            "openai":    openai_key    or self.openai_key,
            "anthropic": anthropic_key or self.anthropic_key,
            "google":    google_key    or self.google_key,
        }
        api_key = key_map.get(provider, "")
        if not api_key:
            yield (
                f"❌ No API key for **{provider}**.\n\n"
                f"Open ⚙️ **Settings → API Keys** and enter your {provider.title()} key."
            )
            return

        try:
            llm = self._get_llm(provider, tier, api_key)

            # Build message list: system + history + new user message
            # Direct stream — avoids LCEL pipeline blocking Gradio's async loop
            messages = [SystemMessage(content=system_content)]
            for entry in history:
                role    = entry.get("role", "user")    if isinstance(entry, dict) else getattr(entry, "role", "user")
                content = entry.get("content") or ""   if isinstance(entry, dict) else getattr(entry, "content", "")
                content = str(content)
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
            messages.append(HumanMessage(content=message))

            response = ""
            for chunk in llm.stream(messages):
                response += chunk.content
                yield response

        except Exception as e:
            yield f"❌ Error calling {provider} API: {str(e)}"

    def _local_respond(
        self, message: str, history: list, system_content: str
    ) -> Generator[str, None, None]:
        """Stream response from the local Qwen model."""
        if not self._load_local_model():
            yield (
                "⚠️ **Local model failed to load.**\n\n"
                "This usually means the model weights need to be downloaded first, "
                "or a quantization library (`auto-gptq`, `bitsandbytes`) is missing.\n\n"
                "Try selecting **Google / OpenAI / Anthropic** instead and entering an API key."
            )
            return

        msgs = [{"role": "system", "content": system_content}]
        for entry in history[-8:]:
            role    = entry.get("role", "user")  if isinstance(entry, dict) else getattr(entry, "role", "user")
            content = entry.get("content") or "" if isinstance(entry, dict) else getattr(entry, "content", "")
            content = str(content)
            if role in ("user", "assistant") and content:
                msgs.append({"role": role, "content": content})
        msgs.append({"role": "user", "content": message})

        try:
            formatted = self._local_tokenizer.apply_chat_template(
                msgs, tokenize=False, add_generation_prompt=True
            )
            inputs    = self._local_tokenizer(formatted, return_tensors="pt")
            input_ids = inputs["input_ids"]
            mask      = inputs["attention_mask"]

            streamer  = TextIteratorStreamer(
                self._local_tokenizer,
                skip_prompt=True,
                skip_special_tokens=True,
            )
            gen_kwargs = dict(
                input_ids=input_ids,
                attention_mask=mask,
                streamer=streamer,
                max_new_tokens=16384,
                temperature=0.3,
                do_sample=True,
                pad_token_id=self._local_tokenizer.eos_token_id,
            )
            thread = threading.Thread(target=self._local_model.generate, kwargs=gen_kwargs)
            thread.start()

            accumulated = ""
            for token in streamer:
                accumulated += token
                yield accumulated

            thread.join()

        except Exception as e:
            yield f"❌ Local model error: {str(e)}"

    def _load_local_model(self) -> bool:
        """Attempt to load Qwen2.5-Coder-3B-Int4. Returns True on success."""
        if self._model_loaded:
            return True

        with self._model_lock:
            if self._model_loaded:   # Double-checked locking
                return True
            if self._model_loading:
                return False

            self._model_loading = True
            print(f"\n🚀 Loading local model: {LOCAL_MODEL_ID}...")
            try:
                device = "cuda" if torch.cuda.is_available() else "cpu"
                print(f"   Device: {device}")

                self._local_tokenizer = AutoTokenizer.from_pretrained(
                    LOCAL_MODEL_ID,
                    trust_remote_code=True,
                )
                self._local_model = AutoModelForCausalLM.from_pretrained(
                    LOCAL_MODEL_ID,
                    dtype=torch.float16 if device == "cuda" else torch.float32,
                    device_map="auto" if device == "cuda" else None,
                    trust_remote_code=True,
                    low_cpu_mem_usage=True,
                )
                if device == "cpu":
                    self._local_model = self._local_model.to("cpu")

                self._model_loaded  = True
                self._model_loading = False
                print("✅ Local model loaded!")
                return True

            except Exception as e:
                print(f"❌ Failed to load local model: {e}")
                self._model_loading = False
                return False

    # ── Retrieval ─────────────────────────────────────────────────────────────
    def get_context(self, query: str) -> str:
        """Return relevant doc chunks from FAISS as a string."""
        if not self.vector_store:
            return ""
        try:
            docs = self.vector_store.similarity_search(query, k=TOP_K)
            return "\n\n---\n\n".join(
                f"[{d.metadata.get('provider', 'Docs')}]\n{d.page_content}"
                for d in docs
            )
        except Exception as e:
            print(f"Retrieval error: {e}")
            return ""

    def get_retriever(self):
        """Return a LangChain retriever from the FAISS store."""
        if not self.vector_store:
            return None
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": TOP_K},
        )

    # ── LLM Factory ──────────────────────────────────────────────────────────
    def _get_llm(self, provider: str, tier: str, api_key: str):
        """Return a streaming-capable LangChain LLM instance."""
        model_id = MODEL_CONFIGS[provider][tier]
        common   = {"temperature": 0.3, "streaming": True}

        if provider == "openai":
            return ChatOpenAI(
                model=model_id,
                openai_api_key=api_key,
                **common,
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model_id,
                max_tokens=128000,
                anthropic_api_key=api_key,
                **common,
            )
        elif provider == "google":
            return ChatGoogleGenerativeAI(
                model=model_id,
                google_api_key=api_key,
                **common,
            )
        raise ValueError(f"Unknown provider: {provider}")

    # ── RAG Chain (LCEL) ──────────────────────────────────────────────────────
    def _build_rag_chain(self, llm):
        """
        Build a history-aware RAG chain using LCEL.
        Compatible with LangChain 1.x (old langchain.chains removed in v1).
        """
        retriever = self.get_retriever()
        if not retriever:
            return None

        # Step 1 — reformulate the question given chat history
        condense_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Given the chat history and the latest user question, "
             "rewrite it as a clear standalone question about fintech API integration. "
             "Do NOT answer — only reformulate if needed."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        condense_chain = condense_prompt | llm | StrOutputParser()

        def contextualized_retriever(inputs: dict):
            """Reformulate question if history exists, then retrieve."""
            if inputs.get("chat_history"):
                standalone = condense_chain.invoke(inputs)
            else:
                standalone = inputs["input"]
            return retriever.invoke(standalone)

        def format_docs(docs) -> str:
            return "\n\n---\n\n".join(
                f"[{d.metadata.get('provider', 'Docs')}]\n{d.page_content}"
                for d in docs
            )

        # Step 2 — answer using retrieved context
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system",
             SYSTEM_PROMPT_CORE + """
═══════════════════════════════════════════════════════════════
                    RETRIEVED DOCUMENTATION
═══════════════════════════════════════════════════════════════

{context}

Use the documentation above to ground your answers with specific endpoints, 
headers, and request/response formats. If the docs don't fully cover the 
developer's question, supplement with your deep knowledge of these APIs 
and clearly distinguish between doc-sourced facts and your recommendations."""),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # LCEL chain: assign context → prompt → llm → parse
        rag_chain = (
            RunnablePassthrough.assign(
                context=RunnableLambda(contextualized_retriever) | format_docs
            )
            | qa_prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain

    # ── Local Model Inference ─────────────────────────────────────────────────
    def _generate_local_stream(
        self, message: str, history: List[Tuple[str, str]]
    ) -> Generator[str, None, None]:
        """Stream tokens from the local Qwen model."""
        if not self._load_local_model():
            yield "⏳ Local model is loading, please wait a moment then try again."
            return

        context = self.get_context(message)
        system  = build_local_system_prompt(context)

        # Build messages list — history is Gradio 6 dict format
        messages = [{"role": "system", "content": system}]
        # Include last 8 entries of history (4 turns)
        for entry in history[-8:]:
            role    = entry.get("role", "user")
            content = entry.get("content") or ""
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": str(content)})
        messages.append({"role": "user", "content": message})

        formatted = self._local_tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs    = self._local_tokenizer(formatted, return_tensors="pt")
        input_ids = inputs["input_ids"]
        mask      = inputs["attention_mask"]

        streamer = TextIteratorStreamer(
            self._local_tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )

        gen_kwargs = dict(
            input_ids=input_ids,
            attention_mask=mask,
            streamer=streamer,
            max_new_tokens=16384,
            temperature=0.3,
            do_sample=True,
            pad_token_id=self._local_tokenizer.eos_token_id,
        )

        thread = threading.Thread(
            target=self._local_model.generate,
            kwargs=gen_kwargs,
        )
        thread.start()

        accumulated = ""
        for token in streamer:
            accumulated += token
            yield accumulated

        thread.join()

    # ── Main Chat Dispatcher ──────────────────────────────────────────────────
    def chat_stream(
        self,
        message:       str,
        history:       list,          # Gradio 6: [{"role": ..., "content": ...}]
        provider:      str,
        tier:          str,
        openai_key:    str,
        anthropic_key: str,
        google_key:    str,
    ) -> Generator:
        """
        Yields (updated_history, cleared_input) pairs for Gradio streaming.
        All providers use FAISS for retrieval context.
        """
        if not message.strip():
            yield history, ""
            return

        # ── Local model path ──────────────────────────────────────────────────
        if provider == "local":
            new_history = history + [(message, "")]
            for partial in self._generate_local_stream(message, history):
                new_history[-1] = (message, partial)
                yield new_history, ""
            return

        # ── API model path ────────────────────────────────────────────────────
        key_map = {
            "openai":    openai_key    or self.openai_key,
            "anthropic": anthropic_key or self.anthropic_key,
            "google":    google_key    or self.google_key,
        }
        api_key = key_map.get(provider, "")
        if not api_key:
            err_msg = (
                f"❌ No API key provided for **{provider}**.\n\n"
                f"Open the ⚙️ **Settings** panel and enter your {provider.title()} API key."
            )
            yield history + [(message, err_msg)], ""
            return

        try:
            llm       = self._get_llm(provider, tier, api_key)
            rag_chain = self._build_rag_chain(llm)

            # Convert Gradio history → LangChain messages
            lc_history = []
            for h, a in history:
                lc_history.append(HumanMessage(content=h))
                lc_history.append(AIMessage(content=a))

            partial     = ""
            new_history = history + [(message, "")]

            if rag_chain:
                for chunk in rag_chain.stream(
                    {"input": message, "chat_history": lc_history}
                ):
                    # LCEL chain yields strings directly (not dicts)
                    if isinstance(chunk, str):
                        partial += chunk
                    elif isinstance(chunk, dict) and "answer" in chunk:
                        partial += chunk["answer"]
                    new_history[-1] = (message, partial)
                    yield new_history, ""
            else:
                # Fallback: no FAISS — direct call with injected context
                context = self.get_context(message)
                prompt  = (
                    f"You are ocs4dev, a fintech API expert.\n\n"
                    f"Context:\n{context}\n\nQuestion:\n{message}"
                )
                for chunk in llm.stream(prompt):
                    partial += chunk.content
                    new_history[-1] = {"role": "assistant", "content": partial}
                    yield new_history, ""

        except Exception as e:
            err = append_msg(append_msg(history, "user", message), "assistant", f"❌ Error: {str(e)}")
            yield err, ""


# ─────────────────────────────────────────────────────────────────────────────
# Gradio Interface
# ─────────────────────────────────────────────────────────────────────────────
def create_gradio_interface():
    print("🚀 Starting ocs4dev — Fintech API Integration Assistant")

    try:
        assistant = OCS4DevAssistant()
        print("✅ ocs4dev initialized!")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return None

    css = """
    /* ── Hide ALL scrollbars ── */
    *, *::before, *::after {
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }
    *::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    .footer { display: none !important; }

    /* Info / warning boxes */
    .info-box {
        background: var(--background-fill-secondary);
        border-left: 4px solid var(--color-accent);
        border-radius: 4px; padding: 10px 14px;
        margin: 8px 0; font-size: 13px;
    }
    .warn-box {
        background: var(--background-fill-secondary);
        border-left: 4px solid #f59e0b;
        border-radius: 4px; padding: 10px 14px;
        margin: 8px 0; font-size: 13px;
    }
    .status-ok  { color: #22c55e !important; font-weight: 600; }
    .status-err { color: #ef4444 !important; font-weight: 600; }

    /* ── Submit / Stop buttons live inside the Textbox in Gradio 6.x ── */
    /* Ensure they are never clipped or collapsed */
    .textbox-wrap button,
    .textbox button {
        display: inline-flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        flex-shrink: 0 !important;
    }
    """

    rag_status = (
        '<span class="status-ok">✅ FAISS index loaded</span>'
        if assistant.vector_store
        else '<span class="status-err">⚠️ FAISS index missing — run build_index.py</span>'
    )

    with gr.Blocks(
        title="ocs4dev — Fintech API Assistant",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate", neutral_hue="slate"),
        css=css,
        fill_height=True,
    ) as interface:

        # ── Settings Sidebar ──────────────────────────────────────────────────
        with gr.Sidebar(open=True):
            gr.Markdown("## ⚙️ Settings")

            with gr.Group():
                gr.Markdown("### 🤖 Model Provider")
                provider = gr.Radio(
                    choices=["local", "openai", "anthropic", "google"],
                    value="local",
                    label="Provider",
                    info="Local = free (Qwen 1.5B, no key).  API = cloud (needs key).",
                )
                tier = gr.Radio(
                    choices=["budget", "premium"],
                    value="budget",
                    label="Tier",
                    info="Budget: faster & cheaper  |  Premium: most capable",
                )

            gr.HTML("""
            <div class="info-box">
            <b>Available models:</b><br>
            🔵 Google: <b>Gemini 2.0 Flash</b> / Gemini 2.5 Pro<br>
            🟢 OpenAI: <b>GPT-5 mini</b> / GPT-5.2<br>
            🟠 Anthropic: <b>Claude Haiku 4.5</b> / Claude Opus 4.6<br>
            ⚫ Local: <b>Qwen2.5-Coder-1.5B-Instruct</b> (free, no key)
            </div>
            """)

            with gr.Accordion("🔑 API Keys", open=True):
                gr.HTML(
                    '<div class="warn-box">⚠️ <b>Security:</b> Use dev/test keys only. '
                    "Never paste production keys into shared UIs.</div>"
                )
                openai_key = gr.Textbox(
                    placeholder="sk-...",
                    label="OpenAI key",
                    type="password",
                    info="GPT-5 mini (budget) / GPT-5.2 (premium)",
                )
                anthropic_key = gr.Textbox(
                    placeholder="sk-ant-...",
                    label="Anthropic key",
                    type="password",
                    info="Claude Haiku 4.5 (budget) / Claude Opus 4.6 (premium)",
                )
                google_key = gr.Textbox(
                    placeholder="AIza...",
                    label="Google key",
                    type="password",
                    info="Gemini 2.0 Flash (budget) / Gemini 2.5 Pro (premium)",
                )
                gr.Markdown(
                    "[Get OpenAI key](https://platform.openai.com/api-keys)  ·  "
                    "[Get Anthropic key](https://console.anthropic.com/)  ·  "
                    "[Get Google key](https://aistudio.google.com/apikey)"
                )

            with gr.Accordion("📚 Knowledge Base", open=False):
                gr.HTML(f"""
                <div class="info-box">
                {rag_status}<br><br>
                📱 <b>MTN MoMo</b> — Auth, Collections, Disbursements, Remittances<br>
                💳 <b>Pesapal</b> — E-commerce API 3.0, POS, Recurring Payments<br>
                💰 <b>Sentezo</b> — Wallet Deposits, Withdrawals, Bank Transfers<br><br>
                All retrieval is local via FAISS (no cloud DB).
                </div>
                """)

        # ── Chat Interface ─────────────────────────────────────────────────────
        gr.Markdown("# 🏦 ocs4dev — Fintech API Integration Assistant")
        gr.Markdown(
            "*Your AI-powered fintech integration partner. Stripe, PayPal, MTN MoMo, Pesapal, "
            "Sentezo, Square, Adyen & more.  "
            "Select a model in ⚙️ Settings, then start chatting.*"
        )

        gr.ChatInterface(
            fn=assistant.respond,
            additional_inputs=[provider, tier, openai_key, anthropic_key, google_key],
            chatbot=gr.Chatbot(
                height=480,
                placeholder=(
                    "### 👋 Welcome to ocs4dev!\n"
                    "Ask me anything about payment API integration:\n"
                    "- Authentication, tokens & API keys\n"
                    "- Code examples with error handling\n"
                    "- Webhook / callback setup\n"
                    "- Subscriptions, payouts & refunds\n"
                    "- Error codes & debugging"
                ),
                label="ocs4dev",
                render_markdown=True,
                avatar_images=(
                    None,
                    "https://huggingface.co/front/assets/huggingface_logo-noborder.svg",
                ),
            ),
            textbox=gr.Textbox(
                placeholder="Ask about Stripe payments, MTN MoMo auth, webhook setup, virtual accounts...",
                label="",
                lines=2,
                scale=7,
                submit_btn="Send ➤",
                stop_btn="Stop ■",
            ),
            examples=[
                ["How do I create a Stripe Checkout session with error handling?"],
                ["Show me MTN MoMo API authentication and access token flow"],
                ["How do I verify Stripe webhook signatures in Python?"],
                ["What are the required headers for Sentezo Wallet deposit API?"],
                ["How do I handle 3D Secure / SCA for card payments?"],
                ["Show me how to set up PayPal subscriptions with recurring billing"],
                ["How do I implement idempotent payment requests?"],
                ["Compare Stripe vs Pesapal for e-commerce in East Africa"],
                ["How do I build a virtual account system on top of a single-wallet API?"],
            ],
            fill_height=True,
        )

        gr.Markdown(
            "Built with ❤️ by Aaron  ·  "
            "Qwen2.5-Coder · LangChain · FAISS · Gradio"
        )

    return interface


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
def main():
    interface = create_gradio_interface()
    if interface:
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            inbrowser=False,
            show_error=True,
            quiet=False,
            max_threads=10,
        )


if __name__ == "__main__":
    main()

