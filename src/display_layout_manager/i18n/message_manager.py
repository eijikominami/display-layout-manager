"""
Message Manager

Manages message retrieval and formatting based on detected locale.
"""

from typing import Any

from .locale_detector import LocaleDetector
from .message_catalog import MESSAGES


class MessageManager:
    """Message manager for internationalized messages"""

    def __init__(self, locale_detector: LocaleDetector = None):
        self.locale_detector = locale_detector or LocaleDetector()
        self.messages = MESSAGES

    def get(self, key: str, **kwargs: Any) -> str:
        """
        Get message for the current locale

        Args:
            key: Message key
            **kwargs: Format parameters

        Returns:
            str: Localized message
        """
        locale = self.locale_detector.get_locale()

        # Get message for current locale
        message = self.messages.get(locale, {}).get(key)

        # Fallback to English
        if message is None:
            message = self.messages.get("en", {}).get(key, key)

        # Format message
        if kwargs:
            try:
                return message.format(**kwargs)
            except (KeyError, ValueError):
                return message

        return message
