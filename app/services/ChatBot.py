import requests
from app.config import Settings
from app.services.context_retriever import get_relevant_documents

def generate_response(question: str) -> str:
    #prompt = f"""Tu es un assistant virtuel pour les étudiants de L'Ecole Supérieure de Technologie de Salé situer au Maroc. Réponds de manière claire et professionnelle.
     # 1. Get relevant documents
    docs = get_relevant_documents(question)
    context_blocks = "\n\n".join(
        f"📄 Source: {url}\n{content[:1000]}..." for _, url, content in docs
    )

    #  Build the prompt
    prompt = f"""
Tu es un assistant ENT pour les étudiants de L'Ecole Supérieure de Technologie de Salé(ESTS). Utilise uniquement les informations suivantes pour répondre :

{context_blocks}

Étudiant: {question}
Assistant:"""

    response = requests.post(
        f"{Settings.OLLAMA_BASE_URL}/api/generate",
        json={
            "model": Settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise Exception("Erreur Ollama: " + response.text)

    return response.json()["response"]
