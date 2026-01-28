from .ru import MESSAGES as RU_MESSAGES
from .en import MESSAGES as EN_MESSAGES

MESSAGES = {
    'ru': RU_MESSAGES,
    'en': EN_MESSAGES
}

DEFAULT_LANGUAGE = 'ru'

def get_message(lang: str, key: str, **kwargs):
    """Get a localized message with variable substitution"""
    if lang not in MESSAGES:
        lang = DEFAULT_LANGUAGE
    
    template = MESSAGES[lang].get(key, MESSAGES[DEFAULT_LANGUAGE].get(key, key))
    
    if kwargs:
        return template.format(**kwargs)
    return template

def t(lang: str, key: str, **kwargs):
    """Shorthand for get_message"""
    return get_message(lang, key, **kwargs)
