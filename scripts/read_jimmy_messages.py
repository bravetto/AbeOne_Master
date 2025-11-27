#!/usr/bin/env python3
"""
Read Text Messages with Jimmy
Pattern: CLARITY × TRUTH × CONNECTION × ONE
Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON)
Guardians: YOU (530 Hz) + AEYON (999 Hz) + JØHN (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Messages database path
MESSAGES_DB = Path.home() / "Library" / "Messages" / "chat.db"


def format_timestamp(timestamp: float) -> str:
    """Convert Apple timestamp to readable date"""
    # Apple timestamp is seconds since 2001-01-01
    apple_epoch = datetime(2001, 1, 1)
    dt = apple_epoch + timedelta(seconds=timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def list_all_contacts(conn: sqlite3.Connection, limit: int = 50, search_term: str = None):
    """List all contacts to help identify Jimmy"""
    cursor = conn.cursor()
    
    if search_term:
        # Search for contacts matching search term
        cursor.execute("""
            SELECT DISTINCT
                h.ROWID,
                h.id,
                h.country,
                h.service,
                c.display_name,
                COUNT(m.ROWID) as message_count
            FROM handle h
            LEFT JOIN chat_handle_join chj ON h.ROWID = chj.handle_id
            LEFT JOIN chat c ON chj.chat_id = c.ROWID
            LEFT JOIN message m ON m.handle_id = h.ROWID
            WHERE LOWER(h.id) LIKE ? OR LOWER(COALESCE(c.display_name, '')) LIKE ?
            GROUP BY h.ROWID, h.id, h.country, h.service, c.display_name
            ORDER BY message_count DESC, h.id
            LIMIT ?
        """, (f"%{search_term}%", f"%{search_term}%", limit))
    else:
        cursor.execute("""
            SELECT DISTINCT
                h.ROWID,
                h.id,
                h.country,
                h.service,
                c.display_name,
                COUNT(m.ROWID) as message_count
            FROM handle h
            LEFT JOIN chat_handle_join chj ON h.ROWID = chj.handle_id
            LEFT JOIN chat c ON chj.chat_id = c.ROWID
            LEFT JOIN message m ON m.handle_id = h.ROWID
            GROUP BY h.ROWID, h.id, h.country, h.service, c.display_name
            ORDER BY message_count DESC, h.id
            LIMIT ?
        """, (limit,))
    
    results = cursor.fetchall()
    print(f"\n📱 Contacts (showing top {limit} by message count):")
    print("=" * 100)
    for i, (rowid, handle_id, country, service, display_name, msg_count) in enumerate(results, 1):
        name = display_name or handle_id
        print(f"  {i:2d}. {name:30s} | Handle: {str(handle_id):20s} | Messages: {msg_count:4d} | Service: {service or 'N/A'}")
    
    return results


def find_jimmy_contact(conn: sqlite3.Connection) -> Optional[Dict]:
    """Find Jimmy's contact in the database"""
    cursor = conn.cursor()
    
    # Search for contacts with "jimmy" in name (case insensitive)
    # Check both handle.id and chat.display_name
    cursor.execute("""
        SELECT DISTINCT
            h.ROWID, 
            h.id, 
            h.country, 
            h.service,
            c.display_name
        FROM handle h
        LEFT JOIN chat_handle_join chj ON h.ROWID = chj.handle_id
        LEFT JOIN chat c ON c.ROWID = chj.chat_id
        WHERE LOWER(h.id) LIKE '%jimmy%'
           OR LOWER(COALESCE(c.display_name, '')) LIKE '%jimmy%'
        LIMIT 10
    """)
    
    results = cursor.fetchall()
    
    # Also search chat display names directly
    cursor.execute("""
        SELECT DISTINCT
            h.ROWID,
            h.id,
            h.country,
            h.service,
            c.display_name
        FROM chat c
        JOIN chat_handle_join chj ON c.ROWID = chj.chat_id
        JOIN handle h ON chj.handle_id = h.ROWID
        WHERE LOWER(COALESCE(c.display_name, '')) LIKE '%jimmy%'
        LIMIT 10
    """)
    
    chat_results = cursor.fetchall()
    
    # Combine and deduplicate
    all_results = {}
    for row in results + chat_results:
        rowid = row[0]
        if rowid not in all_results:
            all_results[rowid] = row
    
    if all_results:
        print("\n📱 Found potential Jimmy contacts:")
        for i, (rowid, handle_id, country, service, display_name) in enumerate(all_results.values(), 1):
            name = display_name or handle_id
            print(f"  {i}. {name} | Handle ID: {handle_id} | Country: {country} | Service: {service}")
        
        # Return first match
        first_row = list(all_results.values())[0]
        return {
            "rowid": first_row[0],
            "id": first_row[1],
            "country": first_row[2],
            "service": first_row[3],
            "display_name": first_row[4]
        }
    
    return None


def get_messages_with_jimmy(conn: sqlite3.Connection, handle_id: Optional[int] = None) -> List[Dict]:
    """Get all messages with Jimmy"""
    cursor = conn.cursor()
    
    if handle_id:
        # Get messages for specific handle with more details
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
                m.is_audio_message,
                m.is_delayed,
                m.is_read,
                m.item_type
            FROM message m
            LEFT JOIN handle h ON m.handle_id = h.ROWID
            WHERE m.handle_id = ?
            ORDER BY m.date DESC
            LIMIT 500
        """, (handle_id,))
    else:
        # Get all messages, we'll filter by name
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
                m.is_audio_message,
                m.is_delayed,
                m.is_read,
                m.item_type
            FROM message m
            LEFT JOIN handle h ON m.handle_id = h.ROWID
            WHERE h.id LIKE '%jimmy%' OR h.id LIKE '%Jimmy%'
            ORDER BY m.date DESC
            LIMIT 500
        """)
    
    messages = []
    for row in cursor.fetchall():
        rowid = row[0]
        text = row[1]
        date = row[2]
        is_from_me = row[3]
        handle_id_val = row[4]
        handle_identifier = row[5]
        service = row[6]
        attributed_body = row[7]
        has_attachments = row[8]
        is_audio = row[9]
        is_delayed = row[10]
        is_read = row[11]
        item_type = row[12]
        
        # Try to extract text from attributedBody if text is None
        message_text = text
        if not message_text and attributed_body:
            try:
                # attributedBody is a binary plist, try to extract readable text
                import plistlib
                if isinstance(attributed_body, bytes):
                    # Try to decode plist
                    try:
                        plist_data = plistlib.loads(attributed_body)
                        if isinstance(plist_data, dict) and 'NSAttributedString' in str(plist_data):
                            # Extract string from attributed string
                            message_text = str(attributed_body)[:200]  # Fallback
                    except:
                        pass
            except:
                pass
        
        # Build message type description
        msg_type_parts = []
        if has_attachments:
            msg_type_parts.append("📎 Attachment")
        if is_audio:
            msg_type_parts.append("🎤 Audio")
        if item_type and item_type != 0:
            msg_type_parts.append(f"Type: {item_type}")
        
        messages.append({
            "rowid": rowid,
            "text": message_text,
            "date": date,
            "is_from_me": bool(is_from_me),
            "handle_id": handle_id_val,
            "handle_identifier": handle_identifier,
            "service": service,
            "timestamp": format_timestamp(date / 1000000000) if date else None,
            "has_attachments": bool(has_attachments),
            "is_audio": bool(is_audio),
            "item_type": item_type,
            "type_description": " | ".join(msg_type_parts) if msg_type_parts else None
        })
    
    return messages


def display_messages(messages: List[Dict]):
    """Display messages in readable format"""
    if not messages:
        print("\n⚠️  No messages found with Jimmy")
        return
    
    print(f"\n💬 Messages with Jimmy ({len(messages)} total)\n")
    print("=" * 80)
    
    for msg in messages:
        sender = "You" if msg["is_from_me"] else "Jimmy"
        timestamp = msg["timestamp"] or "Unknown time"
        text = msg["text"] or "[No text]"
        
        # Add type indicators
        type_info = ""
        if msg.get("has_attachments"):
            type_info = " 📎"
        if msg.get("is_audio"):
            type_info += " 🎤"
        if msg.get("type_description"):
            type_info += f" ({msg['type_description']})"
        
        print(f"\n[{timestamp}] {sender}{type_info}:")
        if text and text != "[No text]":
            # Truncate very long messages
            display_text = text if len(text) < 500 else text[:500] + "..."
            print(f"  {display_text}")
        else:
            print(f"  {text}")
        print("-" * 80)


def main():
    """Main execution"""
    import sys
    
    print("🔍 Reading messages with Jimmy...")
    print(f"📂 Database: {MESSAGES_DB}")
    
    if not MESSAGES_DB.exists():
        print(f"❌ Messages database not found at {MESSAGES_DB}")
        print("   Make sure Messages app has been used at least once.")
        return
    
    try:
        # Connect to database (read-only)
        conn = sqlite3.connect(f"file:{MESSAGES_DB}?mode=ro", uri=True)
        
        # Check if handle ID provided as argument
        handle_id = None
        if len(sys.argv) > 1:
            try:
                handle_id = int(sys.argv[1])
                print(f"\n📞 Using provided handle ID: {handle_id}")
            except ValueError:
                # Try searching by phone number
                phone_search = sys.argv[1]
                cursor = conn.cursor()
                cursor.execute("SELECT ROWID, id FROM handle WHERE id LIKE ?", (f"%{phone_search}%",))
                result = cursor.fetchone()
                if result:
                    handle_id = result[0]
                    print(f"\n📞 Found handle ID {handle_id} for: {result[1]}")
                else:
                    print(f"\n⚠️  Could not find contact matching: {phone_search}")
        
        # Find Jimmy's contact if not provided
        if not handle_id:
            jimmy_contact = find_jimmy_contact(conn)
            
            if jimmy_contact:
                print(f"\n✅ Found Jimmy: {jimmy_contact.get('display_name') or jimmy_contact['id']}")
                handle_id = jimmy_contact["rowid"]
            else:
                print("\n⚠️  Could not find Jimmy by name.")
                print("\n💡 Searching contacts...")
                # Try searching with common variations
                for search_term in ["jim", "jimmy", "james"]:
                    results = list_all_contacts(conn, limit=10, search_term=search_term)
                    if results:
                        print(f"\n✅ Found contacts matching '{search_term}':")
                        # Use first result
                        handle_id = results[0][0]
                        print(f"   Using: {results[0][4] or results[0][1]} (Handle ID: {handle_id})")
                        break
                
                if not handle_id:
                    print("\n💡 Listing top contacts...")
                    list_all_contacts(conn, limit=20)
                    print("\n💡 Usage options:")
                    print("   python3 read_jimmy_messages.py [phone_number]")
                    print("   python3 read_jimmy_messages.py [handle_rowid]")
                    print("   Example: python3 read_jimmy_messages.py +14076873157")
                    handle_id = None
        
        # Get messages
        if handle_id:
            messages = get_messages_with_jimmy(conn, handle_id)
            # Display messages
            display_messages(messages)
        else:
            print("\n⚠️  No handle ID specified. Cannot retrieve messages.")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

