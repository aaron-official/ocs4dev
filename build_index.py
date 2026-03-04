"""
build_index.py — One-time FAISS index builder for ocs4dev
==========================================================
Run this script ONCE locally before deploying to HuggingFace Spaces.
It reads all markdown files from knowledge_base/ and builds a FAISS
vector index that the main app uses for retrieval.

After running, commit the generated faiss_index/ folder to your repo:
    git add faiss_index/
    git commit -m "Add FAISS vector index"
    git push

Usage:
    python build_index.py
    python build_index.py --kb ./knowledge_base --out ./faiss_index
"""

import os
import argparse
from pathlib import Path

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Defaults ---
DEFAULT_KB_DIR   = "./knowledge_base"
DEFAULT_OUT_DIR  = "./faiss_index"
EMBEDDING_MODEL  = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE       = 1000
CHUNK_OVERLAP    = 200


def load_documents(kb_dir: str):
    """Recursively load all .md files from the knowledge base directory."""
    print(f"\n📂 Loading documents from: {kb_dir}")
    loader = DirectoryLoader(
        kb_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
        use_multithreading=True,
    )
    docs = loader.load()

    # Enrich metadata with API provider based on folder name
    for doc in docs:
        source = doc.metadata.get("source", "")
        path_parts = Path(source).parts
        # Detect provider from folder structure
        for part in path_parts:
            if "mtn" in part.lower():
                doc.metadata["provider"] = "MTN MoMo"
                break
            elif "pesapal" in part.lower():
                doc.metadata["provider"] = "Pesapal"
                break
            elif "sentezo" in part.lower() or "ssentezo" in part.lower():
                doc.metadata["provider"] = "Sentezo"
                break
        else:
            doc.metadata["provider"] = "General"

    print(f"✅ Loaded {len(docs)} documents")
    return docs


def split_documents(docs):
    """Split documents into overlapping chunks for better retrieval."""
    print(f"\n✂️  Splitting into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks from {len(docs)} documents")
    return chunks


def build_faiss_index(chunks, out_dir: str):
    """Generate embeddings and save FAISS index to disk."""
    print(f"\n🔢 Loading embedding model: {EMBEDDING_MODEL}")
    print("   (This may take a minute on first run — model will be cached)")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print(f"\n🔄 Building FAISS index from {len(chunks)} chunks...")
    vector_store = FAISS.from_documents(chunks, embeddings)

    os.makedirs(out_dir, exist_ok=True)
    vector_store.save_local(out_dir)
    print(f"✅ FAISS index saved to: {out_dir}/")
    return vector_store


def run_verification(vector_store):
    """Run a quick search test to confirm the index works."""
    print("\n🧪 Running verification queries...")
    test_queries = [
        ("MTN MoMo authentication", "MTN MoMo"),
        ("Pesapal payment integration", "Pesapal"),
        ("Sentezo wallet deposit", "Sentezo"),
    ]

    all_passed = True
    for query, expected_provider in test_queries:
        try:
            results = vector_store.similarity_search(query, k=3)
            providers = [r.metadata.get("provider", "?") for r in results]
            hit = any(expected_provider in p for p in providers)
            status = "✅" if hit else "⚠️ "
            if not hit:
                all_passed = False
            print(f"   {status} '{query}'")
            print(f"      Top result: {Path(results[0].metadata.get('source', '?')).name}")
            print(f"      Preview: {results[0].page_content[:80].strip()}...")
        except Exception as e:
            print(f"   ❌ '{query}' — Error: {e}")
            all_passed = False

    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="Build FAISS vector index for ocs4dev"
    )
    parser.add_argument(
        "--kb", default=DEFAULT_KB_DIR,
        help=f"Path to knowledge base directory (default: {DEFAULT_KB_DIR})"
    )
    parser.add_argument(
        "--out", default=DEFAULT_OUT_DIR,
        help=f"Output directory for FAISS index (default: {DEFAULT_OUT_DIR})"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  ocs4dev — FAISS Vector Index Builder")
    print("=" * 60)

    # Validate knowledge base dir
    if not os.path.exists(args.kb):
        print(f"\n❌ Knowledge base directory not found: {args.kb}")
        print("   Make sure your knowledge_base/ folder exists with .md files.")
        return

    # Load → split → index
    docs = load_documents(args.kb)
    if not docs:
        print("❌ No .md files found in the knowledge base!")
        return

    chunks = split_documents(docs)
    vector_store = build_faiss_index(chunks, args.out)

    # Verify
    passed = run_verification(vector_store)

    print("\n" + "=" * 60)
    if passed:
        print("🎉 Index built and verified successfully!")
    else:
        print("⚠️  Index built, but some queries returned unexpected results.")
        print("   Consider checking your knowledge base content.")
    print()
    print("📋 Next steps:")
    print(f"   1. git add {args.out}/")
    print(f"   2. git commit -m 'Add FAISS vector index'")
    print(f"   3. git push (to deploy to HuggingFace Spaces)")
    print("=" * 60)


if __name__ == "__main__":
    main()
