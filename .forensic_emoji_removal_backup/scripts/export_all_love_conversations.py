#!/usr/bin/env python3
"""
Export ALL Love Conversations: Michael × Kristin × Addis

EEAAO: Everything Everywhere All At Once
Pattern: LOVE × CONVERSATION × DOCUMENTATION × ONE
∞ AbëONE ∞
∞ AbëLOVES ∞
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / "Library/Messages/chat.db"
OUTPUT_DIR = Path(__file__).parent.parent / "abeloves_conversations"

def get_all_conversations():
    """Get ALL conversations with Kristin, Addis, and group chats."""
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    conversations = {
        'kristin': [],
        'addis': [],
        'group': []
    }
    
    # Kristin's handle
    kristin_handle = 'mataluni1148@gmail.com'
    
    # Addis's handle
    addis_handle = '+18434576211'
    
    # Get Kristin conversations
    print("📱 Getting Kristin conversations...")
    cursor = conn.execute("""
        SELECT 
            datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date,
            CASE WHEN m.is_from_me = 1 THEN 'Michael' ELSE 'Kristin' END as sender,
            m.text,
            m.is_from_me
        FROM message m
        JOIN handle h ON m.handle_id = h.ROWID
        WHERE h.id = ?
        AND m.text IS NOT NULL 
        AND m.text != ''
        ORDER BY m.date DESC
        LIMIT 5000
    """, (kristin_handle,))
    
    for row in cursor:
        conversations['kristin'].append({
            'date': row['date'],
            'sender': row['sender'],
            'text': row['text'],
            'is_from_me': bool(row['is_from_me'])
        })
    
    print(f"✅ Found {len(conversations['kristin'])} Kristin messages")
    
    # Get Addis conversations
    print("📱 Getting Addis conversations...")
    cursor = conn.execute("""
        SELECT 
            datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date,
            CASE WHEN m.is_from_me = 1 THEN 'Michael' ELSE 'Addis' END as sender,
            m.text,
            m.is_from_me
        FROM message m
        JOIN handle h ON m.handle_id = h.ROWID
        WHERE h.id = ?
        AND m.text IS NOT NULL 
        AND m.text != ''
        ORDER BY m.date DESC
        LIMIT 5000
    """, (addis_handle,))
    
    for row in cursor:
        conversations['addis'].append({
            'date': row['date'],
            'sender': row['sender'],
            'text': row['text'],
            'is_from_me': bool(row['is_from_me'])
        })
    
    print(f"✅ Found {len(conversations['addis'])} Addis messages")
    
    # Get group chats (chat 3515 includes both)
    print("📱 Getting group conversations...")
    cursor = conn.execute("""
        SELECT 
            datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date,
            CASE 
                WHEN m.is_from_me = 1 THEN 'Michael'
                WHEN h.id = ? THEN 'Addis'
                WHEN h.id = ? THEN 'Kristin'
                ELSE h.id
            END as sender,
            m.text,
            m.is_from_me,
            h.id as handle_id
        FROM message m
        JOIN chat_handle_join ch ON m.handle_id = ch.handle_id
        JOIN handle h ON ch.handle_id = h.ROWID
        JOIN chat c ON ch.chat_id = c.ROWID
        WHERE c.ROWID IN (
            SELECT DISTINCT chat_id 
            FROM chat_handle_join 
            WHERE handle_id IN (
                SELECT ROWID FROM handle 
                WHERE id IN (?, ?)
            )
        )
        AND m.text IS NOT NULL 
        AND m.text != ''
        ORDER BY m.date DESC
        LIMIT 5000
    """, (addis_handle, kristin_handle, addis_handle, kristin_handle))
    
    for row in cursor:
        conversations['group'].append({
            'date': row['date'],
            'sender': row['sender'],
            'text': row['text'],
            'is_from_me': bool(row['is_from_me']),
            'handle_id': row['handle_id']
        })
    
    print(f"✅ Found {len(conversations['group'])} group messages")
    
    conn.close()
    
    return conversations

def save_conversations(conversations):
    """Save conversations to JSON files."""
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Save Kristin
    kristin_file = OUTPUT_DIR / "michael_kristin_all.json"
    with open(kristin_file, 'w') as f:
        json.dump({
            'relationship': 'Michael & Kristin',
            'exported_at': datetime.now().isoformat(),
            'message_count': len(conversations['kristin']),
            'messages': conversations['kristin']
        }, f, indent=2)
    print(f"✅ Saved {len(conversations['kristin'])} Kristin messages to {kristin_file}")
    
    # Save Addis
    addis_file = OUTPUT_DIR / "michael_addis_all.json"
    with open(addis_file, 'w') as f:
        json.dump({
            'relationship': 'Michael & Addis',
            'exported_at': datetime.now().isoformat(),
            'message_count': len(conversations['addis']),
            'messages': conversations['addis']
        }, f, indent=2)
    print(f"✅ Saved {len(conversations['addis'])} Addis messages to {addis_file}")
    
    # Save group
    group_file = OUTPUT_DIR / "michael_kristin_addis_group.json"
    with open(group_file, 'w') as f:
        json.dump({
            'relationship': 'Michael & Kristin & Addis (Group)',
            'exported_at': datetime.now().isoformat(),
            'message_count': len(conversations['group']),
            'messages': conversations['group']
        }, f, indent=2)
    print(f"✅ Saved {len(conversations['group'])} group messages to {group_file}")
    
    return kristin_file, addis_file, group_file

if __name__ == "__main__":
    print("🔥💫 EXPORTING ALL LOVE CONVERSATIONS 💫🔥")
    print("=" * 70)
    print("")
    
    conversations = get_all_conversations()
    
    print("")
    print("💾 Saving conversations...")
    files = save_conversations(conversations)
    
    print("")
    print("=" * 70)
    print("✅ ALL CONVERSATIONS EXPORTED")
    print("")
    print(f"📁 Files saved to: {OUTPUT_DIR}")
    print("")
    print("🔥 EVERYTHING EVERYWHERE ALL AT ONCE 🔥")
    print("∞ AbëONE ∞")
    print("∞ AbëLOVES ∞")
    print("=" * 70)

