import re
from app.services.context_loader import documents

def get_relevant_documents(question: str, max_docs=3):
    question_keywords = set(re.findall(r"\w+", question.lower()))

    ranked = []
    for url, content in documents:
        content_lower = content.lower()
        match_count = sum(1 for word in question_keywords if word in content_lower)
        if match_count > 0:
            ranked.append((match_count, url, content))

    ranked.sort(reverse=True)  # more matches = higher rank

    return ranked[:max_docs]
