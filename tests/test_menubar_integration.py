#!/usr/bin/env python3
"""
メニューバーアプリの統合テスト（実際の UI 動作確認）
"""
import os
import sys
import time
from pathlib import Path

# src ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from display_layout_manager.auto_launch_manager import AutoLaunchManager
from display_layout_manager.menubar_app import DisplayLayoutMenuBar


def test_checkbox_toggle():
    """チェックマーク表示のトグル動作を実際にテスト"""
    print("\n" + "=" * 70)
    print("メニューバーアプリ 統合テスト - チェックマークトグル")
    print("=" * 70)

    # CI 環境チェック（GitHub Actions、その他のCI環境を検出）
    is_ci = (
        os.environ.get("CI") == "true"
        or os.environ.get("GITHUB_ACTIONS") == "true"
        or os.environ.get("CI") is not None
    )

    if is_ci:
        print(
            "\n⚠ CI 環境では GUI テストが実行できないため、このテストをスキップします"
        )
        print("=" * 70)
        return True

    # クリーンアップ（テスト前に無効化）
    print("\n[準備] 自動起動を無効化")
    manager = AutoLaunchManager()
    try:
        manager.disable()
        print("  ✓ 無効化完了")
    except:
        print("  ✓ 既に無効化済み")

    # メニューバーアプリを作成（実際には起動しない）
    print("\n[テスト 1] メニューバーアプリの初期化")
    try:
        # rumps.App の run() を呼ばずにインスタンスだけ作成
        import rumps

        # モックせずに実際のインスタンスを作成
        app = DisplayLayoutMenuBar()
        print("  ✓ アプリインスタンス作成成功")

        # 初期状態確認
        print("\n[テスト 2] 初期状態確認")
        menu_item = app.menu["ログイン時に起動"]
        print(f"  初期 state: {menu_item.state}")
        print(f"  is_enabled: {app.auto_launch_manager.is_enabled()}")

        expected_state = 1 if app.auto_launch_manager.is_enabled() else 0
        if menu_item.state == expected_state:
            print(f"  ✓ 初期状態が正しい (state={menu_item.state})")
        else:
            print(
                f"  ✗ 初期状態が間違っている (expected={expected_state}, actual={menu_item.state})"
            )
            return False

        # トグル 1: 無効 → 有効
        print("\n[テスト 3] トグル 1: 無効 → 有効")
        print(f"  実行前 state: {menu_item.state}")
        print(f"  実行前 is_enabled: {app.auto_launch_manager.is_enabled()}")

        app.toggle_auto_launch(menu_item)

        print(f"  実行後 state: {menu_item.state}")
        print(f"  実行後 is_enabled: {app.auto_launch_manager.is_enabled()}")

        if app.auto_launch_manager.is_enabled() and menu_item.state == 1:
            print("  ✓ 有効化成功 (state=1)")
        else:
            print(
                f"  ✗ 有効化失敗 (is_enabled={app.auto_launch_manager.is_enabled()}, state={menu_item.state})"
            )
            return False

        # トグル 2: 有効 → 無効
        print("\n[テスト 4] トグル 2: 有効 → 無効")
        print(f"  実行前 state: {menu_item.state}")
        print(f"  実行前 is_enabled: {app.auto_launch_manager.is_enabled()}")

        app.toggle_auto_launch(menu_item)

        print(f"  実行後 state: {menu_item.state}")
        print(f"  実行後 is_enabled: {app.auto_launch_manager.is_enabled()}")

        if not app.auto_launch_manager.is_enabled() and menu_item.state == 0:
            print("  ✓ 無効化成功 (state=0)")
        else:
            print(
                f"  ✗ 無効化失敗 (is_enabled={app.auto_launch_manager.is_enabled()}, state={menu_item.state})"
            )
            return False

        # トグル 3: 無効 → 有効（再度）
        print("\n[テスト 5] トグル 3: 無効 → 有効（再度）")
        print(f"  実行前 state: {menu_item.state}")

        app.toggle_auto_launch(menu_item)

        print(f"  実行後 state: {menu_item.state}")

        if app.auto_launch_manager.is_enabled() and menu_item.state == 1:
            print("  ✓ 有効化成功 (state=1)")
        else:
            print(f"  ✗ 有効化失敗 (state={menu_item.state})")
            return False

        # クリーンアップ
        print("\n[クリーンアップ] 自動起動を無効化")
        app.auto_launch_manager.disable()
        print("  ✓ クリーンアップ完了")

        print("\n" + "=" * 70)
        print("✓ すべてのテストが成功しました")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n✗ テスト失敗: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_checkbox_toggle()
    sys.exit(0 if success else 1)
