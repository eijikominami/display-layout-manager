#!/usr/bin/env python3
"""
メニューバーアプリの包括的な単体テスト
"""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# src ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from display_layout_manager.auto_launch_manager import AutoLaunchManager
from display_layout_manager.menubar_app import DisplayLayoutMenuBar


def test_menubar_initialization():
    """メニューバーアプリの初期化テスト"""
    print("\n" + "=" * 60)
    print("テスト 1: メニューバーアプリの初期化")
    print("=" * 60)

    with patch(
        "display_layout_manager.menubar_app.rumps.App.__init__"
    ) as mock_init, patch(
        "display_layout_manager.menubar_app.rumps.App.menu",
        new_callable=lambda: property(
            lambda self: self._menu_dict, lambda self, v: setattr(self, "_menu_dict", v)
        ),
    ):
        mock_init.return_value = None

        try:
            app = DisplayLayoutMenuBar()
            app._menu_dict = {}  # メニュー辞書を初期化
            print("  ✓ DisplayLayoutMenuBar インスタンス作成成功")

            # コンポーネントが初期化されているか確認
            assert hasattr(app, "cli_bridge"), "cli_bridge が存在すべき"
            print("  ✓ cli_bridge 初期化確認")

            assert hasattr(
                app, "auto_launch_manager"
            ), "auto_launch_manager が存在すべき"
            print("  ✓ auto_launch_manager 初期化確認")

            return True
        except Exception as e:
            print(f"  ✗ 初期化失敗: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_menu_structure():
    """メニュー構造のテスト"""
    print("\n" + "=" * 60)
    print("テスト 2: メニュー構造")
    print("=" * 60)

    with patch("display_layout_manager.menubar_app.rumps.App.__init__") as mock_init:
        mock_init.return_value = None

        try:
            app = DisplayLayoutMenuBar()
            menu_items = app._build_menu()

            print(f"  メニュー項目数: {len(menu_items)}")

            # メニュー項目の確認
            expected_items = [
                "レイアウトを適用",
                "現在の設定を保存",
                "ログイン時に起動",
                "終了",
            ]

            actual_items = [
                item.title if hasattr(item, "title") else None
                for item in menu_items
                if hasattr(item, "title")
            ]
            print(f"  実際のメニュー項目: {actual_items}")

            for expected in expected_items:
                assert expected in actual_items, f"'{expected}' がメニューに存在すべき"
                print(f"  ✓ '{expected}' 存在確認")

            # セパレーターの確認
            separators = [item for item in menu_items if not hasattr(item, "title")]
            print(f"  セパレーター数: {len(separators)}")
            assert len(separators) == 2, "セパレーターは2つであるべき"
            print("  ✓ セパレーター数確認")

            return True
        except Exception as e:
            print(f"  ✗ メニュー構造テスト失敗: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_auto_launch_state_update():
    """自動起動状態更新のテスト"""
    print("\n" + "=" * 60)
    print("テスト 3: 自動起動状態更新")
    print("=" * 60)

    with patch("display_layout_manager.menubar_app.rumps.App.__init__") as mock_init:
        mock_init.return_value = None

        try:
            app = DisplayLayoutMenuBar()

            # モックメニュー項目を作成
            mock_menu_item = Mock()
            mock_menu_item.state = 0

            # メニューをモック
            app.menu = {"ログイン時に起動": mock_menu_item}

            # 自動起動マネージャーをモック
            app.auto_launch_manager = Mock()

            # テスト 1: 有効状態
            print("\n  [3-1] 有効状態のテスト")
            app.auto_launch_manager.is_enabled.return_value = True
            app._update_auto_launch_state()
            assert mock_menu_item.state == 1, "有効時は state = 1 であるべき"
            print("    ✓ 有効時の state = 1 確認")

            # テスト 2: 無効状態
            print("\n  [3-2] 無効状態のテスト")
            app.auto_launch_manager.is_enabled.return_value = False
            app._update_auto_launch_state()
            assert mock_menu_item.state == 0, "無効時は state = 0 であるべき"
            print("    ✓ 無効時の state = 0 確認")

            return True
        except Exception as e:
            print(f"  ✗ 自動起動状態更新テスト失敗: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_toggle_auto_launch():
    """自動起動トグルのテスト"""
    print("\n" + "=" * 60)
    print("テスト 4: 自動起動トグル")
    print("=" * 60)

    with patch("display_layout_manager.menubar_app.rumps.App.__init__") as mock_init:
        mock_init.return_value = None

        try:
            app = DisplayLayoutMenuBar()

            # モックメニュー項目を作成
            mock_menu_item = Mock()
            mock_menu_item.state = 0

            # メニューをモック
            app.menu = {"ログイン時に起動": mock_menu_item}

            # 自動起動マネージャーをモック
            app.auto_launch_manager = Mock()

            # テスト 1: 無効 → 有効
            print("\n  [4-1] 無効 → 有効のテスト")
            app.auto_launch_manager.is_enabled.return_value = False
            app.toggle_auto_launch(mock_menu_item)
            app.auto_launch_manager.enable.assert_called_once()
            print("    ✓ enable() が呼ばれた")

            # テスト 2: 有効 → 無効
            print("\n  [4-2] 有効 → 無効のテスト")
            app.auto_launch_manager.reset_mock()
            app.auto_launch_manager.is_enabled.return_value = True
            app.toggle_auto_launch(mock_menu_item)
            app.auto_launch_manager.disable.assert_called_once()
            print("    ✓ disable() が呼ばれた")

            return True
        except Exception as e:
            print(f"  ✗ 自動起動トグルテスト失敗: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_apply_layout():
    """レイアウト適用のテスト"""
    print("\n" + "=" * 60)
    print("テスト 5: レイアウト適用")
    print("=" * 60)

    with patch("display_layout_manager.menubar_app.rumps.App.__init__") as mock_init:
        mock_init.return_value = None

        try:
            app = DisplayLayoutMenuBar()

            # CLI ブリッジをモック
            app.cli_bridge = Mock()

            # レイアウト適用を実行
            app.apply_layout(None)

            # execute_apply_layout が呼ばれたか確認
            app.cli_bridge.execute_apply_layout.assert_called_once()
            print("  ✓ execute_apply_layout() が呼ばれた")

            return True
        except Exception as e:
            print(f"  ✗ レイアウト適用テスト失敗: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_save_current():
    """現在の設定保存のテスト"""
    print("\n" + "=" * 60)
    print("テスト 6: 現在の設定保存")
    print("=" * 60)

    with patch("display_layout_manager.menubar_app.rumps.App.__init__") as mock_init:
        mock_init.return_value = None

        try:
            app = DisplayLayoutMenuBar()

            # CLI ブリッジをモック
            app.cli_bridge = Mock()

            # 設定保存を実行
            app.save_current(None)

            # execute_save_current が呼ばれたか確認
            app.cli_bridge.execute_save_current.assert_called_once()
            print("  ✓ execute_save_current() が呼ばれた")

            return True
        except Exception as e:
            print(f"  ✗ 現在の設定保存テスト失敗: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_error_handling():
    """エラーハンドリングのテスト"""
    print("\n" + "=" * 60)
    print("テスト 7: エラーハンドリング")
    print("=" * 60)

    with patch("display_layout_manager.menubar_app.rumps.App.__init__") as mock_init:
        mock_init.return_value = None

        try:
            app = DisplayLayoutMenuBar()

            # CLI ブリッジをモック（エラーを発生させる）
            app.cli_bridge = Mock()
            app.cli_bridge.execute_apply_layout.side_effect = Exception("テストエラー")

            # エラーが発生してもクラッシュしないことを確認
            try:
                app.apply_layout(None)
                print("  ✓ エラー時もクラッシュしない（サイレント実行）")
            except Exception as e:
                print(f"  ✗ エラーハンドリング失敗: {e}")
                return False

            return True
        except Exception as e:
            print(f"  ✗ エラーハンドリングテスト失敗: {e}")
            import traceback

            traceback.print_exc()
            return False


def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 70)
    print("メニューバーアプリ 包括的単体テスト")
    print("=" * 70)

    tests = [
        ("初期化", test_menubar_initialization),
        ("メニュー構造", test_menu_structure),
        ("自動起動状態更新", test_auto_launch_state_update),
        ("自動起動トグル", test_toggle_auto_launch),
        ("レイアウト適用", test_apply_layout),
        ("現在の設定保存", test_save_current),
        ("エラーハンドリング", test_error_handling),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ テスト '{name}' で予期しないエラー: {e}")
            import traceback

            traceback.print_exc()
            results.append((name, False))

    # 結果サマリー
    print("\n" + "=" * 70)
    print("テスト結果サマリー")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")

    print(f"\n合計: {passed}/{total} テスト成功")
    print("=" * 70)

    return all(result for _, result in results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
