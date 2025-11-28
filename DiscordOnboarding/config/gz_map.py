"""
GreatnessZone™ Map Configuration
Pattern: MAP × CHANNELS × REALMS × ONE
"""

from typing import List, Dict

# GreatnessZone™ Realms
REALMS = [
    "Rising Forge",
    "Mindspire",
    "Echo Nexus",
    "Chaos Gate"
]

# GreatnessZone™ Map Structure
GZ_MAP = {
    'HOME_BASE': {
        'name': ' Home Base',
        'description': 'Your starting point and journey hub',
        'realm': 'Rising Forge',
        'channels': [
            'start-here',
            'your-journey',
            'announcements',
        ],
        'icon': '',
        'color': 0x00ff00,  # Green
    },
    'GROWTH_LAB': {
        'name': ' Growth Lab',
        'description': 'Level up, challenges, and systems',
        'realm': 'Mindspire',
        'channels': [
            'daily-greatness',
            'challenges',
            'systems-lab',
            'vision-hall',
        ],
        'icon': '',
        'color': 0x5ac7ff,  # Blue/Cyan
    },
    'CREATOR_WING': {
        'name': ' Creator Wing',
        'description': 'Build, create, and showcase',
        'realm': 'Rising Forge',
        'channels': [
            'creative-forge',
            'builder-lab',
            'showcase',
        ],
        'icon': '',
        'color': 0xff5a5a,  # Red/Pink
    },
    'ECHO_NEXUS': {
        'name': ' Echo Nexus',
        'description': 'Connect, network, and build alliances',
        'realm': 'Echo Nexus',
        'channels': [
            'introductions',
            'networking',
            'guilds',
        ],
        'icon': '',
        'color': 0xffcc33,  # Yellow/Gold
    },
    'CHAOS_GATE': {
        'name': ' Chaos Gate',
        'description': 'AI, NPCs, and pure chaos',
        'realm': 'Chaos Gate',
        'channels': [
            'ai-summon',
            'npc-arena',
            'meme-dojo',
        ],
        'icon': '',
        'color': 0xff7af5,  # Magenta/Pink
    },
}

# Role to Map Area Mappings
ROLE_TO_MAP_AREAS = {
    'creative_warrior': ['CREATOR_WING', 'CHAOS_GATE'],
    'systems_wizard': ['GROWTH_LAB', 'HOME_BASE'],
    'quiet_assassin': ['GROWTH_LAB', 'CREATOR_WING'],
    'influence_architect': ['ECHO_NEXUS', 'HOME_BASE'],
    'vision_builder': ['CREATOR_WING', 'GROWTH_LAB'],
    'momentum_beast': ['CHAOS_GATE', 'CREATOR_WING'],
}

# Universal Access Channels (everyone gets these)
UNIVERSAL_CHANNELS = [
    'start-here',
    'announcements',
    'introductions',
]

def get_map_areas_for_role(role: str) -> List[str]:
    """Get map areas unlocked for a role"""
    return ROLE_TO_MAP_AREAS.get(role, ['HOME_BASE'])

def get_all_channels_for_role(role: str) -> List[str]:
    """Get all channels unlocked for a role"""
    areas = get_map_areas_for_role(role)
    channels = UNIVERSAL_CHANNELS.copy()
    
    for area_key in areas:
        if area_key in GZ_MAP:
            channels.extend(GZ_MAP[area_key]['channels'])
    
    # Remove duplicates
    return list(set(channels))

def get_all_channels_for_role_stack(role_stack: List[str]) -> List[str]:
    """Get all channels unlocked for a role stack"""
    all_channels = UNIVERSAL_CHANNELS.copy()
    
    for role in role_stack:
        areas = get_map_areas_for_role(role)
        for area_key in areas:
            if area_key in GZ_MAP:
                all_channels.extend(GZ_MAP[area_key]['channels'])
    
    # Remove duplicates
    return list(set(all_channels))

def get_map_data_for_role_stack(role_stack: List[str]) -> Dict:
    """Get map data with unlocked areas for role stack"""
    unlocked_areas = set()
    
    for role in role_stack:
        areas = get_map_areas_for_role(role)
        unlocked_areas.update(areas)
    
    # Always include HOME_BASE
    unlocked_areas.add('HOME_BASE')
    
    map_areas = []
    for area_key in unlocked_areas:
        if area_key in GZ_MAP:
            map_areas.append({
                'key': area_key,
                **GZ_MAP[area_key]
            })
    
    # Get realms for unlocked areas
    unlocked_realms = set()
    for area_key in unlocked_areas:
        if area_key in GZ_MAP and 'realm' in GZ_MAP[area_key]:
            unlocked_realms.add(GZ_MAP[area_key]['realm'])
    
    return {
        'unlocked_areas': list(unlocked_areas),
        'unlocked_realms': list(unlocked_realms),
        'map_areas': map_areas,
        'all_channels': get_all_channels_for_role_stack(role_stack),
        'realms': REALMS,
    }

def get_channels_by_realm(realm: str) -> List[str]:
    """Get all channels in a specific realm"""
    channels = []
    for area_key, area_data in GZ_MAP.items():
        if area_data.get('realm') == realm:
            channels.extend(area_data['channels'])
    return list(set(channels))

def get_areas_by_realm(realm: str) -> List[str]:
    """Get all map areas in a specific realm"""
    areas = []
    for area_key, area_data in GZ_MAP.items():
        if area_data.get('realm') == realm:
            areas.append(area_key)
    return areas

