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
from display_layout_manager.single_instance_manager import SingleInstanceManager


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

    # 単一インスタンス管理
    instance_manager = SingleInstanceManager()

    # 既に起動しているかチェック
    if instance_manager.is_already_running():
        print("Display Layout Manager is already running.")
        # 既存のインスタンスを前面に表示
        instance_manager.bring_existing_to_front()
        return 0

    # ロックを取得
    if not instance_manager.acquire_lock():
        print("Failed to acquire lock.", file=sys.stderr)
        return 1

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
    finally:
        # 終了時にロックを解放
        instance_manager.release_lock()


if __name__ == "__main__":
    sys.exit(main())
