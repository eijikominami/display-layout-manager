"""
Locale Detector

Detects system locale and determines the appropriate language for messages.
"""

import locale
import os


class LocaleDetector:
    """System locale detector"""

    def __init__(self):
        self._detected_locale = None

    def detect_locale(self) -> str:
        """
        Detect system locale

        Returns:
            str: 'ja' for Japanese, 'en' for English
        """
        # Environment variable override (highest priority for testing)
        override = os.environ.get("DISPLAY_LAYOUT_LANG")
        if override:
            return "ja" if override.startswith("ja") else "en"

        # Check LANG environment variable (for testing and CLI usage)
        lang = os.environ.get("LANG", "")
        if lang.startswith("ja"):
            return "ja"
        elif lang.startswith("en"):
            return "en"

        # macOS: Use NSLocale to get preferred languages (for GUI apps)
        try:
            from Foundation import NSLocale

            # Get the list of preferred languages
            preferred_languages = NSLocale.preferredLanguages()
            if preferred_languages and len(preferred_languages) > 0:
                # Check the first preferred language
                first_lang = preferred_languages[0]
                if first_lang.startswith("ja"):
                    return "ja"
        except Exception:
            pass

        # Use locale module as fallback
        try:
            current_locale, _ = locale.getdefaultlocale()
            if current_locale and current_locale.startswith("ja"):
                return "ja"
        except Exception:
            pass

        # Default to English
        return "en"

    def get_locale(self) -> str:
        """Get cached locale"""
        if self._detected_locale is None:
            self._detected_locale = self.detect_locale()
        return self._detected_locale
