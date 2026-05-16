"""
AI Response Engine
Generates context-aware emergency responses based on classified intent
"""

import random
from typing import Dict, Any, List
from .intent_classifier import get_classifier


# ============================================================
# RESPONSE TEMPLATES PER INTENT
# ============================================================

RESPONSE_TEMPLATES = {
    "flood_emergency": [
        {
            "response": (
                "🌊 **FLOOD EMERGENCY DETECTED** — Stay calm and act immediately!\n\n"
                "**Immediate Actions:**\n"
                "• Move to higher ground RIGHT NOW — do not wait\n"
                "• Avoid walking through flowing water (6 inches can knock you down)\n"
                "• Stay away from electrical poles and fallen wires\n"
                "• Turn off utilities at main switches if safe to do so\n"
                "• Do NOT drive through flooded roads\n\n"
                "**Emergency Numbers:** 🆘 Dial **112** | NDRF: **011-24363260**\n\n"
                "Do you need nearby shelter information or rescue assistance?"
            ),
            "follow_up": "Are you currently in a safe location? Do you need evacuation help?"
        },
        {
            "response": (
                "🌊 **Flood Alert Response:**\n\n"
                "Your safety is the top priority. Please:\n"
                "1. **Evacuate immediately** if water is rising near you\n"
                "2. Take essential documents (Aadhaar, passport) in a waterproof bag\n"
                "3. Signal for help from your rooftop if trapped\n"
                "4. Call **NDRF Helpline: 011-24363260** for rescue\n"
                "5. Follow official evacuation routes only\n\n"
                "⚠️ Do not attempt to swim through floodwater — currents are deceptive!"
            ),
            "follow_up": "Should I find the nearest flood relief shelter for you?"
        }
    ],

    "fire_emergency": [
        {
            "response": (
                "🔥 **FIRE EMERGENCY — EVACUATE IMMEDIATELY!**\n\n"
                "**Critical Steps (Act in 90 seconds):**\n"
                "• Pull the fire alarm if available\n"
                "• Call **Fire Services: 101** immediately\n"
                "• Crawl low under smoke — clean air is near the floor\n"
                "• Feel doors before opening — if hot, DO NOT open\n"
                "• Use stairs ONLY (never elevator during fire)\n"
                "• Meet at your designated assembly point\n\n"
                "**If trapped:** Close doors, signal from window, call 101\n\n"
                "🆘 **Fire Emergency: 101 | National Emergency: 112**"
            ),
            "follow_up": "Are you currently inside the building? How many people are with you?"
        },
        {
            "response": (
                "🔥 **Fire Safety Response:**\n\n"
                "• **STOP, DROP & ROLL** if clothes catch fire\n"
                "• Use a wet cloth over your mouth and nose\n"
                "• Keep all doors closed to slow fire spread\n"
                "• Never go back inside a burning building\n"
                "• Account for everyone at the meeting point\n\n"
                "**Contact:** Fire Department **101** | Emergency **112**\n\n"
                "Is the fire department already notified? Do you need first aid guidance?"
            ),
            "follow_up": "Is everyone out of the building safely?"
        }
    ],

    "earthquake_help": [
        {
            "response": (
                "🏚️ **EARTHQUAKE SAFETY RESPONSE**\n\n"
                "**During shaking — DROP, COVER, HOLD ON:**\n"
                "• Drop to hands and knees immediately\n"
                "• Take cover under a sturdy desk/table or against interior wall\n"
                "• Hold on until shaking stops\n"
                "• Stay away from windows, shelves, and heavy objects\n"
                "• If outdoors — stay in open areas, away from buildings\n\n"
                "**After shaking stops:**\n"
                "• Check yourself for injuries\n"
                "• Be prepared for aftershocks\n"
                "• Do not use elevators\n"
                "• Check for gas leaks — if detected, evacuate and call **112**\n\n"
                "🆘 **NDRF: 011-24363260 | Emergency: 112**"
            ),
            "follow_up": "Are you or anyone nearby injured? Is the building structurally safe?"
        }
    ],

    "medical_support": [
        {
            "response": (
                "🏥 **MEDICAL EMERGENCY RESPONSE**\n\n"
                "**CALL AMBULANCE NOW: 108** (Free emergency service)\n\n"
                "**While waiting for help:**\n"
                "• Check if the person is conscious and breathing\n"
                "• If not breathing — start CPR: 30 chest compressions + 2 rescue breaths\n"
                "• Control bleeding with firm pressure using a clean cloth\n"
                "• Do NOT move a person with suspected spinal injury\n"
                "• Keep them warm and calm\n"
                "• Clear the airway if unconscious (recovery position)\n\n"
                "**Emergency Contacts:**\n"
                "🚑 Ambulance: **108** | Emergency: **112** | Red Cross: **011-23711551**"
            ),
            "follow_up": "Is the person conscious and breathing? Should I guide you through CPR steps?"
        },
        {
            "response": (
                "🏥 **Medical Emergency Detected!**\n\n"
                "Please call **108 (Ambulance)** immediately!\n\n"
                "**First Aid Basics:**\n"
                "• Stay with the patient — do not leave them alone\n"
                "• Keep them lying down with legs elevated (unless head/chest injury)\n"
                "• Loosen tight clothing around neck and chest\n"
                "• Do not give food or water to an unconscious person\n"
                "• Document symptoms to tell the paramedics\n\n"
                "Is this a cardiac event, trauma, or breathing problem? I can give specific guidance."
            ),
            "follow_up": "What are the exact symptoms? Age of the patient?"
        }
    ],

    "shelter_request": [
        {
            "response": (
                "🏠 **SHELTER ASSISTANCE**\n\n"
                "I can help you find emergency shelter. Here are your options:\n\n"
                "**Government Shelters:**\n"
                "• Contact your local District Collector's office\n"
                "• Schools and community halls are often designated as relief camps\n"
                "• Call **State Disaster Helpline** for your area\n\n"
                "**National Resources:**\n"
                "• NDRF Shelter Line: **011-24363260**\n"
                "• Red Cross Emergency: **1800-180-0900** (Toll-free)\n"
                "• PM Relief Fund: **011-23388061**\n\n"
                "**What to Bring:**\n"
                "Essential documents, medications, warm clothing, water (1L per person)\n\n"
                "📍 Can you share your city/district? I'll provide more specific shelter locations."
            ),
            "follow_up": "How many people need shelter? Do you have any special medical needs?"
        }
    ],

    "rescue_request": [
        {
            "response": (
                "🚁 **RESCUE REQUEST RECEIVED — ESCALATING!**\n\n"
                "⚠️ **CALL IMMEDIATELY:**\n"
                "• **Emergency: 112**\n"
                "• **NDRF (National Disaster Response Force): 011-24363260**\n"
                "• **Coast Guard (if near water): 1554**\n"
                "• **Police: 100**\n\n"
                "**While awaiting rescue:**\n"
                "• Stay in a visible location\n"
                "• Signal rescuers with bright cloth, mirror, or torch\n"
                "• If on rooftop — write SOS in large letters\n"
                "• Conserve phone battery — only essential calls\n"
                "• Stay together as a group — do not separate\n\n"
                "🆘 **Your report has been flagged as CRITICAL for admin review.**"
            ),
            "follow_up": "How many people need rescue? What is your exact location or landmark?"
        }
    ],

    "cyclone_emergency": [
        {
            "response": (
                "🌀 **CYCLONE EMERGENCY PROTOCOL**\n\n"
                "**Before Cyclone Hits:**\n"
                "• Board up windows and doors immediately\n"
                "• Store 72-hour emergency supplies (water, food, medicines)\n"
                "• Charge all devices and power banks\n"
                "• Know your evacuation route and nearest cyclone shelter\n"
                "• Tie down or bring in outdoor furniture\n\n"
                "**During Cyclone:**\n"
                "• Stay indoors, away from windows\n"
                "• If eye passes — do NOT go outside (more wind is coming)\n"
                "• Avoid flooded areas — storm surges are deadly\n\n"
                "**Emergency:** India Meteorological Dept: **1800-180-1717**\n"
                "NDRF: **011-24363260** | Emergency: **112**"
            ),
            "follow_up": "Is the cyclone approaching or have you already been impacted?"
        }
    ],

    "emergency_contact": [
        {
            "response": (
                "📞 **INDIA EMERGENCY CONTACTS**\n\n"
                "| Service | Number |\n"
                "|---------|--------|\n"
                "| 🆘 National Emergency | **112** |\n"
                "| 🚑 Ambulance | **108** |\n"
                "| 🔥 Fire Services | **101** |\n"
                "| 👮 Police | **100** |\n"
                "| 🚢 Coast Guard | **1554** |\n"
                "| 🏚️ NDRF Disaster Response | **011-24363260** |\n"
                "| 🌊 Flood Control | **1800-180-5999** |\n"
                "| 🏥 Medical Helpline | **104** |\n"
                "| ☎️ IMD Weather | **1800-180-1717** |\n"
                "| 🔴 PM Relief Fund | **011-23388061** |\n"
                "| ❤️ Red Cross | **1800-180-0900** |\n\n"
                "💡 **Tip:** Save **112** as your first emergency dial — it connects to all services."
            ),
            "follow_up": "Is there a specific emergency service you're trying to reach?"
        }
    ],

    "general": [
        {
            "response": (
                "👋 **Hello! I'm SmartAssist — Your AI Emergency Guide.**\n\n"
                "I'm here to help you during disasters and emergencies. I can assist with:\n\n"
                "• 🌊 **Flood** guidance and evacuation\n"
                "• 🔥 **Fire** safety and escape\n"
                "• 🏚️ **Earthquake** response\n"
                "• 🏥 **Medical** emergencies\n"
                "• 🏠 **Shelter** finding\n"
                "• 🚁 **Rescue** coordination\n"
                "• 🌀 **Cyclone** preparedness\n"
                "• 📞 **Emergency contacts**\n\n"
                "Please describe your situation and I'll provide immediate guidance."
            ),
            "follow_up": "What type of emergency are you facing right now?"
        },
        {
            "response": (
                "ℹ️ I'm SmartAssist, your AI disaster management assistant.\n\n"
                "I can help you with emergency situations including floods, fires, "
                "earthquakes, medical emergencies, shelter needs, and rescue coordination.\n\n"
                "Please tell me more about your situation so I can provide targeted assistance.\n\n"
                "**Quick Help:** Type the type of emergency you're facing (e.g., 'flood help', 'fire escape', 'need shelter')"
            ),
            "follow_up": "What is your current emergency situation?"
        }
    ]
}

# ============================================================
# ESCALATION ALERT TEMPLATES
# ============================================================

ESCALATION_ALERTS = [
    "⚠️ **CRITICAL ALERT:** This situation has been flagged for immediate attention. Emergency services should be contacted NOW.",
    "🆘 **URGENT:** Based on your message, this appears to be a life-threatening situation. Please call 112 immediately.",
    "🔴 **HIGH PRIORITY:** Your report has been escalated to our emergency response system."
]

# ============================================================
# TIPS AND PRECAUTIONARY RESPONSES
# ============================================================

SAFETY_TIPS = {
    "flood": [
        "Keep a waterproof emergency kit with documents, medications, and cash.",
        "Know your local evacuation routes before disasters strike.",
        "Never walk or drive through flooded waters — just 6 inches can sweep you away.",
        "Store emergency water (1 gallon per person per day for 3 days).",
    ],
    "fire": [
        "Test smoke detectors monthly and replace batteries annually.",
        "Have a fire escape plan with two ways out of every room.",
        "Keep fire extinguishers accessible — know how to use PASS technique.",
        "Never leave cooking unattended — it's the #1 cause of home fires.",
    ],
    "earthquake": [
        "Secure heavy furniture and appliances to walls.",
        "Keep an emergency kit under your bed with shoes and flashlight.",
        "Identify safe spots in each room: under sturdy tables, against interior walls.",
        "Learn to shut off gas, water, and electricity at main switches.",
    ]
}


class ResponseEngine:
    """
    Generates intelligent, context-aware responses to disaster emergency queries.
    Integrates with the intent classifier and an ML feedback loop for adaptive responses.
    """
    
    def __init__(self):
        self.classifier = get_classifier()
        
        # ML Feedback Loop components
        from sklearn.linear_model import SGDRegressor
        from sklearn.feature_extraction.text import HashingVectorizer
        self.vectorizer = HashingVectorizer(n_features=1000)
        self.feedback_model = SGDRegressor(learning_rate='constant', eta0=0.01)
        self.is_model_trained = False
        
    def submit_feedback(self, message: str, intent: str, template_idx: int, rating: float):
        """
        Train the feedback model online with user feedback (rating 0.0 to 1.0).
        """
        try:
            # Create feature vector: combine message and template index
            feature_text = f"{intent} {message} template_{template_idx}"
            X = self.vectorizer.transform([feature_text])
            y = [rating]
            
            # Partial fit for online learning
            self.feedback_model.partial_fit(X, y)
            self.is_model_trained = True
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Feedback training failed: {e}")
    
    def _rank_templates(self, message: str, intent: str, templates: List[Dict]) -> Dict:
        """
        Rank templates using the ML feedback model and return the best one.
        """
        if not self.is_model_trained or len(templates) == 1:
            return random.choice(templates), 0
            
        best_template = templates[0]
        best_score = -float('inf')
        best_idx = 0
        
        for idx, template in enumerate(templates):
            try:
                feature_text = f"{intent} {message} template_{idx}"
                X = self.vectorizer.transform([feature_text])
                score = self.feedback_model.predict(X)[0]
                
                # Add slight randomization for exploration
                score += random.uniform(-0.1, 0.1)
                
                if score > best_score:
                    best_score = score
                    best_template = template
                    best_idx = idx
            except:
                pass
                
        return best_template, best_idx

    def generate_response(self, user_message: str, chat_context: List[Dict] = None) -> Dict[str, Any]:
        """
        Main method to generate AI response for a user message.
        
        Args:
            user_message: The user's input text
            chat_context: Previous conversation messages for context
        
        Returns:
            dict with response, intent, severity, escalation flag, follow_up
        """
        # Classify intent and extract entities
        entities = self.classifier.extract_entities(user_message)
        intent = entities['intent']
        severity = entities['severity']
        confidence = entities['confidence']
        needs_escalation = entities['needs_escalation']
        
        # Select response template using ML Ranking
        templates = RESPONSE_TEMPLATES.get(intent, RESPONSE_TEMPLATES['general'])
        template, template_idx = self._rank_templates(user_message, intent, templates)
        
        response_text = template['response']
        follow_up = template.get('follow_up', '')
        
        # Add escalation warning for critical situations
        if needs_escalation and severity in ['critical', 'high']:
            escalation_msg = random.choice(ESCALATION_ALERTS)
            response_text = f"{escalation_msg}\n\n---\n\n{response_text}"
        
        # Add context-aware additions based on keywords
        response_text = self._add_contextual_details(
            response_text, user_message, intent
        )
        
        return {
            'response': response_text,
            'follow_up': follow_up,
            'intent': intent,
            'confidence': round(confidence, 3),
            'severity': severity,
            'needs_escalation': needs_escalation,
            'disaster_type': entities['disaster_type'],
            'icon': entities['icon'],
            'location': entities.get('location'),
            'template_idx': template_idx
        }
    
    def _add_contextual_details(self, response: str, message: str, intent: str) -> str:
        """Add contextual details based on message content"""
        message_lower = message.lower()
        
        # Add CPR guidance if mentioned
        if 'cpr' in message_lower or 'not breathing' in message_lower:
            cpr_guide = (
                "\n\n**CPR Steps:**\n"
                "1. Place heel of hand on center of chest\n"
                "2. Push hard and fast (2 inches deep, 100-120/min)\n"
                "3. Give 2 rescue breaths after 30 compressions\n"
                "4. Continue until help arrives"
            )
            response += cpr_guide
        
        # Add children-specific guidance
        if 'child' in message_lower or 'children' in message_lower or 'baby' in message_lower:
            response += "\n\n👶 **For children:** Keep them calm, carry them if possible. Children are priority in evacuation."
        
        # Add night-time guidance
        if 'night' in message_lower or 'dark' in message_lower:
            response += "\n\n🔦 **Night Emergency Tip:** Use your phone flashlight or torch. Signal rescuers with flashing light."
        
        return response
    
    def get_disaster_info(self, disaster_type: str) -> Dict:
        """Get comprehensive information about a specific disaster type"""
        info_map = {
            'flood': {
                'title': 'Flood Emergency Guide',
                'icon': '🌊',
                'causes': 'Heavy rainfall, dam failures, river overflow, coastal storms',
                'warning_signs': 'Rapidly rising water levels, unusual river flow, weather alerts',
                'dos': [
                    'Move to higher ground immediately',
                    'Follow official evacuation orders',
                    'Disconnect electrical appliances',
                    'Take emergency kit with essentials',
                    'Keep tuned to weather broadcasts'
                ],
                'donts': [
                    "Don't walk through moving floodwater",
                    "Don't drive through flooded roads",
                    "Don't ignore evacuation warnings",
                    "Don't touch electrical equipment if wet",
                    "Don't drink floodwater"
                ],
                'contacts': [('NDRF', '011-24363260'), ('Flood Control Room', '1800-180-5999'), ('Emergency', '112')]
            },
            'fire': {
                'title': 'Fire Emergency Guide',
                'icon': '🔥',
                'causes': 'Electrical faults, cooking accidents, gas leaks, arson, wildfires',
                'warning_signs': 'Smoke smell, unusual heat, sparking wires, burning odor',
                'dos': [
                    'Evacuate immediately',
                    'Call Fire Services: 101',
                    'Crawl below smoke',
                    'Use stairways not elevators',
                    'Stop, drop and roll if on fire'
                ],
                'donts': [
                    "Don't go back inside burning building",
                    "Don't use elevators",
                    "Don't open hot doors",
                    "Don't hide from firefighters",
                    "Don't waste time collecting possessions"
                ],
                'contacts': [('Fire Services', '101'), ('Emergency', '112'), ('Ambulance', '108')]
            },
            'earthquake': {
                'title': 'Earthquake Safety Guide',
                'icon': '🏚️',
                'causes': 'Tectonic plate movements, volcanic activity, underground nuclear tests',
                'warning_signs': 'Animal behavior changes, ground vibrations, groundwater changes',
                'dos': [
                    'Drop, Cover, Hold On',
                    'Stay away from windows',
                    'If outdoors, move to open area',
                    'After shaking, check for injuries',
                    'Prepare for aftershocks'
                ],
                'donts': [
                    "Don't run outside during shaking",
                    "Don't stand in doorways",
                    "Don't use elevators",
                    "Don't light matches after (gas leaks)",
                    "Don't spread unverified information"
                ],
                'contacts': [('NDRF', '011-24363260'), ('Emergency', '112'), ('Seismic Centre', '1800-180-1717')]
            },
            'cyclone': {
                'title': 'Cyclone Emergency Guide',
                'icon': '🌀',
                'causes': 'Low pressure systems over warm ocean water, tropical disturbances',
                'warning_signs': 'IMD alerts, dark sky, strong winds, storm surges, rough seas',
                'dos': [
                    'Stock 72-hour emergency supplies',
                    'Board up windows',
                    'Know evacuation routes',
                    'Stay indoors during cyclone',
                    'Listen to official broadcasts'
                ],
                'donts': [
                    "Don't venture out during cyclone",
                    "Don't ignore official warnings",
                    "Don't go out during eye of storm",
                    "Don't stay in flood-prone areas",
                    "Don't touch fallen power lines"
                ],
                'contacts': [('IMD Weather', '1800-180-1717'), ('NDRF', '011-24363260'), ('Emergency', '112')]
            },
            'medical': {
                'title': 'Medical Emergency Guide',
                'icon': '🏥',
                'causes': 'Trauma, cardiac events, respiratory distress, poisoning, disaster injuries',
                'warning_signs': 'Unconsciousness, severe bleeding, difficulty breathing, chest pain',
                'dos': [
                    'Call ambulance: 108 immediately',
                    'Check breathing and pulse',
                    'Start CPR if needed',
                    'Control bleeding with pressure',
                    'Keep patient calm and warm'
                ],
                'donts': [
                    "Don't move patient with spinal injury",
                    "Don't give water to unconscious person",
                    "Don't remove embedded objects",
                    "Don't leave patient alone",
                    "Don't panic"
                ],
                'contacts': [('Ambulance', '108'), ('Emergency', '112'), ('Poison Control', '1800-116-117')]
            },
            'landslide': {
                'title': 'Landslide Emergency Guide',
                'icon': '⛰️',
                'causes': 'Heavy rainfall, earthquakes, deforestation, loose soil',
                'warning_signs': 'Rumbling sounds, ground cracks, tilting trees, muddy water',
                'dos': [
                    'Evacuate immediately when warning issued',
                    'Move away from slope direction',
                    'Alert neighbors and authorities',
                    'Move to higher ground if flooding',
                    'Stay tuned to emergency broadcasts'
                ],
                'donts': [
                    "Don't stay near landslide-prone slopes",
                    "Don't build near unstable hillsides",
                    "Don't cross landslide path",
                    "Don't ignore ground cracks",
                    "Don't wait for visual confirmation"
                ],
                'contacts': [('Geological Survey India', '033-22861626'), ('NDRF', '011-24363260'), ('Emergency', '112')]
            }
        }
        
        return info_map.get(disaster_type.lower(), {})


# Singleton instance
_engine_instance = None


def get_response_engine() -> ResponseEngine:
    """Get or create response engine singleton"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ResponseEngine()
    return _engine_instance
