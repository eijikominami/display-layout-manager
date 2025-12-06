#!/usr/bin/env python3
"""
Display Layout Manager - Menu Bar Application Entry Point

macOS メニューバーアプリケーションのエントリーポイント
"""

import argparse
import sys

from display_layout_manager.auto_launch_manager import AutoLaunchManager
from display_layout_manager.menubar_app import DisplayLayoutMenuBar


def main():
    """メニューバーアプリケーションのメインエントリーポイント"""
    parser = argparse.ArgumentParser(
        description="Display Layout Manager - Menu Bar Application"
    )
    parser.add_argument(
        "--enable-auto-launch", action="store_true", help="ログイン時の自動起動を有効化"
    )
    parser.add_argument(
        "--disable-auto-launch",
        action="store_true",
        help="ログイン時の自動起動を無効化",
    )

    args = parser.parse_args()

    # 自動起動の有効化・無効化
    if args.enable_auto_launch:
        auto_launch = AutoLaunchManager()
        auto_launch.enable()
        print("✓ ログイン時の自動起動を有効化しました")
        return 0

    if args.disable_auto_launch:
        auto_launch = AutoLaunchManager()
        auto_launch.disable()
        print("✓ ログイン時の自動起動を無効化しました")
        return 0

    # メニューバーアプリケーションを起動
    try:
        app = DisplayLayoutMenuBar()
        app.run()
        return 0
    except KeyboardInterrupt:
        print("\nメニューバーアプリケーションを終了します")
        return 0
    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
