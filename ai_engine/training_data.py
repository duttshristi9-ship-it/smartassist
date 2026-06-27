"""
AI Training Data
Intent corpus for disaster emergency classification
"""

# ============================================================
# TRAINING CORPUS
# Each entry: (text_sample, intent_label)
# ============================================================

TRAINING_DATA = [
    # ---- FLOOD EMERGENCY ----
    ("there is flooding near my house", "flood_emergency"),
    ("flood water is rising fast", "flood_emergency"),
    ("my area is flooded", "flood_emergency"),
    ("water level is increasing rapidly", "flood_emergency"),
    ("flood alert in my village", "flood_emergency"),
    ("river is overflowing", "flood_emergency"),
    ("heavy rainfall causing flood", "flood_emergency"),
    ("my house is surrounded by water", "flood_emergency"),
    ("flood near me what to do", "flood_emergency"),
    ("torrential rain flooding the street", "flood_emergency"),
    ("flash flood warning issued", "flood_emergency"),
    ("water is entering my home due to flood", "flood_emergency"),
    ("roads blocked due to flooding", "flood_emergency"),
    ("dam overflow causing flood downstream", "flood_emergency"),
    ("people stranded in flood water", "flood_emergency"),
    ("need evacuation due to flood", "flood_emergency"),
    ("flood safety tips please", "flood_emergency"),
    ("what to do in a flood situation", "flood_emergency"),
    ("flood hit our locality", "flood_emergency"),
    ("rising flood water emergency", "flood_emergency"),

    # ---- FIRE EMERGENCY ----
    ("there is a fire in my building", "fire_emergency"),
    ("fire broke out in my house", "fire_emergency"),
    ("my kitchen is on fire", "fire_emergency"),
    ("fire alarm going off", "fire_emergency"),
    ("smoke filling the room", "fire_emergency"),
    ("forest fire spreading near our village", "fire_emergency"),
    ("building is on fire help", "fire_emergency"),
    ("fire spreading very fast", "fire_emergency"),
    ("electrical fire in office", "fire_emergency"),
    ("fire emergency what should I do", "fire_emergency"),
    ("fire extinguisher not working", "fire_emergency"),
    ("how to escape from fire", "fire_emergency"),
    ("wildfire approaching our area", "fire_emergency"),
    ("gas leak causing fire", "fire_emergency"),
    ("children trapped in burning building", "fire_emergency"),
    ("fire in the neighborhood", "fire_emergency"),
    ("vehicle caught fire on highway", "fire_emergency"),
    ("fire safety instructions needed", "fire_emergency"),
    ("chimney fire in my house", "fire_emergency"),
    ("industrial fire near factory", "fire_emergency"),

    # ---- EARTHQUAKE HELP ----
    ("there was an earthquake just now", "earthquake_help"),
    ("earthquake hit our area", "earthquake_help"),
    ("strong tremors felt in the city", "earthquake_help"),
    ("building is shaking due to earthquake", "earthquake_help"),
    ("aftershock following earthquake", "earthquake_help"),
    ("what to do during earthquake", "earthquake_help"),
    ("earthquake safety tips", "earthquake_help"),
    ("collapsed building after earthquake", "earthquake_help"),
    ("people trapped under rubble", "earthquake_help"),
    ("seismic activity felt strongly", "earthquake_help"),
    ("ground shaking very badly", "earthquake_help"),
    ("earthquake occurred magnitude 6", "earthquake_help"),
    ("walls cracking due to tremors", "earthquake_help"),
    ("how to protect myself in earthquake", "earthquake_help"),
    ("earthquake emergency procedures", "earthquake_help"),
    ("rescue needed after earthquake", "earthquake_help"),
    ("building collapsed in earthquake", "earthquake_help"),
    ("survived earthquake need help", "earthquake_help"),
    ("earthquake warning system", "earthquake_help"),
    ("underground tremors detected", "earthquake_help"),

    # ---- MEDICAL SUPPORT ----
    ("my friend is injured badly", "medical_support"),
    ("someone is unconscious", "medical_support"),
    ("person having heart attack", "medical_support"),
    ("need medical emergency help", "medical_support"),
    ("someone collapsed on the street", "medical_support"),
    ("child is not breathing", "medical_support"),
    ("severe bleeding from wound", "medical_support"),
    ("person in shock after accident", "medical_support"),
    ("how to do CPR", "medical_support"),
    ("snake bite emergency", "medical_support"),
    ("allergic reaction severe", "medical_support"),
    ("broken bone after fall", "medical_support"),
    ("burn injury treatment", "medical_support"),
    ("poisoning emergency", "medical_support"),
    ("drowning victim need help", "medical_support"),
    ("heat stroke symptoms", "medical_support"),
    ("diabetic emergency insulin", "medical_support"),
    ("first aid for injury", "medical_support"),
    ("ambulance not arriving", "medical_support"),
    ("medical emergency at home", "medical_support"),

    # ---- SHELTER REQUEST ----
    ("I need a shelter", "shelter_request"),
    ("where can I find nearby shelter", "shelter_request"),
    ("looking for evacuation center", "shelter_request"),
    ("need temporary housing after disaster", "shelter_request"),
    ("displaced from home need shelter", "shelter_request"),
    ("relief camp location", "shelter_request"),
    ("government shelter during flood", "shelter_request"),
    ("emergency housing needed", "shelter_request"),
    ("where is nearest safe zone", "shelter_request"),
    ("evacuation route information", "shelter_request"),
    ("shelter for homeless after earthquake", "shelter_request"),
    ("refugee camp nearby", "shelter_request"),
    ("community center for disaster victims", "shelter_request"),
    ("need food and shelter immediately", "shelter_request"),
    ("stranded without shelter in rain", "shelter_request"),
    ("family needs shelter after cyclone", "shelter_request"),
    ("emergency accommodation needed", "shelter_request"),
    ("safe building to stay during storm", "shelter_request"),
    ("school being used as shelter", "shelter_request"),
    ("nearest relief centre address", "shelter_request"),

    # ---- RESCUE REQUEST ----
    ("please send rescue team", "rescue_request"),
    ("we are trapped need rescue", "rescue_request"),
    ("people stuck on rooftop", "rescue_request"),
    ("need helicopter rescue", "rescue_request"),
    ("stranded on flooded road", "rescue_request"),
    ("SOS emergency rescue needed", "rescue_request"),
    ("family members missing after disaster", "rescue_request"),
    ("rescue boat needed", "rescue_request"),
    ("trapped under collapsed building", "rescue_request"),
    ("need immediate rescue operation", "rescue_request"),
    ("cut off from rest of city", "rescue_request"),
    ("rescue team not responding", "rescue_request"),
    ("emergency evacuation needed quickly", "rescue_request"),
    ("people in danger need help", "rescue_request"),
    ("children trapped need rescue urgently", "rescue_request"),
    ("send help immediately", "rescue_request"),
    ("life threatening situation rescue now", "rescue_request"),
    ("call rescue services please", "rescue_request"),
    ("national disaster response force contact", "rescue_request"),
    ("emergency SOS signal", "rescue_request"),

    # ---- CYCLONE EMERGENCY ----
    ("cyclone is approaching our coast", "cyclone_emergency"),
    ("hurricane warning issued", "cyclone_emergency"),
    ("strong winds damaging houses", "cyclone_emergency"),
    ("typhoon hitting our area", "cyclone_emergency"),
    ("cyclone safety precautions", "cyclone_emergency"),
    ("what to do before cyclone", "cyclone_emergency"),
    ("tropical storm warning", "cyclone_emergency"),
    ("cyclone damaged my roof", "cyclone_emergency"),
    ("storm surge flooding coastal area", "cyclone_emergency"),
    ("violent winds uprooting trees", "cyclone_emergency"),
    ("cyclone landfall expected soon", "cyclone_emergency"),
    ("how to prepare for cyclone", "cyclone_emergency"),
    ("cyclone emergency kit", "cyclone_emergency"),
    ("power outage due to cyclone", "cyclone_emergency"),
    ("windows broken due to storm", "cyclone_emergency"),
    ("cyclone shelter location", "cyclone_emergency"),
    ("evacuation due to cyclone", "cyclone_emergency"),
    ("high speed winds cyclone", "cyclone_emergency"),
    ("cyclone warning red alert", "cyclone_emergency"),
    ("severe cyclonic storm approaching", "cyclone_emergency"),

    # ---- EMERGENCY CONTACT ----
    ("what is the emergency number", "emergency_contact"),
    ("give me police contact", "emergency_contact"),
    ("ambulance phone number", "emergency_contact"),
    ("fire department number", "emergency_contact"),
    ("disaster management helpline", "emergency_contact"),
    ("NDRF contact number", "emergency_contact"),
    ("coast guard emergency", "emergency_contact"),
    ("how to contact rescue services", "emergency_contact"),
    ("relief helpline number", "emergency_contact"),
    ("emergency hotline", "emergency_contact"),
    ("hospital emergency contact", "emergency_contact"),
    ("government disaster helpline", "emergency_contact"),
    ("who to call during emergency", "emergency_contact"),
    ("toll free number for disaster", "emergency_contact"),
    ("control room number", "emergency_contact"),
    ("local police number", "emergency_contact"),
    ("red cross contact", "emergency_contact"),
    ("NGO disaster relief contact", "emergency_contact"),
    ("national emergency number India", "emergency_contact"),
    ("dial 112 emergency services", "emergency_contact"),
]

# ============================================================
# INTENT LABELS AND METADATA
# ============================================================

INTENT_METADATA = {
    "flood_emergency": {
        "label": "Flood Emergency",
        "icon": "🌊",
        "color": "#3b82f6",
        "severity_default": "high",
        "escalate": True
    },
    "fire_emergency": {
        "label": "Fire Emergency",
        "icon": "🔥",
        "color": "#ef4444",
        "severity_default": "critical",
        "escalate": True
    },
    "earthquake_help": {
        "label": "Earthquake Help",
        "icon": "🏚️",
        "color": "#f59e0b",
        "severity_default": "high",
        "escalate": True
    },
    "medical_support": {
        "label": "Medical Emergency",
        "icon": "🏥",
        "color": "#ec4899",
        "severity_default": "critical",
        "escalate": True
    },
    "shelter_request": {
        "label": "Shelter Request",
        "icon": "🏠",
        "color": "#8b5cf6",
        "severity_default": "medium",
        "escalate": False
    },
    "rescue_request": {
        "label": "Rescue Request",
        "icon": "🚁",
        "color": "#dc2626",
        "severity_default": "critical",
        "escalate": True
    },
    "cyclone_emergency": {
        "label": "Cyclone Emergency",
        "icon": "🌀",
        "color": "#06b6d4",
        "severity_default": "high",
        "escalate": True
    },
    "emergency_contact": {
        "label": "Emergency Contact",
        "icon": "📞",
        "color": "#10b981",
        "severity_default": "medium",
        "escalate": False
    },
    "general": {
        "label": "General Query",
        "icon": "💬",
        "color": "#6b7280",
        "severity_default": "low",
        "escalate": False
    }
}

# Keywords for entity extraction
LOCATION_KEYWORDS = [
    'near', 'in', 'at', 'around', 'village', 'city', 'town', 'district',
    'road', 'street', 'area', 'region', 'coast', 'river', 'building', 'house',
    'locality', 'neighborhood', 'colony', 'sector', 'block', 'ward', 'zone'
]

SEVERITY_KEYWORDS = {
    'critical': ['critical', 'dying', 'life threatening', 'urgent', 'immediately', 'SOS', 'help now', 'emergency'],
    'high': ['bad', 'severe', 'serious', 'dangerous', 'fast', 'quickly', 'rapidly', 'strong', 'heavy'],
    'medium': ['need', 'require', 'help', 'assist', 'support', 'guidance'],
    'low': ['information', 'tips', 'advice', 'how to', 'what is', 'precaution', 'prepare']
}
