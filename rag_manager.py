import os
import uuid
import json
from typing import List, Dict

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


# Initialize Gemini embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


class RAGManager:
    """Corrective RAG with Gemini Embeddings + FAISS"""

    def __init__(self, persist_dir: str = "./rag_memory"):
        self.persist_dir = persist_dir
        self.embeddings = embedding_model
        self.db = None  # FAISS starts empty

    def _ensure_index(self):
        """Ensure FAISS index exists."""
        if self.db is None:
            self.db = FAISS.from_texts(
                texts=[],
                embedding=self.embeddings,
                metadatas=[]
            )

    def add_corrective_insight(self, insight_package: Dict):
        try:
            self._ensure_index()

            paragraph = json.dumps(insight_package, indent=2)

            self.db.add_texts(
                texts=[paragraph],
                metadatas=[{"session_id": insight_package.get("session_id")}],
                ids=[str(uuid.uuid4())]
            )

            print(f"Insight stored for session: {insight_package.get('session_id')}")
            return {"status": "stored", "session_id": insight_package.get("session_id")}
        except Exception as e:
            print(f"Error storing insight: {e}")
            return {"status": "failed", "error": str(e)}

    def fetch_context(self, query: str, k: int = 3) -> List[Dict]:
        try:
            self._ensure_index()
            results = self.db.similarity_search_with_score(query, k=k)

            return [
                {"text": doc.page_content, "similarity": score}
                for doc, score in results
            ]
        except Exception as e:
            print(f"Error fetching context: {e}")
            return []

    def clear_memory(self, confirm=False):
        if confirm:
            self.db = None
            print("Memory cleared.")
        else:
            print("Pass confirm=True to clear memory.")
