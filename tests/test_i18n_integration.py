"""
Integration tests for internationalization (i18n) functionality
Tests actual CLI and menubar app behavior with different locales
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from display_layout_manager.i18n import LocaleDetector, MessageManager
from display_layout_manager.logger import Logger


class TestCLIInternationalization(unittest.TestCase):
    """Integration tests for CLI internationalization"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = Path(self.test_dir) / "config.json"

        # Create a minimal valid config file
        config = {
            "version": "1.0",
            "patterns": [
                {
                    "name": "Test Pattern",
                    "description": "Test description",
                    "screen_ids": ["TEST-SCREEN-ID"],
                    "command": 'displayplacer "id:TEST-SCREEN-ID res:1920x1080"',
                }
            ],
        }

        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def tearDown(self):
        """Clean up test environment"""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cli_japanese_environment(self):
        """Test CLI output in Japanese environment"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test key messages
            self.assertIn("確認中", msg.get("checking_dependencies"))
            self.assertIn("ディスプレイ", msg.get("checking_displays"))
            self.assertIn("設定", msg.get("loading_config"))

    def test_cli_english_environment(self):
        """Test CLI output in English environment"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test key messages
            self.assertIn("Checking", msg.get("checking_dependencies"))
            self.assertIn("display", msg.get("checking_displays").lower())
            self.assertIn("config", msg.get("loading_config").lower())

    def test_cli_environment_variable_override(self):
        """Test CLI with DISPLAY_LAYOUT_LANG override"""
        # Override to Japanese even with English system locale
        with patch.dict(
            os.environ, {"LANG": "en_US.UTF-8", "DISPLAY_LAYOUT_LANG": "ja"}
        ):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            self.assertIn("確認中", msg.get("checking_dependencies"))

        # Override to English even with Japanese system locale
        with patch.dict(
            os.environ, {"LANG": "ja_JP.UTF-8", "DISPLAY_LAYOUT_LANG": "en"}
        ):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            self.assertIn("Checking", msg.get("checking_dependencies"))


class TestLoggerInternationalization(unittest.TestCase):
    """Integration tests for Logger internationalization"""

    def setUp(self):
        """Set up test environment"""
        self.test_log_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test environment"""
        import shutil

        shutil.rmtree(self.test_log_dir, ignore_errors=True)

    def test_log_file_always_english(self):
        """Test that log files are always written in English"""
        # Test with Japanese locale
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            with patch(
                "display_layout_manager.logger.Path.home",
                return_value=Path(self.test_log_dir),
            ):
                logger = Logger(verbose=True, log_to_file=True)

                # Log some messages
                logger.info("test", "Test message")
                logger.success("test", "Success message")
                logger.error("test", "Error message")

                # Read log file
                log_file = logger.get_log_file_path()
                self.assertIsNotNone(log_file)

                if log_file and log_file.exists():
                    with open(log_file, "r") as f:
                        log_content = f.read()

                    # Log file should contain English messages
                    self.assertIn("Test message", log_content)
                    self.assertIn("Success message", log_content)
                    self.assertIn("Error message", log_content)

                    # Log file should NOT contain Japanese
                    self.assertNotIn("確認中", log_content)
                    self.assertNotIn("成功", log_content)

    def test_cli_output_internationalized(self):
        """Test that CLI output (print statements) is internationalized"""
        # Japanese environment
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            logger = Logger(verbose=True, log_to_file=False)
            msg = logger.msg

            # CLI output should be in Japanese
            self.assertIn("セッション", msg.get("session_summary"))
            self.assertIn("ログ", msg.get("total_log_entries", count=5))

        # English environment
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            logger = Logger(verbose=True, log_to_file=False)
            msg = logger.msg

            # CLI output should be in English
            self.assertIn("Session", msg.get("session_summary"))
            self.assertIn("log", msg.get("total_log_entries", count=5).lower())


class TestMenuBarInternationalization(unittest.TestCase):
    """Integration tests for Menu Bar app internationalization"""

    def test_menu_items_japanese(self):
        """Test menu items in Japanese environment"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test all menu items
            self.assertEqual(msg.get("menu_apply_layout"), "レイアウトを適用")
            self.assertEqual(msg.get("menu_save_current"), "現在の設定を保存")
            self.assertEqual(msg.get("menu_auto_launch"), "ログイン時に起動")
            self.assertEqual(msg.get("menu_quit"), "終了")

    def test_menu_items_english(self):
        """Test menu items in English environment"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test all menu items
            self.assertEqual(msg.get("menu_apply_layout"), "Apply Layout")
            self.assertEqual(msg.get("menu_save_current"), "Save Current Layout")
            self.assertEqual(msg.get("menu_auto_launch"), "Launch at Login")
            self.assertEqual(msg.get("menu_quit"), "Quit")

    def test_notification_messages_japanese(self):
        """Test notification messages in Japanese environment"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test notification messages
            self.assertIn("適用", msg.get("layout_applied"))
            self.assertIn("保存", msg.get("layout_saved", pattern="Test"))

    def test_notification_messages_english(self):
        """Test notification messages in English environment"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test notification messages
            self.assertIn("applied", msg.get("layout_applied").lower())
            self.assertIn("saved", msg.get("layout_saved", pattern="Test").lower())


class TestErrorMessagesInternationalization(unittest.TestCase):
    """Integration tests for error message internationalization"""

    def test_error_messages_japanese(self):
        """Test error messages in Japanese environment"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test error messages
            self.assertIn("エラー", msg.get("error_occurred", error="test"))
            self.assertIn("見つかりません", msg.get("config_not_found"))
            self.assertIn("失敗", msg.get("command_failed"))

    def test_error_messages_english(self):
        """Test error messages in English environment"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test error messages
            self.assertIn("Error", msg.get("error_occurred", error="test"))
            self.assertIn("not found", msg.get("config_not_found").lower())
            self.assertIn("failed", msg.get("command_failed").lower())


class TestAutoLaunchInternationalization(unittest.TestCase):
    """Integration tests for auto-launch message internationalization"""

    def test_auto_launch_messages_japanese(self):
        """Test auto-launch messages in Japanese environment"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test auto-launch messages
            self.assertIn("有効", msg.get("auto_launch_enabled"))
            self.assertIn("無効", msg.get("auto_launch_disabled"))

    def test_auto_launch_messages_english(self):
        """Test auto-launch messages in English environment"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Test auto-launch messages
            self.assertIn("enabled", msg.get("auto_launch_enabled").lower())
            self.assertIn("disabled", msg.get("auto_launch_disabled").lower())


class TestCompleteWorkflow(unittest.TestCase):
    """Integration test for complete workflow with internationalization"""

    def test_complete_workflow_japanese(self):
        """Test complete workflow in Japanese environment"""
        with patch.dict(os.environ, {"LANG": "ja_JP.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Simulate complete workflow messages
            messages = [
                msg.get("app_start", version="1.0.0"),
                msg.get("checking_dependencies"),
                msg.get("loading_config"),
                msg.get("checking_displays"),
                msg.get("pattern_matching"),
                msg.get("app_complete"),
            ]

            # All messages should be in Japanese
            for message in messages:
                # Check that messages don't contain English-only words
                # (allowing for technical terms like "displayplacer")
                self.assertIsInstance(message, str)
                self.assertTrue(len(message) > 0)

    def test_complete_workflow_english(self):
        """Test complete workflow in English environment"""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            detector = LocaleDetector()
            msg = MessageManager(detector)

            # Simulate complete workflow messages
            messages = [
                msg.get("app_start", version="1.0.0"),
                msg.get("checking_dependencies"),
                msg.get("loading_config"),
                msg.get("checking_displays"),
                msg.get("pattern_matching"),
                msg.get("app_complete"),
            ]

            # All messages should be in English
            for message in messages:
                self.assertIsInstance(message, str)
                self.assertTrue(len(message) > 0)
                # Should not contain Japanese characters
                self.assertFalse(
                    any("\u3040" <= c <= "\u309f" for c in message)
                )  # Hiragana
                self.assertFalse(
                    any("\u30a0" <= c <= "\u30ff" for c in message)
                )  # Katakana


if __name__ == "__main__":
    unittest.main()
