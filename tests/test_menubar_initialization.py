#!/usr/bin/env python3
"""
メニューバーアプリの初期化統合テスト

rumps の実際の初期化をテストして、title パラメータが正しく設定されているか確認
"""
import sys
from pathlib import Path

# src ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from display_layout_manager.menubar_app import DisplayLayoutMenuBar  # noqa: E402


def test_menubar_title_initialization():
    """
    メニューバーアプリの title が正しく初期化されるかテスト

    このテストは rumps の実際の初期化を行うため、
    macOS 環境でのみ正常に動作します。
    """
    print("\n" + "=" * 60)
    print("テスト: メニューバーアプリの title 初期化")
    print("=" * 60)

    try:
        app = DisplayLayoutMenuBar()

        # title が設定されているか確認
        assert app.title is not None, "app.title が None であってはならない"
        print(f"  ✓ app.title が設定されている: '{app.title}'")

        # title が期待値と一致するか確認
        expected_title = "🖥️"
        assert (
            app.title == expected_title
        ), f"app.title は '{expected_title}' であるべき（実際: '{app.title}'）"
        print(f"  ✓ app.title が期待値と一致: '{expected_title}'")

        # name が設定されているか確認
        assert app.name is not None, "app.name が None であってはならない"
        print(f"  ✓ app.name が設定されている: '{app.name}'")

        print("\n  ✓ すべてのチェック成功")
        return True

    except Exception as e:
        print(f"  ✗ テスト失敗: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_menubar_components_initialization():
    """
    メニューバーアプリのコンポーネントが正しく初期化されるかテスト
    """
    print("\n" + "=" * 60)
    print("テスト: メニューバーアプリのコンポーネント初期化")
    print("=" * 60)

    try:
        app = DisplayLayoutMenuBar()

        # 必須コンポーネントの存在確認
        assert hasattr(app, "locale_detector"), "locale_detector が存在すべき"
        print("  ✓ locale_detector 初期化確認")

        assert hasattr(app, "msg"), "msg (MessageManager) が存在すべき"
        print("  ✓ msg (MessageManager) 初期化確認")

        assert hasattr(app, "cli_bridge"), "cli_bridge が存在すべき"
        print("  ✓ cli_bridge 初期化確認")

        assert hasattr(app, "auto_launch_manager"), "auto_launch_manager が存在すべき"
        print("  ✓ auto_launch_manager 初期化確認")

        # メニューが構築されているか確認
        assert hasattr(app, "menu"), "menu が存在すべき"
        print("  ✓ menu 構築確認")

        print("\n  ✓ すべてのコンポーネント初期化成功")
        return True

    except Exception as e:
        print(f"  ✗ テスト失敗: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 70)
    print("メニューバーアプリ 初期化統合テスト")
    print("=" * 70)
    print("\n注意: このテストは macOS 環境でのみ正常に動作します")

    tests = [
        ("title 初期化", test_menubar_title_initialization),
        ("コンポーネント初期化", test_menubar_components_initialization),
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
