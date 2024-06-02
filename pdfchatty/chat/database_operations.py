from .utils import load_config
import sqlite3
import os

config = load_config()

def get_db_connection():
    db_path = config['chat_sessions_database_path']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure directory exists
    return sqlite3.connect(db_path, check_same_thread=False)
# Ensure the database table exists

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_history_id TEXT NOT NULL,
                        sender_type TEXT NOT NULL,
                        message_type TEXT NOT NULL,
                        text_content TEXT,
                        blob_content BLOB
                      )''')
    conn.commit()
    conn.close()

initialize_db()
def save_text_message(chat_history_id, sender_type, text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (chat_history_id, sender_type, message_type, text_content) VALUES (?, ?, ?, ?)',
                   (chat_history_id, sender_type, 'text', text))
    conn.commit()
    conn.close()

def load_messages(chat_history_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT message_id, sender_type, message_type, text_content, blob_content FROM messages WHERE chat_history_id = ?", (chat_history_id,))
    messages = cursor.fetchall()
    conn.close()
    chat_history = []
    for message in messages:
        message_id, sender_type, message_type, text_content, blob_content = message
        if message_type == 'text':
            chat_history.append({'message_id': message_id, 'sender_type': sender_type, 'message_type': message_type, 'content': text_content})
        else:
            chat_history.append({'message_id': message_id, 'sender_type': sender_type, 'message_type': message_type, 'content': blob_content})
    return chat_history

def load_last_k_text_messages(chat_history_id, k):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT message_id, sender_type, message_type, text_content
    FROM messages
    WHERE chat_history_id = ? AND message_type = 'text'
    ORDER BY message_id DESC
    LIMIT ?
    """, (chat_history_id, k))
    messages = cursor.fetchall()
    conn.close()
    chat_history = []
    for message in reversed(messages):
        message_id, sender_type, message_type, text_content = message
        chat_history.append({'message_id': message_id, 'sender_type': sender_type, 'message_type': message_type, 'content': text_content})
    return chat_history

def get_all_chat_history_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT chat_history_id FROM messages ORDER BY chat_history_id ASC")
    chat_history_ids = cursor.fetchall()
    conn.close()
    return [item[0] for item in chat_history_ids]

def delete_chat_history(chat_history_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE chat_history_id = ?", (chat_history_id,))
    conn.commit()
    conn.close()
