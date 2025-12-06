#!/usr/bin/env python3
"""
テストカバレッジを測定するスクリプト
"""
import subprocess
import sys
from pathlib import Path


def run_coverage():
    """カバレッジ測定を実行"""
    project_root = Path(__file__).parent.parent

    print("=" * 80)
    print("テストカバレッジ測定")
    print("=" * 80)

    # カバレッジデータをクリア
    print("\n1. カバレッジデータをクリア...")
    subprocess.run([sys.executable, "-m", "coverage", "erase"], cwd=project_root)

    # 各テストファイルを個別に実行してカバレッジを収集
    test_files = [
        "tests/test_cli_components.py",
        "tests/test_dependency_manager.py",
        "tests/test_display_manager.py",
        "tests/test_command_executor.py",
        "tests/test_layout_saver.py",
        "tests/test_menubar_checkbox.py",
        "tests/test_menubar_logic.py",
        "tests/test_menubar_integration.py",
    ]

    print("\n2. テストを実行してカバレッジを収集...")
    for test_file in test_files:
        print(f"  実行中: {test_file}")
        result = subprocess.run(
            [sys.executable, "-m", "coverage", "run", "-a", "--source=src", test_file],
            cwd=project_root,
            capture_output=True,
        )
        if result.returncode != 0:
            print(f"    ✗ 失敗: {test_file}")
        else:
            print(f"    ✓ 成功: {test_file}")

    # カバレッジレポートを生成
    print("\n3. カバレッジレポートを生成...")
    print("\n" + "=" * 80)
    print("カバレッジレポート")
    print("=" * 80)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "report",
            "--omit=*/tests/*,*/integration_test.py",
        ],
        cwd=project_root,
    )

    # HTML レポートを生成
    print("\n4. HTML レポートを生成...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "html",
            "--omit=*/tests/*,*/integration_test.py",
        ],
        cwd=project_root,
    )

    print("\n" + "=" * 80)
    print("HTML レポートが生成されました: htmlcov/index.html")
    print("=" * 80)

    return result.returncode == 0


if __name__ == "__main__":
    success = run_coverage()
    sys.exit(0 if success else 1)
