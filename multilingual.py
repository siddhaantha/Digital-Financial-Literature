"""
multilingual.py
Language detection and translation layer using deep-translator (Google Translate API).
Supports 12 Indian languages + English for the Digital Financial Literacy Agent.
"""

import logging
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Unicode block → ISO 639-1 code for scripts that langdetect misses on short
# mixed-script text (e.g. "UPI ಎಂದರೇನು?" where "UPI" is ASCII).
_SCRIPT_RANGES: list[tuple[int, int, str]] = [
    (0x0900, 0x097F, "hi"),   # Devanagari  (Hindi / Marathi)
    (0x0980, 0x09FF, "bn"),   # Bengali
    (0x0A00, 0x0A7F, "pa"),   # Gurmukhi    (Punjabi)
    (0x0A80, 0x0AFF, "gu"),   # Gujarati
    (0x0B00, 0x0B7F, "or"),   # Odia
    (0x0B80, 0x0BFF, "ta"),   # Tamil
    (0x0C00, 0x0C7F, "te"),   # Telugu
    (0x0C80, 0x0CFF, "kn"),   # Kannada
    (0x0D00, 0x0D7F, "ml"),   # Malayalam
    (0x0600, 0x06FF, "ur"),   # Arabic / Urdu
]


def _detect_script(text: str) -> str | None:
    """
    Return the ISO code of the first Indic/Arabic script block found in text,
    or None if the text contains only ASCII/Latin characters.
    """
    for ch in text:
        cp = ord(ch)
        for lo, hi, code in _SCRIPT_RANGES:
            if lo <= cp <= hi:
                return code
    return None

# Supported languages with ISO codes and display names
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "bn": "Bengali (বাংলা)",
    "mr": "Marathi (मराठी)",
    "gu": "Gujarati (ગુજરાતી)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "ml": "Malayalam (മലയാളം)",
    "or": "Odia (ଓଡ଼ିଆ)",
    "ur": "Urdu (اردو)",
}

# Map langdetect codes to Google Translate codes where they differ
LANGDETECT_TO_GOOGLE = {
    "zh-cn": "zh-CN",
    "zh-tw": "zh-TW",
}


def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    Returns ISO 639-1 language code string (e.g. 'en', 'hi', 'ta').
    Uses a Unicode-script check first so mixed-script queries like
    "UPI ಎಂದರೇನು?" are correctly identified before langdetect runs.
    Falls back to 'en' on detection failure.
    """
    if not text or len(text.strip()) < 3:
        return "en"
    # Fast path: any Indic/Arabic codepoint identifies the script unambiguously
    script = _detect_script(text)
    if script:
        return script
    try:
        detected = detect(text.strip())
        return LANGDETECT_TO_GOOGLE.get(detected, detected)
    except Exception:
        return "en"


def translate_to_english(text: str, source_lang: str = "auto") -> str:
    """
    Translate any text to English for RAG processing.
    Returns the original text if source is already English or translation fails.
    """
    if source_lang == "en":
        return text
    try:
        translator = GoogleTranslator(source=source_lang, target="en")
        result = translator.translate(text.strip())
        return result if result else text
    except Exception as exc:
        logger.warning("translate_to_english failed (lang=%s): %s", source_lang, exc)
        return text  # Graceful degradation — use original text


def translate_from_english(text: str, target_lang: str) -> str:
    """
    Translate an English response into the target language.
    Returns the original English text if target is 'en' or translation fails.
    """
    if target_lang == "en" or target_lang not in SUPPORTED_LANGUAGES:
        return text
    try:
        translator = GoogleTranslator(source="en", target=target_lang)
        # Split on double-newlines to preserve paragraph structure
        paragraphs = text.split("\n\n")
        translated_paragraphs = []
        for para in paragraphs:
            if para.strip():
                translated = translator.translate(para.strip())
                translated_paragraphs.append(translated if translated else para)
            else:
                translated_paragraphs.append("")
        return "\n\n".join(translated_paragraphs)
    except Exception as exc:
        logger.warning("translate_from_english failed (lang=%s): %s", target_lang, exc)
        return text  # Graceful degradation


def get_language_greeting(lang: str) -> str:
    """Return a greeting in the detected language."""
    greetings = {
        "en": "Hello! I'm your Digital Financial Literacy Assistant.",
        "hi": "नमस्ते! मैं आपका डिजिटल वित्तीय साक्षरता सहायक हूँ।",
        "ta": "வணக்கம்! நான் உங்கள் டிஜிட்டல் நிதி கல்வி உதவியாளர்.",
        "te": "నమస్కారం! నేను మీ డిజిటల్ ఆర్థిక అక్షరాస్యత సహాయకుడిని.",
        "bn": "নমস্কার! আমি আপনার ডিজিটাল আর্থিক সাক্ষরতা সহকারী।",
        "mr": "नमस्कार! मी तुमचा डिजिटल आर्थिक साक्षरता सहायक आहे।",
        "gu": "નમસ્તે! હું તમારો ડિજિટલ નાણાકીય સાક્ષરતા સહાયક છું।",
        "kn": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಡಿಜಿಟಲ್ ಹಣಕಾಸು ಸಾಕ್ಷರತೆ ಸಹಾಯಕ.",
        "pa": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਡਿਜੀਟਲ ਵਿੱਤੀ ਸਾਖਰਤਾ ਸਹਾਇਕ ਹਾਂ।",
        "ml": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ ഡിജിറ്റൽ സാമ്പത്തിക സാക്ഷരതാ സഹായി.",
        "or": "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କ ଡିଜିଟାଲ ଆର୍ଥିକ ସାକ୍ଷରତା ସହାୟକ।",
        "ur": "السلام علیکم! میں آپ کا ڈیجیٹل مالی خواندگی معاون ہوں۔",
    }
    return greetings.get(lang, greetings["en"])
