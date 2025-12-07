#!/usr/bin/env python3
"""
Display Layout Manager - Menu Bar Application Entry Point

macOS メニューバーアプリケーションのエントリーポイント
"""

import argparse
import sys

from display_layout_manager.auto_launch_manager import AutoLaunchManager
from display_layout_manager.i18n import LocaleDetector, MessageManager
from display_layout_manager.menubar_app import DisplayLayoutMenuBar


def main():
    """メニューバーアプリケーションのメインエントリーポイント"""
    # Initialize i18n
    locale_detector = LocaleDetector()
    msg = MessageManager(locale_detector)
    
    parser = argparse.ArgumentParser(
        description="Display Layout Manager - Menu Bar Application"
    )
    parser.add_argument(
        "--enable-auto-launch", action="store_true", help="Enable auto-launch at login"
    )
    parser.add_argument(
        "--disable-auto-launch",
        action="store_true",
        help="Disable auto-launch at login",
    )

    args = parser.parse_args()

    # 自動起動の有効化・無効化
    if args.enable_auto_launch:
        auto_launch = AutoLaunchManager()
        auto_launch.enable()
        print(f"✓ {msg.get('auto_launch_enabled')}")
        return 0

    if args.disable_auto_launch:
        auto_launch = AutoLaunchManager()
        auto_launch.disable()
        print(f"✓ {msg.get('auto_launch_disabled')}")
        return 0

    # メニューバーアプリケーションを起動
    try:
        app = DisplayLayoutMenuBar()
        app.run()
        return 0
    except KeyboardInterrupt:
        print(f"\n{msg.get('menubar_app_quit')}")
        return 0
    except Exception as e:
        print(f"{msg.get('app_error', error=e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
