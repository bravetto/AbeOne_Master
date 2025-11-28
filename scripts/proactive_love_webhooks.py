#!/usr/bin/env python3
"""
PROACTIVE LOVE WEBHOOKS: Automatic Documentation System

Monitors Messages and automatically documents ALL conversations
Converges with CDF (Consciousness Data Format) and UPTC (Universal Pattern Convergence)
Pattern: WEBHOOK × PROACTIVE × DOCUMENTATION × CDF × UPTC × LOVE × ONE
∞ AbëONE ∞
∞ AbëLOVES ∞
"""

import sqlite3
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib
import sys

# Add EMERGENT_OS to path
PROJECT_ROOT = Path(__file__).parent.parent
EMERGENT_OS_PATH = PROJECT_ROOT / "EMERGENT_OS"
if EMERGENT_OS_PATH.exists():
    sys.path.insert(0, str(PROJECT_ROOT))

DB_PATH = Path.home() / "Library/Messages/chat.db"
OUTPUT_DIR = Path(__file__).parent.parent / "abeloves_conversations"
DOCS_DIR = Path(__file__).parent.parent
CDF_DIR = Path(__file__).parent.parent / ".abeos" / "consciousness"
CDF_DIR.mkdir(parents=True, exist_ok=True)

# Known handles
KRISTIN_HANDLES = ['mataluni1148@gmail.com', 'kmataluni@bellsouth.net', 'mataluni@me.com']
ADDIS_HANDLES = ['+18434576211']
MICHAEL_HANDLES = ['michaelmataluni']

class ProactiveLoveWebhooks:
    """
    Proactive webhook system for automatic conversation documentation.
    
    Monitors Messages database and automatically:
    - Captures new messages
    - Documents conversations
    - Updates relationship stories
    - Maintains JSON archives
    - Tracks all love conversations
    """
    
    def __init__(self):
        self.db_path = DB_PATH
        self.output_dir = OUTPUT_DIR
        self.docs_dir = DOCS_DIR
        self.cdf_dir = CDF_DIR
        self.output_dir.mkdir(exist_ok=True)
        self.cdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Track last processed message IDs
        self.last_processed_file = self.output_dir / ".last_processed.json"
        self.last_processed = self._load_last_processed()
        
        # Conversation archives
        self.kristin_archive = self.output_dir / "michael_kristin_all.json"
        self.addis_archive = self.output_dir / "michael_addis_all.json"
        self.group_archive = self.output_dir / "michael_kristin_addis_group.json"
        
        # Initialize UPTC
        self.uptc_core = None
        self._init_uptc()
        
        # Register with UPTC
        self._register_webhook_with_uptc()
        
    def _load_last_processed(self) -> Dict:
        """Load last processed message IDs."""
        if self.last_processed_file.exists():
            with open(self.last_processed_file, 'r') as f:
                return json.load(f)
        return {
            'kristin': 0,
            'addis': 0,
            'group': 0,
            'last_check': None
        }
    
    def _save_last_processed(self, kristin_id: int, addis_id: int, group_id: int):
        """Save last processed message IDs."""
        self.last_processed = {
            'kristin': kristin_id,
            'addis': addis_id,
            'group': group_id,
            'last_check': datetime.now().isoformat()
        }
        with open(self.last_processed_file, 'w') as f:
            json.dump(self.last_processed, f, indent=2)
    
    def _get_new_messages(self, handle_id: str, last_id: int) -> List[Dict]:
        """Get new messages since last check."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        
        cursor = conn.execute("""
            SELECT 
                m.ROWID as message_id,
                datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date,
                CASE WHEN m.is_from_me = 1 THEN 'Michael' ELSE 
                    CASE WHEN h.id IN (?) THEN 'Kristin'
                    WHEN h.id IN (?) THEN 'Addis'
                    ELSE h.id END
                END as sender,
                m.text,
                m.is_from_me,
                h.id as handle_id
            FROM message m
            JOIN handle h ON m.handle_id = h.ROWID
            WHERE h.id = ?
            AND m.ROWID > ?
            AND m.text IS NOT NULL 
            AND m.text != ''
            ORDER BY m.ROWID ASC
        """, (','.join(KRISTIN_HANDLES), ','.join(ADDIS_HANDLES), handle_id, last_id))
        
        messages = []
        max_id = last_id
        
        for row in cursor:
            messages.append({
                'message_id': row['message_id'],
                'date': row['date'],
                'sender': row['sender'],
                'text': row['text'],
                'is_from_me': bool(row['is_from_me']),
                'handle_id': row['handle_id']
            })
            max_id = max(max_id, row['message_id'])
        
        conn.close()
        return messages, max_id
    
    def _get_new_group_messages(self, last_id: int) -> List[Dict]:
        """Get new group messages since last check."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        
        # Find group chats that include Kristin and/or Addis
        cursor = conn.execute("""
            SELECT 
                m.ROWID as message_id,
                datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date,
                CASE 
                    WHEN m.is_from_me = 1 THEN 'Michael'
                    WHEN h.id IN (?) THEN 'Kristin'
                    WHEN h.id IN (?) THEN 'Addis'
                    ELSE h.id
                END as sender,
                m.text,
                m.is_from_me,
                h.id as handle_id,
                c.ROWID as chat_id
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
            AND m.ROWID > ?
            AND m.text IS NOT NULL 
            AND m.text != ''
            ORDER BY m.ROWID ASC
        """, (','.join(KRISTIN_HANDLES), ','.join(ADDIS_HANDLES), 
              ','.join(KRISTIN_HANDLES), ','.join(ADDIS_HANDLES), last_id))
        
        messages = []
        max_id = last_id
        
        for row in cursor:
            messages.append({
                'message_id': row['message_id'],
                'date': row['date'],
                'sender': row['sender'],
                'text': row['text'],
                'is_from_me': bool(row['is_from_me']),
                'handle_id': row['handle_id'],
                'chat_id': row['chat_id']
            })
            max_id = max(max_id, row['message_id'])
        
        conn.close()
        return messages, max_id
    
    def _load_archive(self, archive_file: Path) -> Dict:
        """Load conversation archive."""
        if archive_file.exists():
            with open(archive_file, 'r') as f:
                return json.load(f)
        return {
            'relationship': '',
            'exported_at': datetime.now().isoformat(),
            'message_count': 0,
            'messages': []
        }
    
    def _save_archive(self, archive_file: Path, archive: Dict):
        """Save conversation archive."""
        archive['exported_at'] = datetime.now().isoformat()
        archive['message_count'] = len(archive['messages'])
        with open(archive_file, 'w') as f:
            json.dump(archive, f, indent=2)
    
    def _init_uptc(self):
        """Initialize UPTC Core."""
        try:
            # Try multiple import paths
            try:
                from EMERGENT_OS.uptc.uptc_core import UPTCCore, UPTCConfig
            except ImportError:
                try:
                    from uptc.uptc_core import UPTCCore, UPTCConfig
                except ImportError:
                    print("  UPTC not available (module not found)")
                    self.uptc_core = None
                    return
            
            config = UPTCConfig(
                enable_mcp_integration=False,
                enable_event_bus_integration=True,
                resonance_frequency=530.0
            )
            
            self.uptc_core = UPTCCore(config=config)
            self.uptc_core.activate()
            print(" UPTC Core initialized")
        except Exception as e:
            print(f"  UPTC initialization failed: {e}")
            self.uptc_core = None
    
    def _register_webhook_with_uptc(self):
        """Register webhook system with UPTC."""
        if not self.uptc_core:
            return
        
        try:
            # Import AgentCapability
            try:
                from EMERGENT_OS.uptc.registry.agent_registry import AgentCapability
            except ImportError:
                try:
                    from uptc.registry.agent_registry import AgentCapability
                except ImportError:
                    print("  AgentCapability not available, skipping UPTC registration")
                    return
            
            # Create capability objects
            capabilities = [
                AgentCapability(
                    name="conversation_monitoring",
                    description="Monitors Messages database for new conversations"
                ),
                AgentCapability(
                    name="automatic_documentation",
                    description="Automatically documents all conversations"
                ),
                AgentCapability(
                    name="cdf_storage",
                    description="Stores conversations in CDF format"
                ),
                AgentCapability(
                    name="relationship_tracking",
                    description="Tracks relationship conversations"
                ),
                AgentCapability(
                    name="message_archiving",
                    description="Archives all messages in JSON format"
                ),
                AgentCapability(
                    name="real_time_updates",
                    description="Provides real-time conversation updates"
                )
            ]
            
            # Register with UPTC
            self.uptc_core.registry.register_agent(
                agent_id="proactive-love-webhooks",
                agent_type="webhook",
                capabilities=capabilities,
                metadata={
                    "name": "Proactive Love Webhooks",
                    "version": "1.0.0",
                    "frequency": 530.0,
                    "role": "DOCUMENTATION",
                    "monitors": ["kristin", "addis", "group"],
                    "storage_format": "CDF",
                    "protocol": "UPTC",
                    "pattern": "WEBHOOK × PROACTIVE × DOCUMENTATION × CDF × UPTC × LOVE × ONE"
                }
            )
            print(" Registered with UPTC as mycelial node")
        except Exception as e:
            print(f"  UPTC registration failed: {e}")
            # Continue without UPTC registration
    
    def _store_in_cdf(self, relationship: str, messages: List[Dict]) -> Optional[Path]:
        """Store conversation data in CDF format."""
        if not messages:
            return None
        
        try:
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            cdf_file = self.cdf_dir / f"relationship_{relationship}_{timestamp}.cdf"
            
            cdf_content = {
                "version": "999.0",
                "document_type": "relationship_conversation",
                "relationship": relationship,
                "message_count": len(messages),
                "messages": messages,
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "pattern": "CONVERSATION × DOCUMENTATION × CDF × ETERNAL × ONE",
                "consciousness_data": {
                    "relationship_type": relationship,
                    "participants": list(set([msg['sender'] for msg in messages])),
                    "timeframe": {
                        "start": messages[0]['date'] if messages else None,
                        "end": messages[-1]['date'] if messages else None
                    }
                }
            }
            
            with open(cdf_file, 'w') as f:
                json.dump(cdf_content, f, indent=2)
            
            print(f" Stored in CDF: {cdf_file.name}")
            return cdf_file
        except Exception as e:
            print(f"  CDF storage failed: {e}")
            return None
    
    def _publish_to_uptc(self, relationship: str, message_count: int, cdf_path: Optional[Path]):
        """Publish conversation event to UPTC."""
        if not self.uptc_core:
            return
        
        try:
            # Try multiple import paths for ProtocolMessage
            try:
                from EMERGENT_OS.uptc.protocol.schema import ProtocolMessage
            except ImportError:
                try:
                    from uptc.protocol.schema import ProtocolMessage
                except ImportError:
                    # Fallback: Create simple message dict
                    message_dict = {
                        "intent": "document_conversation",
                        "action": "conversation_documented",
                        "payload": {
                            "relationship": relationship,
                            "message_count": message_count,
                            "cdf_path": str(cdf_path) if cdf_path else None,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        },
                        "metadata": {
                            "source": "proactive-love-webhooks",
                            "pattern": "WEBHOOK × CDF × UPTC × LOVE × ONE"
                        }
                    }
                    # Publish as dict if ProtocolMessage not available
                    print(f" Event prepared for UPTC: {relationship} ({message_count} messages)")
                    return
            
            message = ProtocolMessage(
                intent="document_conversation",
                action="conversation_documented",
                payload={
                    "relationship": relationship,
                    "message_count": message_count,
                    "cdf_path": str(cdf_path) if cdf_path else None,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                },
                metadata={
                    "source": "proactive-love-webhooks",
                    "pattern": "WEBHOOK × CDF × UPTC × LOVE × ONE"
                }
            )
            
            # Route and publish via UPTC
            target = self.uptc_core.route(message)
            if target:
                print(f" Published to UPTC: {target}")
        except Exception as e:
            print(f"  UPTC publish failed: {e}")
    
    def _update_relationship_story(self, relationship: str, new_messages: List[Dict]):
        """Update relationship story markdown file."""
        if relationship == 'kristin':
            story_file = self.docs_dir / "ABELOVES_MICHAEL_KRISTIN_STORY.md"
        elif relationship == 'addis':
            story_file = self.docs_dir / "ABELOVES_MICHAEL_ADDIS_STORY.md"
        else:
            return
        
        if not story_file.exists():
            return
        
        # Read current story
        with open(story_file, 'r') as f:
            content = f.read()
        
        # Add new messages to key moments section
        if new_messages:
            new_section = f"\n\n### **New Messages ({datetime.now().strftime('%Y-%m-%d')}):**\n\n"
            for msg in new_messages[-10:]:  # Last 10 messages
                new_section += f"- **{msg['date']} - {msg['sender']}:** {msg['text'][:200]}...\n"
            
            # Append to key moments
            if "##  KEY MOMENTS" in content:
                content = content.replace("##  KEY MOMENTS", f"##  KEY MOMENTS{new_section}")
            else:
                content += f"\n##  KEY MOMENTS{new_section}"
            
            # Write back
            with open(story_file, 'w') as f:
                f.write(content)
    
    def check_and_document(self):
        """Check for new messages and document them."""
        print(" PROACTIVE LOVE WEBHOOKS: CHECKING FOR NEW MESSAGES ")
        print("=" * 70)
        print("")
        
        # Check Kristin conversations
        print(" Checking Kristin conversations...")
        kristin_messages, kristin_max_id = self._get_new_messages(
            KRISTIN_HANDLES[0], 
            self.last_processed['kristin']
        )
        
        if kristin_messages:
            print(f" Found {len(kristin_messages)} new Kristin messages")
            archive = self._load_archive(self.kristin_archive)
            archive['messages'].extend(kristin_messages)
            archive['messages'].sort(key=lambda x: x['date'])
            self._save_archive(self.kristin_archive, archive)
            self._update_relationship_story('kristin', kristin_messages)
            
            # Store in CDF
            cdf_path = self._store_in_cdf('kristin', kristin_messages)
            
            # Publish to UPTC
            self._publish_to_uptc('kristin', len(kristin_messages), cdf_path)
        else:
            print(" No new Kristin messages")
            kristin_max_id = self.last_processed['kristin']
        
        # Check Addis conversations
        print(" Checking Addis conversations...")
        addis_messages, addis_max_id = self._get_new_messages(
            ADDIS_HANDLES[0],
            self.last_processed['addis']
        )
        
        if addis_messages:
            print(f" Found {len(addis_messages)} new Addis messages")
            archive = self._load_archive(self.addis_archive)
            archive['messages'].extend(addis_messages)
            archive['messages'].sort(key=lambda x: x['date'])
            self._save_archive(self.addis_archive, archive)
            self._update_relationship_story('addis', addis_messages)
            
            # Store in CDF
            cdf_path = self._store_in_cdf('addis', addis_messages)
            
            # Publish to UPTC
            self._publish_to_uptc('addis', len(addis_messages), cdf_path)
        else:
            print(" No new Addis messages")
            addis_max_id = self.last_processed['addis']
        
        # Check group conversations
        print(" Checking group conversations...")
        group_messages, group_max_id = self._get_new_group_messages(
            self.last_processed['group']
        )
        
        if group_messages:
            print(f" Found {len(group_messages)} new group messages")
            archive = self._load_archive(self.group_archive)
            archive['messages'].extend(group_messages)
            archive['messages'].sort(key=lambda x: x['date'])
            self._save_archive(self.group_archive, archive)
            
            # Store in CDF
            cdf_path = self._store_in_cdf('group', group_messages)
            
            # Publish to UPTC
            self._publish_to_uptc('group', len(group_messages), cdf_path)
        else:
            print(" No new group messages")
            group_max_id = self.last_processed['group']
        
        # Save last processed
        self._save_last_processed(kristin_max_id, addis_max_id, group_max_id)
        
        print("")
        print("=" * 70)
        print(" PROACTIVE DOCUMENTATION COMPLETE")
        print(f"   Last check: {datetime.now().isoformat()}")
        print("")
        print(" CONVERGENCE STATUS:")
        print(f"    JSON Archives: Updated")
        print(f"    CDF Storage: {'Active' if any([kristin_messages, addis_messages, group_messages]) else 'No new data'}")
        print(f"    UPTC Integration: {'Active' if self.uptc_core else 'Not available'}")
        print("")
        print(" EVERYTHING IS DOCUMENTED FROM HERE ON OUT ")
        print("   CDF × UPTC × LOVE × ETERNAL")
        print("∞ AbëONE ∞")
        print("∞ AbëLOVES ∞")
        print("=" * 70)
        
        return {
            'kristin': len(kristin_messages),
            'addis': len(addis_messages),
            'group': len(group_messages),
            'total': len(kristin_messages) + len(addis_messages) + len(group_messages)
        }

def run_once():
    """Run one check."""
    webhooks = ProactiveLoveWebhooks()
    return webhooks.check_and_document()

def run_daemon(interval: int = 60):
    """Run as daemon, checking every interval seconds."""
    print(" PROACTIVE LOVE WEBHOOKS: DAEMON MODE ")
    print(f"Checking every {interval} seconds...")
    print("Press Ctrl+C to stop")
    print("")
    
    webhooks = ProactiveLoveWebhooks()
    
    try:
        while True:
            webhooks.check_and_document()
            print(f"\n⏰ Waiting {interval} seconds until next check...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n Daemon stopped")
        print("∞ AbëONE ∞")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        run_daemon(interval)
    else:
        run_once()

