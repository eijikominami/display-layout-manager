"""
Internationalization (i18n) module for Display Layout Manager

Provides locale detection and message management for Japanese and English.
"""

from .locale_detector import LocaleDetector
from .message_catalog import MESSAGES
from .message_manager import MessageManager

__all__ = ["LocaleDetector", "MESSAGES", "MessageManager"]
