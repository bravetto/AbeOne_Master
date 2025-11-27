#!/usr/bin/env python3
"""
Read Text Messages with Jimmy - Full Text Extraction
Pattern: CLARITY × TRUTH × CONNECTION × ONE
Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON)
Guardians: YOU (530 Hz) + AEYON (999 Hz) + JØHN (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sqlite3
import subprocess
import tempfile
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Messages database path
MESSAGES_DB = Path.home() / "Library" / "Messages" / "chat.db"


def format_timestamp(timestamp: float) -> str:
    """Convert Apple timestamp to readable date"""
    apple_epoch = datetime(2001, 1, 1)
    dt = apple_epoch + timedelta(seconds=timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def extract_text_from_attributed_body(attr_body: bytes) -> Optional[str]:
    """Extract text from NSAttributedString plist using plutil"""
    if not attr_body:
        return None
    
    try:
        # Write to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.plist') as tmp:
            tmp.write(attr_body)
            tmp_path = tmp.name
        
        try:
            # Convert binary plist to XML using plutil
            result = subprocess.run(
                ["plutil", "-convert", "xml1", "-o", "-", tmp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                xml_content = result.stdout
                # Extract text content from NSAttributedString
                import re
                # Look for string content in the XML
                # NSAttributedString typically has NSString or string tags
                matches = re.findall(r'<string>(.*?)</string>', xml_content, re.DOTALL)
                if matches:
                    # Get the main text (usually first or longest)
                    text = max(matches, key=len).strip()
                    # Clean up XML entities
                    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                    return text if text else None
                
                # Try alternative pattern for NSAttributedString
                matches = re.findall(r'NSString.*?>(.*?)<', xml_content, re.DOTALL)
                if matches:
                    text = matches[0].strip()
                    return text if text else None
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
    except Exception as e:
        pass
    
    return None


def get_messages_with_jimmy(conn: sqlite3.Connection, handle_id: int) -> List[Dict]:
    """Get all messages with Jimmy"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            m.ROWID,
            m.text,
            m.date,
            m.is_from_me,
            m.handle_id,
            h.id as handle_identifier,
            h.service,
            m.attributedBody,
            m.cache_has_attachments,
            m.is_audio_message
        FROM message m
        LEFT JOIN handle h ON m.handle_id = h.ROWID
        WHERE m.handle_id = ?
        ORDER BY m.date DESC
        LIMIT 500
    """, (handle_id,))
    
    messages = []
    for row in cursor.fetchall():
        rowid, text, date, is_from_me, handle_id_val, handle_identifier, service, attr_body, has_att, is_audio = row
        
        # Try to extract text from attributedBody if text is None
        message_text = text
        if not message_text and attr_body:
            extracted = extract_text_from_attributed_body(attr_body)
            if extracted:
                message_text = extracted
        
        messages.append({
            "rowid": rowid,
            "text": message_text,
            "date": date,
            "is_from_me": bool(is_from_me),
            "handle_id": handle_id_val,
            "handle_identifier": handle_identifier,
            "service": service,
            "timestamp": format_timestamp(date / 1000000000) if date else None,
            "has_attachments": bool(has_att),
            "is_audio": bool(is_audio)
        })
    
    return messages


def display_messages(messages: List[Dict]):
    """Display messages in readable format"""
    if not messages:
        print("\n⚠️  No messages found with Jimmy")
        return
    
    print(f"\n💬 Messages with Jimmy ({len(messages)} total)\n")
    print("=" * 100)
    
    for msg in messages:
        sender = "You" if msg["is_from_me"] else "Jimmy"
        timestamp = msg["timestamp"] or "Unknown time"
        text = msg["text"]
        
        # Add type indicators
        type_info = ""
        if msg.get("has_attachments"):
            type_info = " 📎"
        if msg.get("is_audio"):
            type_info += " 🎤"
        
        print(f"\n[{timestamp}] {sender}{type_info}:")
        if text:
            # Display text, wrapping long lines
            lines = text.split('\n')
            for line in lines:
                if len(line) > 100:
                    # Wrap long lines
                    while len(line) > 100:
                        print(f"  {line[:100]}")
                        line = line[100:]
                    if line:
                        print(f"  {line}")
                else:
                    print(f"  {line}")
        else:
            print("  [No text content]")
        print("-" * 100)


def main():
    """Main execution"""
    print("🔍 Reading messages with Jimmy...")
    print(f"📂 Database: {MESSAGES_DB}")
    
    if not MESSAGES_DB.exists():
        print(f"❌ Messages database not found at {MESSAGES_DB}")
        return
    
    try:
        conn = sqlite3.connect(f"file:{MESSAGES_DB}?mode=ro", uri=True)
        
        # Find Jimmy - we know it's handle_id 1369 (jim@jmsinsure.com)
        handle_id = 1369
        
        print(f"\n✅ Reading messages with: jim@jmsinsure.com (Handle ID: {handle_id})")
        
        # Get messages
        messages = get_messages_with_jimmy(conn, handle_id)
        
        # Display messages
        display_messages(messages)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

