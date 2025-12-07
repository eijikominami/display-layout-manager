#!/usr/bin/env python3
"""
DependencyManager の単体テスト
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from display_layout_manager.dependency_manager import DependencyManager


def test_check_homebrew():
    """Homebrew 存在確認のテスト"""
    print("\n=== test_check_homebrew ===")

    manager = DependencyManager(verbose=True)
    result = manager.check_homebrew()

    print(f"結果: {'✓ Homebrew が利用可能' if result else '✗ Homebrew が見つかりません'}")

    # Homebrew は通常インストールされているはず
    assert result, "Homebrew が見つかりません。このテストを実行するには Homebrew が必要です"

    print("✓ test_check_homebrew 成功")


def test_check_displayplacer():
    """displayplacer 存在確認のテスト"""
    print("\n=== test_check_displayplacer ===")

    manager = DependencyManager(verbose=True)
    result = manager.check_displayplacer()

    print(f"結果: {'✓ displayplacer が利用可能' if result else '✗ displayplacer が見つかりません'}")

    # displayplacer は通常インストールされているはず
    assert result, "displayplacer が見つかりません。このテストを実行するには displayplacer が必要です"

    print("✓ test_check_displayplacer 成功")


def test_check_gnu_grep():
    """GNU grep 存在確認のテスト"""
    print("\n=== test_check_gnu_grep ===")

    manager = DependencyManager(verbose=True)
    result = manager.check_gnu_grep()

    print(f"結果: {'✓ GNU grep が利用可能' if result else '✗ GNU grep が見つかりません'}")

    # GNU grep は通常インストールされているはず
    assert result, "GNU grep が見つかりません。このテストを実行するには GNU grep が必要です"

    print("✓ test_check_gnu_grep 成功")


def test_check_all_dependencies():
    """すべての依存関係チェックのテスト"""
    print("\n=== test_check_all_dependencies ===")

    manager = DependencyManager(verbose=False)
    all_available, status = manager.check_all_dependencies()

    print(f"\n結果:")
    print(f"  すべて利用可能: {all_available}")
    print(f"  Homebrew: {status['homebrew']}")
    print(f"  displayplacer: {status['displayplacer']}")
    print(f"  GNU grep: {status['gnu_grep']}")

    # すべての依存関係が利用可能であることを確認
    assert all_available, "一部の依存関係が利用できません"
    assert status["homebrew"], "Homebrew が利用できません"
    assert status["displayplacer"], "displayplacer が利用できません"
    assert status["gnu_grep"], "GNU grep が利用できません"

    print("✓ test_check_all_dependencies 成功")


def test_run_command():
    """コマンド実行機能のテスト"""
    print("\n=== test_run_command ===")

    manager = DependencyManager(verbose=True)

    # 成功するコマンド
    success, stdout, stderr = manager._run_command(["echo", "test"])
    assert success, "echo コマンドの実行に失敗しました"
    assert "test" in stdout, "echo コマンドの出力が期待と異なります"
    print("✓ 成功するコマンドのテスト完了")

    # 失敗するコマンド
    success, stdout, stderr = manager._run_command(["false"])
    assert not success, "false コマンドが成功してしまいました"
    print("✓ 失敗するコマンドのテスト完了")

    # 存在しないコマンド
    success, stdout, stderr = manager._run_command(["nonexistent_command_12345"])
    assert not success, "存在しないコマンドが成功してしまいました"
    print("✓ 存在しないコマンドのテスト完了")

    print("✓ test_run_command 成功")


def main():
    """メイン関数"""
    print("=" * 80)
    print("DependencyManager 単体テスト")
    print("=" * 80)

    tests = [
        test_check_homebrew,
        test_check_displayplacer,
        test_check_gnu_grep,
        test_check_all_dependencies,
        test_run_command,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 失敗: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} エラー: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"テスト結果: {passed}/{len(tests)} 成功, {failed}/{len(tests)} 失敗")
    print("=" * 80)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
