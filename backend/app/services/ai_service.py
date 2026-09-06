from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import re, json, logging

logger = logging.getLogger(__name__)

INTENT_PATTERNS = {
    "greeting": r"\b(hi|hello|hey|good morning|good evening|howdy)\b",
    "pricing": r"\b(price|cost|rate|budget|mortgage|afford|cheap|expensive|how much|payment|down payment)\b",
    "availability": r"\b(available|unit|home|house|ready|stock|vacant|left|remaining|open house)\b",
    "configuration": r"\b(bed|bath|bedroom|bathroom|sqft|square|garage|basement|layout|floor plan|condo|townhouse|detached)\b",
    "timeline": r"\b(when|complete|ready|move.?in|closing|timeline|delivery|date|month|year|possession)\b",
    "amenities": r"\b(amenity|amenities|facility|gym|pool|club|parking|garden|security|ev|smart|school|park)\b",
    "visit": r"\b(visit|see|tour|inspect|viewing|walk|open house|show|appointment|book|schedule|come by)\b",
    "location": r"\b(location|where|address|map|direction|near|neighborhood|commute|transit|drive)\b",
    "offers": r"\b(offer|discount|deal|incentive|promotion|free|closing cost|credit)\b",
    "mortgage": r"\b(mortgage|loan|finance|bank|pre.?approv|interest rate|monthly payment|fha|conventional)\b",
    "comparison": r"\b(compare|vs|versus|difference|better|which)\b",
    "legal": r"\b(legal|title|deed|inspection|disclosure|hoa|tax|closing|escrow|attorney)\b",
    "negotiation": r"\b(negotiat|offer|counter|under asking|reduce|lower|deal)\b",
}

def detect_intent(msg: str) -> str:
    m = msg.lower()
    for intent, pat in INTENT_PATTERNS.items():
        if re.search(pat, m, re.IGNORECASE): return intent
    return "general"

class AIServiceInterface(ABC):
    @abstractmethod
    async def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]: ...

class DummyAIService(AIServiceInterface):
    async def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        intent = detect_intent(message)
        escalated = intent in ("legal", "negotiation")
        return {"reply": self._reply(intent), "intent": intent, "suggested_actions": self._actions(intent), "escalated": escalated, "confidence": 0.92}

    def _reply(self, intent):
        R = {
            "greeting": "Hello! 👋 Welcome to HomeConnect AI. I'm your personal real estate assistant, available 24/7.\n\nWe have beautiful homes across North America:\n\n🏠 Maple Ridge Estates — Toronto, ON (Townhomes from $589K)\n🌅 Sunset Valley Homes — Austin, TX (Single-family from $425K)\n🏔️ Pacific Crest Residences — Vancouver, BC (Condos from $649K)\n\nWhat are you looking for?",
            "pricing": "Here's our current pricing:\n\n🏠 Maple Ridge Estates (Toronto, ON):\n• 3-Bed Townhome: $589K – $729K\n• 4-Bed Detached: $849K – $1.1M\n• Executive Home: $1.2M – $1.6M\n\n🌅 Sunset Valley (Austin, TX):\n• 3-Bed Ranch: $425K – $549K\n• 4-Bed Colonial: $575K – $725K\n• Custom Build: $750K – $1.2M\n\n🏔️ Pacific Crest (Vancouver, BC):\n• 1-Bed Condo: $649K – $789K\n• 2-Bed Condo: $849K – $1.1M\n• Penthouse: $1.8M – $2.5M\n\nWant me to calculate monthly mortgage payments?",
            "availability": "Current availability:\n\n🏠 Maple Ridge Estates (Toronto):\n→ 8 townhomes, 4 detached homes available\n→ South-facing units going fast — only 3 left!\n\n🌅 Sunset Valley (Austin):\n→ 12 homes available across Phase 2\n→ Premium lots with hill country views\n\n🏔️ Pacific Crest (Vancouver):\n→ Floors 8, 12, 15, 18, 22 available\n→ Corner units with mountain views — last 2!\n\nWant to schedule a tour?",
            "configuration": "Our home configurations:\n\n🏠 Maple Ridge Townhomes:\n• 3 Bed / 2.5 Bath — 1,800 sqft, 2-car garage\n• 4 Bed / 3 Bath — 2,400 sqft, finished basement\n\n🌅 Sunset Valley Homes:\n• Ranch: 3 Bed / 2 Bath — 2,100 sqft, open floor plan\n• Colonial: 4 Bed / 3.5 Bath — 3,200 sqft, bonus room\n• Custom: 4-5 Bed — 3,500–4,800 sqft, your design\n\n🏔️ Pacific Crest Condos:\n• 1 Bed — 650 sqft, floor-to-ceiling windows\n• 2 Bed — 980 sqft, in-suite laundry\n• Penthouse — 2,100 sqft, private terrace\n\nAll homes: smart home ready, energy efficient, premium finishes.",
            "timeline": "Move-in timelines:\n\n✅ Sunset Valley Phase 1 — Ready Now!\n🔨 Maple Ridge — Spring 2026 (framing complete)\n🔨 Pacific Crest — Fall 2026 (structure up to 15th floor)\n\nClosing typically takes 30-45 days after agreement. Want to start the process?",
            "amenities": "Community amenities:\n\n🏠 Maple Ridge: Community center, playground, walking trails, dog park, tennis courts, 24/7 concierge\n\n🌅 Sunset Valley: Pool & spa, fitness center, hiking trails, BBQ pavilion, sports courts, nature preserve\n\n🏔️ Pacific Crest: Rooftop pool, sky lounge, yoga studio, co-working space, EV charging, bike storage, concierge\n\nNearby: Top-rated schools, hospitals, shopping, transit, and major highways.",
            "visit": "I'd love to arrange a tour for you! 🏠\n\nVisiting hours:\n📅 Mon–Fri: 9 AM – 6 PM\n📅 Saturday: 10 AM – 5 PM\n📅 Sunday: 12 PM – 4 PM\n\nI'll automatically find a time that works — no double-bookings!\n\nPlease share your preferred date, time, and which community you'd like to visit.",
            "location": "Our communities:\n\n📍 Maple Ridge Estates — North Toronto, ON\n→ 15 min to downtown, near Highway 401\n→ Top schools: Bayview Glen, TMS\n→ Walk to shops, restaurants, parks\n\n📍 Sunset Valley Homes — Southwest Austin, TX\n→ 20 min to downtown, near MoPac\n→ Excellent AISD schools\n→ Hill country views, Barton Creek nearby\n\n📍 Pacific Crest — Downtown Vancouver, BC\n→ Steps to SkyTrain, seawall, Stanley Park\n→ Walk score: 96/100\n→ Premium dining, shopping district\n\nWant directions or a tour?",
            "offers": "🎉 Current Incentives:\n\n🏠 Maple Ridge:\n• $15,000 closing cost credit\n• Free smart home package ($8K value)\n\n🌅 Sunset Valley:\n• $10,000 design center credit\n• Rate buy-down: 5.99% for first 2 years\n\n🏔️ Pacific Crest:\n• Free parking stall ($75K value)\n• 1 year of HOA fees covered\n\nLimited time — schedule a tour to lock in these offers!",
            "mortgage": "💰 Mortgage Estimates (30yr fixed, ~6.5%):\n\n• $425K home → ~$2,685/mo\n• $589K home → ~$3,725/mo\n• $849K home → ~$5,370/mo\n\n✅ Pre-approval partners: Wells Fargo, Chase, TD Bank, RBC, BMO\n✅ FHA, Conventional, VA, and CMHC-insured options\n✅ Down payment as low as 3.5% (US) or 5% (Canada)\n\nWant me to connect you with our preferred lender?",
            "comparison": "Quick comparison:\n\n| Feature | Maple Ridge (Toronto) | Sunset Valley (Austin) | Pacific Crest (Vancouver) |\n|---------|----------------------|----------------------|-------------------------|\n| Type | Townhomes/Detached | Single-Family | Condos |\n| From | $589K USD | $425K USD | $649K USD |\n| Ready | Spring 2026 | Now! | Fall 2026 |\n| Best For | Families | First-time buyers | Urban professionals |\n\nWhich fits your lifestyle best?",
            "legal": "For legal, title, and closing questions, let me connect you with our team:\n\n• Title search & insurance\n• Home inspection coordination\n• HOA rules & disclosures\n• Closing process walkthrough\n• Tax implications\n\nOur team will respond within 30 minutes with detailed guidance.",
            "negotiation": "I appreciate your interest! 🙏\n\nFor pricing discussions, let me connect you with our Sales Director who can:\n• Review comparable sales\n• Discuss closing cost credits\n• Arrange flexible closing timelines\n• Custom upgrade packages\n\nYou'll hear back within 15 minutes.",
            "general": "Welcome to HomeConnect AI! 🏠\n\nI can help you find your perfect home across our 3 premium communities:\n\n📍 Maple Ridge Estates — Toronto, ON (from $589K)\n📍 Sunset Valley Homes — Austin, TX (from $425K)\n📍 Pacific Crest Residences — Vancouver, BC (from $649K)\n\nI can help with pricing, availability, tours, mortgage estimates, and more. What interests you?",
        }
        return R.get(intent, R["general"])

    def _actions(self, intent):
        M = {
            "greeting": ["View Pricing", "Check Availability", "Schedule Tour", "Compare Communities"],
            "pricing": ["Mortgage Calculator", "Schedule Tour", "Current Offers"],
            "availability": ["Floor Plans", "Schedule Tour", "View Photos"],
            "configuration": ["Floor Plans", "Schedule Tour", "3D Virtual Tour"],
            "timeline": ["Schedule Tour", "View Offers"],
            "amenities": ["Schedule Tour", "Photo Gallery"],
            "visit": ["Pick Date & Time", "Get Directions"],
            "location": ["Get Directions", "Schedule Tour"],
            "offers": ["Schedule Tour", "Apply for Mortgage"],
            "mortgage": ["Get Pre-Approved", "Schedule Tour"],
            "comparison": ["Schedule Tour", "Detailed Pricing"],
            "legal": ["Transferred to Team"],
            "negotiation": ["Transferred to Sales Director"],
            "general": ["View Pricing", "Availability", "Schedule Tour"],
        }
        return M.get(intent, M["general"])

class AzureOpenAIService(AIServiceInterface):
    def __init__(self):
        from app.config import get_settings
        s = get_settings()
        from openai import AzureOpenAI
        self.client = AzureOpenAI(azure_endpoint=s.azure_openai_endpoint, api_key=s.azure_openai_key, api_version=s.azure_openai_api_version)
        self.deployment = s.azure_openai_deployment

    async def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            r = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": "You are HomeConnect AI, a real estate assistant for premium communities in Toronto, Austin, and Vancouver. Be helpful, professional, and warm. Return JSON: {reply, intent, suggested_actions[], escalated, confidence}."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7, max_tokens=800, response_format={"type": "json_object"},
            )
            return json.loads(r.choices[0].message.content)
        except Exception as e:
            logger.error(f"Azure OpenAI error: {e}")
            return await DummyAIService().generate_response(message, context)

def get_ai_service() -> AIServiceInterface:
    from app.config import get_settings
    s = get_settings()
    if s.ai_provider == "azure" and s.azure_openai_endpoint: return AzureOpenAIService()
    return DummyAIService()
