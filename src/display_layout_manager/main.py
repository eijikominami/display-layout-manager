#!/usr/bin/env python3
"""
Display Layout Manager - メインエントリーポイント
macOS用のディスプレイレイアウト自動設定アプリケーション
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .command_executor import CommandExecutor
from .config_manager import ConfigManager
from .dependency_manager import DependencyManager
from .display_manager import DisplayManager
from .error_handler import ErrorHandler
from .i18n import LocaleDetector, MessageManager
from .layout_saver import LayoutSaver
from .logger import Logger
from .pattern_matcher import PatternMatcher


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

        # Initialize i18n
        locale_detector = LocaleDetector()
        msg = MessageManager(locale_detector)

        print(msg.get("app_start", version=__version__))

        # ログ・フィードバック管理の初期化
        logger = Logger(verbose=args.verbose, log_to_file=True)
        logger.info("system", f"Display Layout Manager v{__version__} started")

        # エラーハンドリングの初期化
        error_handler = ErrorHandler(verbose=args.verbose)

        # 設定管理の初期化
        config_manager = ConfigManager(verbose=args.verbose)
        config_path = config_manager.get_config_path(args.config)

        if args.verbose:
            print(msg.get("config_file_path", path=config_path))
            print(msg.get("verbose_enabled"))
            if args.dry_run:
                print(msg.get("dry_run_enabled"))

        # 統合テスト実行の場合
        if args.run_tests:
            from .integration_test import run_integration_tests

            print("\n" + "=" * 50)
            logger.info("system", "Integration test execution started")

            test_success = run_integration_tests(verbose=args.verbose)

            if test_success:
                logger.success("system", "All integration tests passed")
                return 0
            else:
                logger.error("system", "Integration tests failed")
                return 1

        # 設定ファイル検証のみの場合
        if args.validate_config:
            print("\n" + "=" * 50)
            print(msg.get("validating_config"))

            is_valid, errors = config_manager.validate_config_file(config_path)

            if is_valid:
                print(f"✓ {msg.get('config_valid')}")
                return 0
            else:
                print(f"✗ {msg.get('config_invalid')}")
                for error in errors:
                    print(f"  - {error}")
                return 1

        # 依存関係管理の初期化
        dependency_manager = DependencyManager(verbose=args.verbose)

        # 現在レイアウト保存の場合
        if args.save_current:
            print("\n" + "=" * 50)
            logger.info("system", "Current layout save started")

            # 依存関係の確認（displayplacerが必要）
            if not dependency_manager.check_displayplacer():
                error_handler.handle_error("DISPLAYPLACER_NOT_FOUND")
                return error_handler.get_exit_code("DISPLAYPLACER_NOT_FOUND")

            # レイアウト保存の実行
            layout_saver = LayoutSaver(verbose=args.verbose)
            success = layout_saver.save_current_with_feedback(config_path)

            if success:
                logger.success("system", "Current layout save completed")
                return 0
            else:
                logger.error("system", "Current layout save failed")
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
        logger.info("system", "Dependency check started")

        if not dependency_manager.ensure_dependencies():
            logger.error("system", "Execution aborted due to dependency issues")

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
        print(msg.get("loading_config"))
        logger.info("config", f"Configuration file loading started: {config_path}")

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

        print(f"✓ {msg.get('config_loaded', count=len(patterns))}")

        if args.verbose:
            print(msg.get("registered_patterns"))
            for i, pattern in enumerate(patterns, 1):
                print(f"  {msg.get('pattern_info', index=i, name=pattern.name)}")
                if pattern.description:
                    print(
                        f"     {msg.get('pattern_description', description=pattern.description)}"
                    )
                print(
                    f"     {msg.get('pattern_screen_count', count=len(pattern.screen_ids))}"
                )

        # ディスプレイ管理の初期化とテスト
        print("\n" + "=" * 50)
        print(msg.get("checking_displays"))
        logger.info("display", "Display detection started")

        display_manager = DisplayManager(verbose=args.verbose)
        success, current_config, error = display_manager.get_current_displays()

        if not success:
            logger.error("display", f"Display detection failed: {error}")

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
        print(f"✓ {msg.get('displays_detected', count=len(current_config.screen_ids))}")

        if args.verbose:
            print(msg.get("detected_screen_ids"))
            for i, screen_id in enumerate(current_config.screen_ids, 1):
                print(f"  {msg.get('screen_id_item', index=i, screen_id=screen_id)}")

        # パターンマッチング機能のテスト
        print("\n" + "=" * 50)
        print(msg.get("pattern_matching"))
        logger.info("pattern", "Pattern matching started")

        pattern_matcher = PatternMatcher(verbose=args.verbose)
        patterns = config_manager.get_patterns()

        # パターンの検証
        is_valid, validation_issues = pattern_matcher.validate_patterns(patterns)
        if not is_valid:
            logger.error("pattern", f"Pattern validation failed: {validation_issues}")
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

        print(msg.get("pattern_match_result"))
        if match_result.matched:
            print(msg.get("pattern_matched", name=match_result.pattern.name))
            print(msg.get("pattern_match_type", type=match_result.match_type))
            print(msg.get("pattern_confidence", confidence=match_result.confidence))
            if match_result.pattern.description:
                print(
                    msg.get(
                        "pattern_description",
                        description=match_result.pattern.description,
                    )
                )
        else:
            print(msg.get("pattern_no_match"))

        print(msg.get("pattern_details", details=match_result.details))

        if args.verbose:
            print(f"\n{msg.get('matching_details')}")
            summary = pattern_matcher.get_match_summary(
                match_result, current_config.screen_ids
            )
            for line in summary.split("\n"):
                print(f"  {line}")

        # コマンド実行機能のテスト
        print("\n" + "=" * 50)

        if match_result.matched:
            print(msg.get("executing_command"))
            logger.info(
                "command", f"Command execution started: {match_result.pattern.name}"
            )

            # コマンド実行器の初期化
            command_executor = CommandExecutor(
                verbose=args.verbose, dry_run=args.dry_run
            )

            # displayplacerの利用可能性確認
            is_available, error_msg = (
                command_executor.validate_displayplacer_available()
            )
            if not is_available:
                logger.error("command", f"displayplacer not available: {error_msg}")
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
                print(f"\n{msg.get('execution_details')}")
                execution_log = command_executor.get_execution_log(execution_result)
                for line in execution_log.split("\n"):
                    print(f"  {line}")

            if not execution_result.success and not execution_result.dry_run:
                logger.error("command", "Command execution failed, terminating")

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
            logger.warning("pattern", "No matching pattern - command not executed")
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
        print(msg.get("app_complete"))

        # セッションサマリーの表示
        logger.success("system", "Display Layout Manager completed successfully")

        if args.verbose:
            logger.print_session_summary()

        # エラーがあった場合の警告
        if logger.has_errors():
            print(f"\n{msg.get('errors_occurred')}")
            if logger.get_log_file_path():
                print(msg.get("check_log_file", path=logger.get_log_file_path()))

        return 0

    except KeyboardInterrupt:
        print(f"\n{msg.get('app_interrupted') if 'msg' in locals() else 'Interrupted'}")
        if "logger" in locals():
            logger.warning("system", "Interrupted by user")
        return 1
    except Exception as e:
        if "error_handler" in locals():
            error_code = error_handler.handle_exception(e, {"component": "main"})
            if "logger" in locals():
                logger.error("system", f"Unexpected error: {e}")
            return error_handler.get_exit_code(error_code)
        else:
            error_msg = (
                msg.get("app_error", error=e)
                if "msg" in locals()
                else f"An error occurred: {e}"
            )
            print(error_msg, file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())
