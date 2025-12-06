#!/usr/bin/env python3
"""
Display Layout Manager - メインエントリーポイント
macOS用のディスプレイレイアウト自動設定アプリケーション
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

from . import __version__
from .dependency_manager import DependencyManager
from .config_manager import ConfigManager
from .display_manager import DisplayManager
from .pattern_matcher import PatternMatcher
from .command_executor import CommandExecutor
from .logger import Logger
from .error_handler import ErrorHandler
from .layout_saver import LayoutSaver


def parse_arguments() -> argparse.Namespace:
    """コマンドライン引数を解析"""
    parser = argparse.ArgumentParser(
        prog="display-layout-manager",
        description="macOS用ディスプレイレイアウト自動設定ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  display-layout-manager                    # 基本実行
  display-layout-manager --verbose         # 詳細ログ付き実行
  display-layout-manager --dry-run         # ドライラン（実際にコマンドを実行しない）
  display-layout-manager --show-displays   # 現在のディスプレイ構成を表示
  display-layout-manager --validate-config # 設定ファイルの検証
  display-layout-manager --save-current    # 現在のレイアウトを保存
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="設定ファイルのパス (デフォルト: ~/Library/Application Support/DisplayLayoutManager/config.json)",
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="詳細ログを表示")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ドライラン（実際にコマンドを実行しない）",
    )

    parser.add_argument(
        "--show-displays",
        action="store_true",
        help="現在のディスプレイ構成を表示して終了",
    )

    parser.add_argument(
        "--validate-config", action="store_true", help="設定ファイルの検証のみ実行"
    )

    parser.add_argument("--run-tests", action="store_true", help="統合テストを実行")

    parser.add_argument(
        "--save-current",
        action="store_true",
        help="現在のディスプレイレイアウトをパターンとして保存",
    )

    return parser.parse_args()


def main() -> int:
    """メイン実行関数"""
    try:
        args = parse_arguments()

        print(f"Display Layout Manager v{__version__}")

        # ログ・フィードバック管理の初期化
        logger = Logger(verbose=args.verbose, log_to_file=True)
        logger.info("system", f"Display Layout Manager v{__version__} 開始")

        # エラーハンドリングの初期化
        error_handler = ErrorHandler(verbose=args.verbose)

        # 設定管理の初期化
        config_manager = ConfigManager(verbose=args.verbose)
        config_path = config_manager.get_config_path(args.config)

        if args.verbose:
            print(f"設定ファイル: {config_path}")
            print(f"詳細ログ: 有効")
            if args.dry_run:
                print("ドライランモード: 有効")

        # 統合テスト実行の場合
        if args.run_tests:
            from .integration_test import run_integration_tests

            print("\n" + "=" * 50)
            logger.info("system", "統合テスト実行開始")

            test_success = run_integration_tests(verbose=args.verbose)

            if test_success:
                logger.success("system", "統合テスト全て成功")
                return 0
            else:
                logger.error("system", "統合テスト失敗")
                return 1

        # 設定ファイル検証のみの場合
        if args.validate_config:
            print("\n" + "=" * 50)
            print("設定ファイルを検証中...")

            is_valid, errors = config_manager.validate_config_file(config_path)

            if is_valid:
                print("✓ 設定ファイルは有効です")
                return 0
            else:
                print("✗ 設定ファイルに問題があります:")
                for error in errors:
                    print(f"  - {error}")
                return 1

        # 依存関係管理の初期化
        dependency_manager = DependencyManager(verbose=args.verbose)

        # 現在レイアウト保存の場合
        if args.save_current:
            print("\n" + "=" * 50)
            logger.info("system", "現在レイアウト保存開始")

            # 依存関係の確認（displayplacerが必要）
            if not dependency_manager.check_displayplacer():
                error_handler.handle_error("DISPLAYPLACER_NOT_FOUND")
                return error_handler.get_exit_code("DISPLAYPLACER_NOT_FOUND")

            # レイアウト保存の実行
            layout_saver = LayoutSaver(verbose=args.verbose)
            success = layout_saver.save_current_with_feedback(config_path)

            if success:
                logger.success("system", "現在レイアウト保存完了")
                return 0
            else:
                logger.error("system", "現在レイアウト保存失敗")
                return 1

        # ディスプレイ表示のみの場合
        if args.show_displays:
            print("\n" + "=" * 50)

            # 依存関係の確認（displayplacerが必要）
            if not dependency_manager.check_displayplacer():
                print("エラー: displayplacer が必要ですが見つかりません")
                print("以下のコマンドでインストールしてください:")
                print("brew install jakehilborn/jakehilborn/displayplacer")
                return 1

            # ディスプレイ管理の初期化
            display_manager = DisplayManager(verbose=args.verbose)

            # 現在のディスプレイ構成を表示
            if display_manager.show_current_displays():
                return 0
            else:
                return 1

        # 依存関係の確認とインストール
        print("\n" + "=" * 50)
        logger.info("system", "依存関係チェック開始")

        if not dependency_manager.ensure_dependencies():
            logger.error("system", "依存関係の問題により実行を中止")

            # 具体的な依存関係エラーを特定
            all_available, status = dependency_manager.check_all_dependencies()
            if not status.get("homebrew", False):
                error_handler.handle_error("HOMEBREW_NOT_FOUND")
                return error_handler.get_exit_code("HOMEBREW_NOT_FOUND")
            elif not status.get("displayplacer", False):
                error_handler.handle_error("DISPLAYPLACER_NOT_FOUND")
                return error_handler.get_exit_code("DISPLAYPLACER_NOT_FOUND")
            elif not status.get("gnu_grep", False):
                error_handler.handle_error("GNU_GREP_NOT_FOUND")
                return error_handler.get_exit_code("GNU_GREP_NOT_FOUND")
            else:
                error_handler.handle_error(
                    "UNEXPECTED_ERROR", {"component": "dependency"}
                )
                return error_handler.get_exit_code("UNEXPECTED_ERROR")

        # 依存関係チェック結果をログに記録
        all_available, status = dependency_manager.check_all_dependencies()
        for tool, available in status.items():
            logger.log_dependency_check(tool, available)

        # 設定ファイルの読み込み
        print("\n" + "=" * 50)
        print("設定ファイルを読み込み中...")
        logger.info("config", f"設定ファイル読み込み開始: {config_path}")

        success, config, errors = config_manager.ensure_config(config_path)

        if not success:
            logger.log_config_load(config_path, 0, False, errors)

            # エラーの種類を判定
            if not config_path.exists():
                error_handler.handle_error(
                    "CONFIG_FILE_NOT_FOUND", {"config_path": str(config_path)}
                )
                return error_handler.get_exit_code("CONFIG_FILE_NOT_FOUND")
            elif any("JSON構文エラー" in error for error in errors):
                error_handler.handle_error(
                    "CONFIG_SYNTAX_ERROR",
                    {"config_path": str(config_path), "errors": errors},
                )
                return error_handler.get_exit_code("CONFIG_SYNTAX_ERROR")
            else:
                error_handler.handle_error(
                    "CONFIG_VALIDATION_ERROR",
                    {"config_path": str(config_path), "errors": errors},
                )
                return error_handler.get_exit_code("CONFIG_VALIDATION_ERROR")

        config_manager.set_config(config)
        patterns = config_manager.get_patterns()
        logger.log_config_load(config_path, len(patterns), True)

        print(f"✓ 設定ファイル読み込み完了: {len(patterns)}個のパターン")

        if args.verbose:
            print("登録されているパターン:")
            for i, pattern in enumerate(patterns, 1):
                print(f"  {i}. {pattern.name}")
                if pattern.description:
                    print(f"     説明: {pattern.description}")
                print(f"     Screen IDs: {len(pattern.screen_ids)}個")

        # ディスプレイ管理の初期化とテスト
        print("\n" + "=" * 50)
        print("ディスプレイ構成を確認中...")
        logger.info("display", "ディスプレイ検出開始")

        display_manager = DisplayManager(verbose=args.verbose)
        success, current_config, error = display_manager.get_current_displays()

        if not success:
            logger.error("display", f"ディスプレイ検出失敗: {error}")

            if "Screen IDを抽出できませんでした" in error:
                error_handler.handle_error(
                    "NO_DISPLAYS_FOUND", {"error_details": error}
                )
                return error_handler.get_exit_code("NO_DISPLAYS_FOUND")
            else:
                error_handler.handle_error(
                    "DISPLAY_DETECTION_FAILED", {"error_details": error}
                )
                return error_handler.get_exit_code("DISPLAY_DETECTION_FAILED")

        logger.log_display_detection(current_config, True)
        print(f"✓ 現在のディスプレイ: {len(current_config.screen_ids)}個検出")

        if args.verbose:
            print("検出されたScreen IDs:")
            for i, screen_id in enumerate(current_config.screen_ids, 1):
                print(f"  {i}. {screen_id}")

        # パターンマッチング機能のテスト
        print("\n" + "=" * 50)
        print("パターンマッチングを実行中...")
        logger.info("pattern", "パターンマッチング開始")

        pattern_matcher = PatternMatcher(verbose=args.verbose)
        patterns = config_manager.get_patterns()

        # パターンの検証
        is_valid, validation_issues = pattern_matcher.validate_patterns(patterns)
        if not is_valid:
            logger.error("pattern", f"パターン検証失敗: {validation_issues}")
            error_handler.handle_error(
                "CONFIG_VALIDATION_ERROR",
                {"component": "pattern_validation", "issues": validation_issues},
            )
            return error_handler.get_exit_code("CONFIG_VALIDATION_ERROR")

        # パターンマッチングの実行
        match_result = pattern_matcher.match_display_configuration(
            current_config, patterns
        )
        logger.log_pattern_match(match_result, current_config.screen_ids)

        print(f"パターンマッチング結果:")
        if match_result.matched:
            print(f"  ✓ マッチしたパターン: {match_result.pattern.name}")
            print(f"  マッチタイプ: {match_result.match_type}")
            print(f"  信頼度: {match_result.confidence:.2f}")
            if match_result.pattern.description:
                print(f"  説明: {match_result.pattern.description}")
        else:
            print(f"  ✗ マッチするパターンなし")

        print(f"  詳細: {match_result.details}")

        if args.verbose:
            print("\nマッチング詳細:")
            summary = pattern_matcher.get_match_summary(
                match_result, current_config.screen_ids
            )
            for line in summary.split("\n"):
                print(f"  {line}")

        # コマンド実行機能のテスト
        print("\n" + "=" * 50)

        if match_result.matched:
            print("マッチしたパターンのコマンドを実行します...")
            logger.info("command", f"コマンド実行開始: {match_result.pattern.name}")

            # コマンド実行器の初期化
            command_executor = CommandExecutor(
                verbose=args.verbose, dry_run=args.dry_run
            )

            # displayplacerの利用可能性確認
            is_available, error_msg = (
                command_executor.validate_displayplacer_available()
            )
            if not is_available:
                logger.error("command", f"displayplacer利用不可: {error_msg}")
                error_handler.handle_error(
                    "DISPLAYPLACER_NOT_FOUND", {"error_details": error_msg}
                )
                return error_handler.get_exit_code("DISPLAYPLACER_NOT_FOUND")

            # パターンのコマンドを実行
            execution_result = command_executor.execute_pattern(match_result.pattern)
            logger.log_command_execution(execution_result)

            # 結果の表示
            print(execution_result.get_summary())

            if args.verbose:
                print("\n実行詳細:")
                execution_log = command_executor.get_execution_log(execution_result)
                for line in execution_log.split("\n"):
                    print(f"  {line}")

            if not execution_result.success and not execution_result.dry_run:
                logger.error("command", "コマンド実行失敗により終了")

                if "タイムアウト" in execution_result.stderr:
                    error_handler.handle_error(
                        "COMMAND_TIMEOUT",
                        {
                            "pattern_name": execution_result.pattern_name,
                            "command": execution_result.command,
                            "stderr": execution_result.stderr,
                        },
                    )
                    return error_handler.get_exit_code("COMMAND_TIMEOUT")
                else:
                    error_handler.handle_error(
                        "COMMAND_EXECUTION_FAILED",
                        {
                            "pattern_name": execution_result.pattern_name,
                            "command": execution_result.command,
                            "return_code": execution_result.return_code,
                            "stderr": execution_result.stderr,
                        },
                    )
                    return error_handler.get_exit_code("COMMAND_EXECUTION_FAILED")
        else:
            logger.warning("pattern", "マッチするパターンなし - コマンド未実行")
            error_handler.handle_error(
                "NO_PATTERN_MATCH",
                {
                    "current_screen_count": len(current_config.screen_ids),
                    "current_screen_ids": current_config.screen_ids,
                    "available_patterns": [p.name for p in patterns],
                },
            )
            return error_handler.get_exit_code("NO_PATTERN_MATCH")

        print("\n" + "=" * 50)
        print("Display Layout Manager の実行が完了しました")

        # セッションサマリーの表示
        logger.success("system", "Display Layout Manager 正常終了")

        if args.verbose:
            logger.print_session_summary()

        # エラーがあった場合の警告
        if logger.has_errors():
            print("\n注意: 実行中にエラーが発生しました")
            if logger.get_log_file_path():
                print(
                    f"詳細はログファイルを確認してください: {logger.get_log_file_path()}"
                )

        return 0

    except KeyboardInterrupt:
        print("\n中断されました")
        if "logger" in locals():
            logger.warning("system", "ユーザーによる中断")
        return 1
    except Exception as e:
        if "error_handler" in locals():
            error_code = error_handler.handle_exception(e, {"component": "main"})
            if "logger" in locals():
                logger.error("system", f"予期しないエラー: {e}")
            return error_handler.get_exit_code(error_code)
        else:
            print(f"エラーが発生しました: {e}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())
