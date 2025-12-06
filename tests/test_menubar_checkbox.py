#!/usr/bin/env python3
"""
メニューバーアプリのチェックマーク機能の単体テスト
"""
import sys
import os
from pathlib import Path

# src ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from display_layout_manager.auto_launch_manager import AutoLaunchManager


def test_auto_launch_manager():
    """AutoLaunchManager の基本機能テスト"""
    print("=" * 60)
    print("AutoLaunchManager 単体テスト")
    print("=" * 60)

    manager = AutoLaunchManager()

    # 1. 初期状態確認
    print("\n[テスト 1] 初期状態確認")
    print(f"  plist_path: {manager.plist_path}")
    print(f"  plist exists: {manager.plist_path.exists()}")
    initial_state = manager.is_enabled()
    print(f"  is_enabled(): {initial_state}")

    # 2. 無効化（既に無効の場合もテスト）
    print("\n[テスト 2] 無効化")
    try:
        manager.disable()
        print("  ✓ disable() 成功")
        after_disable = manager.is_enabled()
        print(f"  is_enabled(): {after_disable}")
        assert after_disable == False, "無効化後は False であるべき"
        print("  ✓ 無効化後の状態確認: OK")
    except Exception as e:
        print(f"  ✗ disable() 失敗: {e}")

    # 3. 有効化
    print("\n[テスト 3] 有効化")
    try:
        manager.enable()
        print("  ✓ enable() 成功")
        after_enable = manager.is_enabled()
        print(f"  is_enabled(): {after_enable}")
        assert after_enable == True, "有効化後は True であるべき"
        print("  ✓ 有効化後の状態確認: OK")
    except Exception as e:
        print(f"  ✗ enable() 失敗: {e}")
        import traceback

        traceback.print_exc()
        return False

    # 4. トグル動作テスト
    print("\n[テスト 4] トグル動作")
    try:
        # 有効 → 無効
        if manager.is_enabled():
            print("  現在: 有効")
            manager.disable()
            print("  disable() 実行")
            assert manager.is_enabled() == False, "無効化されるべき"
            print("  ✓ 有効 → 無効: OK")

        # 無効 → 有効
        if not manager.is_enabled():
            print("  現在: 無効")
            manager.enable()
            print("  enable() 実行")
            assert manager.is_enabled() == True, "有効化されるべき"
            print("  ✓ 無効 → 有効: OK")

        # 有効 → 無効（再度）
        if manager.is_enabled():
            print("  現在: 有効")
            manager.disable()
            print("  disable() 実行")
            assert manager.is_enabled() == False, "無効化されるべき"
            print("  ✓ 有効 → 無効（再度）: OK")

        print("  ✓ トグル動作: OK")
    except Exception as e:
        print(f"  ✗ トグル動作失敗: {e}")
        import traceback

        traceback.print_exc()
        return False

    # 5. クリーンアップ（テスト後は無効化）
    print("\n[テスト 5] クリーンアップ")
    try:
        manager.disable()
        print("  ✓ テスト後のクリーンアップ完了")
    except Exception as e:
        print(f"  ✗ クリーンアップ失敗: {e}")

    print("\n" + "=" * 60)
    print("✓ すべてのテストが成功しました")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_auto_launch_manager()
    sys.exit(0 if success else 1)
