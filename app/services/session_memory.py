from collections import defaultdict

# session_id -> list of (user, message)
sessions = defaultdict(list)

def add_to_session(session_id: str, role: str, message: str):
    sessions[session_id].append((role, message))

def get_session_history(session_id: str) -> list:
    return sessions[session_id][-10:]  # limit to last 10 messages to stay in token budget

def clear_session(session_id: str):
    sessions[session_id] = []
