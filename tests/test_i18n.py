"""
Tests for internationalization (i18n) functionality
"""

import os
import unittest
from unittest.mock import patch

from display_layout_manager.i18n import LocaleDetector, MessageManager


class TestLocaleDetector(unittest.TestCase):
    """Tests for LocaleDetector"""

    def setUp(self):
        """Set up test environment"""
        # Clear any existing DISPLAY_LAYOUT_LANG override
        if "DISPLAY_LAYOUT_LANG" in os.environ:
            del os.environ["DISPLAY_LAYOUT_LANG"]

    def test_detect_japanese_from_lang(self):
        """Test Japanese locale detection from LANG environment variable"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            self.assertEqual(detector.get_locale(), "ja")

    def test_detect_english_from_lang(self):
        """Test English locale detection from LANG environment variable"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            self.assertEqual(detector.get_locale(), "en")

    def test_environment_variable_override_japanese(self):
        """Test DISPLAY_LAYOUT_LANG override to Japanese"""
        with patch.dict(
            os.environ, {"DISPLAY_LAYOUT_LANG": "ja", "LANG": "en_US.UTF-8"}
        ):
            detector = LocaleDetector()
            self.assertEqual(detector.get_locale(), "ja")

    def test_environment_variable_override_english(self):
        """Test DISPLAY_LAYOUT_LANG override to English"""
        with patch.dict(
            os.environ, {"DISPLAY_LAYOUT_LANG": "en", "LANG": "ja_JP.UTF-8"}
        ):
            detector = LocaleDetector()
            self.assertEqual(detector.get_locale(), "en")

    def test_default_to_english(self):
        """Test default to English when locale cannot be determined"""
        with patch.dict(os.environ, {}, clear=True):
            with patch("locale.getdefaultlocale", return_value=(None, None)):
                detector = LocaleDetector()
                self.assertEqual(detector.get_locale(), "en")

    def test_locale_caching(self):
        """Test that locale is cached after first detection"""
        detector = LocaleDetector()
        first_call = detector.get_locale()
        second_call = detector.get_locale()
        self.assertEqual(first_call, second_call)


class TestMessageManager(unittest.TestCase):
    """Tests for MessageManager"""

    def test_get_english_message(self):
        """Test getting English message"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)
            self.assertEqual(
                msg.get("checking_dependencies"), "Checking dependencies..."
            )

    def test_get_japanese_message(self):
        """Test getting Japanese message"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)
            self.assertEqual(msg.get("checking_dependencies"), "依存関係を確認中...")

    def test_message_formatting_english(self):
        """Test message formatting with parameters in English"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)
            result = msg.get("displays_detected", count=3)
            self.assertEqual(result, "Current displays: 3 detected")

    def test_message_formatting_japanese(self):
        """Test message formatting with parameters in Japanese"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)
            result = msg.get("displays_detected", count=3)
            self.assertEqual(result, "現在のディスプレイ: 3個検出")

    def test_fallback_to_english(self):
        """Test fallback to English for missing keys"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)
            # Use a key that doesn't exist
            result = msg.get("nonexistent_key")
            self.assertEqual(result, "nonexistent_key")

    def test_menu_messages_english(self):
        """Test menu bar messages in English"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)
            self.assertEqual(msg.get("menu_apply_layout"), "Apply Layout")
            self.assertEqual(msg.get("menu_save_current"), "Save Current Layout")
            self.assertEqual(msg.get("menu_auto_launch"), "Launch at Login")
            self.assertEqual(msg.get("menu_quit"), "Quit")

    def test_menu_messages_japanese(self):
        """Test menu bar messages in Japanese"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)
            self.assertEqual(msg.get("menu_apply_layout"), "レイアウトを適用")
            self.assertEqual(msg.get("menu_save_current"), "現在の設定を保存")
            self.assertEqual(msg.get("menu_auto_launch"), "ログイン時に起動")
            self.assertEqual(msg.get("menu_quit"), "終了")


if __name__ == "__main__":
    unittest.main()
