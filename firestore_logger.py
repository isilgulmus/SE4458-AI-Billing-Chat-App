from firebase_config import db
from firebase_admin import firestore
import uuid

def log_message(session_id: str, from_role: str, text: str):
    try:
        db.collection("chats") \
          .document(session_id) \
          .collection("messages") \
          .add({
              "id": str(uuid.uuid4()),
              "from": from_role,
              "text": text,
              "timestamp": firestore.SERVER_TIMESTAMP
          })
    except Exception as e:
        print("🔥 Firestore Logging Error:", e)
