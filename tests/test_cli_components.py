#!/usr/bin/env python3
"""
CLI コンポーネントの包括的単体テスト
"""
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# src ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from display_layout_manager.config_manager import ConfigManager
from display_layout_manager.pattern_matcher import PatternMatcher


def test_config_manager():
    """ConfigManager の単体テスト"""
    print("\n" + "=" * 70)
    print("テスト: ConfigManager")
    print("=" * 70)

    # 一時設定ファイルを作成
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        config_data = {
            "version": "1.0",
            "patterns": [
                {
                    "name": "Test Pattern",
                    "description": "テストパターン",
                    "screen_ids": ["SCREEN1", "SCREEN2"],
                    "command": "displayplacer test command",
                }
            ],
        }
        json.dump(config_data, f)
        config_path = f.name

    try:
        # ConfigManager インスタンス作成
        print("\n[1] ConfigManager 初期化")
        manager = ConfigManager()
        print("  ✓ インスタンス作成成功")

        # 設定読み込み
        print("\n[2] 設定ファイル読み込み")
        success, config, errors = manager.load_config(Path(config_path))
        assert success, f"設定が読み込まれるべき: {errors}"
        assert config is not None, "設定オブジェクトが存在すべき"
        assert len(config.patterns) == 1, "パターンが1つ存在すべき"
        print(f"  ✓ 設定読み込み成功: {len(config.patterns)} パターン")

        # パターン情報確認
        print("\n[3] パターン情報確認")
        pattern = config.patterns[0]
        assert pattern.name == "Test Pattern", "パターン名が一致すべき"
        assert len(pattern.screen_ids) == 2, "screen_ids が2つあるべき"
        print(f"  ✓ パターン情報確認成功: {pattern.name}")

        return True

    except Exception as e:
        print(f"\n✗ テスト失敗: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        # クリーンアップ
        if os.path.exists(config_path):
            os.unlink(config_path)


def test_pattern_matcher():
    """PatternMatcher の単体テスト"""
    print("\n" + "=" * 70)
    print("テスト: PatternMatcher")
    print("=" * 70)

    try:
        from display_layout_manager.config_manager import ConfigPattern

        # テストデータ
        patterns = [
            ConfigPattern(
                name="Pattern 1",
                description="パターン1",
                screen_ids=["SCREEN1", "SCREEN2"],
                command="displayplacer command1",
            ),
            ConfigPattern(
                name="Pattern 2",
                description="パターン2",
                screen_ids=["SCREEN3"],
                command="displayplacer command2",
            ),
        ]

        # PatternMatcher インスタンス作成
        print("\n[1] PatternMatcher 初期化")
        matcher = PatternMatcher()
        print("  ✓ インスタンス作成成功")

        # パターンマッチング - 一致
        print("\n[2] パターンマッチング（一致）")
        current_screens = ["SCREEN1", "SCREEN2"]
        result = matcher.find_best_match(current_screens, patterns)
        assert result.matched, "パターンが一致すべき"
        assert result.pattern.name == "Pattern 1", "Pattern 1 が一致すべき"
        print(f"  ✓ マッチング成功: {result.pattern.name}")

        # パターンマッチング - 不一致
        print("\n[3] パターンマッチング（不一致）")
        current_screens = ["SCREEN4", "SCREEN5"]
        result = matcher.find_best_match(current_screens, patterns)
        assert not result.matched, "パターンが一致しないべき"
        print("  ✓ 不一致確認成功")

        # パターンマッチング - 順序無関係
        print("\n[4] パターンマッチング（順序無関係）")
        current_screens = ["SCREEN2", "SCREEN1"]  # 逆順
        result = matcher.find_best_match(current_screens, patterns)
        assert result.matched, "順序に関係なく一致すべき"
        assert result.pattern.name == "Pattern 1", "Pattern 1 が一致すべき"
        print(f"  ✓ 順序無関係マッチング成功")

        return True

    except Exception as e:
        print(f"\n✗ テスト失敗: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_cli_bridge():
    """CLIBridge の単体テスト"""
    print("\n" + "=" * 70)
    print("テスト: CLIBridge")
    print("=" * 70)

    try:
        from display_layout_manager.cli_bridge import CLIBridge

        # CLIBridge インスタンス作成
        print("\n[1] CLIBridge 初期化")
        bridge = CLIBridge(verbose=False)
        print("  ✓ インスタンス作成成功")

        # メソッドの存在確認
        print("\n[2] メソッド存在確認")
        assert hasattr(
            bridge, "execute_apply_layout"
        ), "execute_apply_layout メソッドが存在すべき"
        assert hasattr(
            bridge, "execute_save_current"
        ), "execute_save_current メソッドが存在すべき"
        print("  ✓ 必要なメソッドが存在")

        return True

    except Exception as e:
        print(f"\n✗ テスト失敗: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 70)
    print("CLI コンポーネント 包括的単体テスト")
    print("=" * 70)

    tests = [
        ("ConfigManager", test_config_manager),
        ("PatternMatcher", test_pattern_matcher),
        ("CLIBridge", test_cli_bridge),
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
