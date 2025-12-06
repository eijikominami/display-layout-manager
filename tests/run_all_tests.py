#!/usr/bin/env python3
"""
全テストを実行するマスタースクリプト
"""
import sys
import subprocess
from pathlib import Path


def run_test_file(test_file: str) -> bool:
    """テストファイルを実行"""
    print(f"\n{'='*80}")
    print(f"実行中: {test_file}")
    print("=" * 80)

    result = subprocess.run(
        [sys.executable, test_file],
        cwd=Path(__file__).parent.parent,
        capture_output=False,
    )

    return result.returncode == 0


def main():
    """メイン関数"""
    print("\n" + "=" * 80)
    print("Display Layout Manager - 全テストスイート")
    print("=" * 80)

    # テストファイルのリスト
    test_files = [
        # CLI コンポーネントテスト
        "tests/test_cli_components.py",
        "tests/test_dependency_manager.py",
        "tests/test_display_manager.py",
        "tests/test_command_executor.py",
        "tests/test_layout_saver.py",
        # メニューバーアプリテスト
        "tests/test_menubar_checkbox.py",
        "tests/test_menubar_logic.py",
        "tests/test_menubar_integration.py",
    ]

    results = {}

    for test_file in test_files:
        test_name = Path(test_file).stem
        success = run_test_file(test_file)
        results[test_name] = success

    # 結果サマリー
    print("\n" + "=" * 80)
    print("全テスト結果サマリー")
    print("=" * 80)

    passed = sum(1 for success in results.values() if success)
    total = len(results)

    for test_name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\n合計: {passed}/{total} テストファイル成功")
    print("=" * 80)

    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
