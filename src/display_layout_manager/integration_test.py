"""
統合テストモジュール
エンドツーエンドテストとエラーシナリオテストを実行
"""

import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

from .dependency_manager import DependencyManager
from .config_manager import ConfigManager, ConfigPattern
from .display_manager import DisplayManager
from .pattern_matcher import PatternMatcher
from .command_executor import CommandExecutor
from .logger import Logger
from .daemon_manager import DaemonManager
from .display_monitor import DisplayMonitor
from .event_processor import EventProcessor
from .configuration_watcher import DaemonConfigManager


@dataclass
class TestResult:
    """テスト結果クラス"""
    test_name: str
    success: bool
    message: str
    details: Dict[str, Any]
    execution_time: float


class IntegrationTester:
    """統合テストクラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results: List[TestResult] = []
        self.temp_dir: Path = None
    
    def _log(self, message: str) -> None:
        """ログ出力（詳細モード時のみ）"""
        if self.verbose:
            print(f"[統合テスト] {message}")
    
    def setup_test_environment(self) -> None:
        """テスト環境のセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="display_layout_test_"))
        self._log(f"テスト環境作成: {self.temp_dir}")
    
    def cleanup_test_environment(self) -> None:
        """テスト環境のクリーンアップ"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self._log(f"テスト環境削除: {self.temp_dir}")
    
    def create_test_config(self, config_data: Dict[str, Any]) -> Path:
        """テスト用設定ファイルを作成"""
        config_path = self.temp_dir / "test_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        return config_path
    
    def test_dependency_management(self) -> TestResult:
        """依存関係管理のテスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("依存関係管理テスト開始")
            
            dependency_manager = DependencyManager(verbose=False)
            
            # 各依存関係の個別チェック
            homebrew_available = dependency_manager.check_homebrew()
            displayplacer_available = dependency_manager.check_displayplacer()
            gnu_grep_available = dependency_manager.check_gnu_grep()
            
            # 全体チェック
            all_available, status = dependency_manager.check_all_dependencies()
            
            details = {
                "homebrew": homebrew_available,
                "displayplacer": displayplacer_available,
                "gnu_grep": gnu_grep_available,
                "all_available": all_available,
                "status": status
            }
            
            success = all_available and homebrew_available and displayplacer_available and gnu_grep_available
            message = "依存関係管理テスト成功" if success else "依存関係管理テスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("dependency_management", success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("dependency_management", False, f"依存関係管理テストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_config_management(self) -> TestResult:
        """設定ファイル管理のテスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("設定ファイル管理テスト開始")
            
            config_manager = ConfigManager(verbose=False)
            
            # 有効な設定ファイルのテスト
            valid_config = {
                "version": "1.0",
                "patterns": [
                    {
                        "name": "Test Pattern",
                        "description": "テスト用パターン",
                        "screen_ids": ["TEST-ID-1", "TEST-ID-2"],
                        "command": "displayplacer \"test command\""
                    }
                ]
            }
            
            valid_config_path = self.create_test_config(valid_config)
            success, config, errors = config_manager.load_config(valid_config_path)
            
            # 無効な設定ファイルのテスト
            invalid_config = {
                "version": "1.0",
                "patterns": [
                    {
                        "name": "",  # 無効な名前
                        "screen_ids": [],  # 空のscreen_ids
                        "command": "invalid command"  # 無効なコマンド
                    }
                ]
            }
            
            invalid_config_path = self.create_test_config(invalid_config)
            invalid_success, invalid_config_obj, invalid_errors = config_manager.load_config(invalid_config_path)
            
            details = {
                "valid_config_success": success,
                "valid_config_patterns": len(config.patterns) if config else 0,
                "valid_config_errors": errors,
                "invalid_config_success": invalid_success,
                "invalid_config_errors": invalid_errors
            }
            
            test_success = success and not invalid_success and len(invalid_errors) > 0
            message = "設定ファイル管理テスト成功" if test_success else "設定ファイル管理テスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("config_management", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("config_management", False, f"設定ファイル管理テストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_display_detection(self) -> TestResult:
        """ディスプレイ検出のテスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("ディスプレイ検出テスト開始")
            
            display_manager = DisplayManager(verbose=False)
            
            # 現在のディスプレイ構成取得
            success, config, error = display_manager.get_current_displays()
            
            details = {
                "detection_success": success,
                "screen_count": len(config.screen_ids) if config else 0,
                "screen_ids": config.screen_ids if config else [],
                "error": error
            }
            
            # 基本的な検証
            if success and config:
                # Screen IDの形式チェック
                valid_ids = all(len(sid) > 0 for sid in config.screen_ids)
                # 重複チェック
                no_duplicates = len(config.screen_ids) == len(set(config.screen_ids))
                
                details.update({
                    "valid_screen_ids": valid_ids,
                    "no_duplicates": no_duplicates
                })
                
                test_success = success and valid_ids and no_duplicates
            else:
                test_success = False
            
            message = "ディスプレイ検出テスト成功" if test_success else f"ディスプレイ検出テスト失敗: {error}"
            
            execution_time = time.time() - start_time
            return TestResult("display_detection", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("display_detection", False, f"ディスプレイ検出テストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_pattern_matching(self) -> TestResult:
        """パターンマッチングのテスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("パターンマッチングテスト開始")
            
            pattern_matcher = PatternMatcher(verbose=False)
            
            # テスト用パターンの作成
            test_patterns = [
                ConfigPattern(
                    name="Single Display",
                    description="単一ディスプレイ",
                    screen_ids=["TEST-ID-1"],
                    command="displayplacer \"test single\""
                ),
                ConfigPattern(
                    name="Dual Display",
                    description="デュアルディスプレイ",
                    screen_ids=["TEST-ID-1", "TEST-ID-2"],
                    command="displayplacer \"test dual\""
                )
            ]
            
            # 完全一致テスト
            exact_match_result = pattern_matcher.find_best_match(["TEST-ID-1", "TEST-ID-2"], test_patterns)
            
            # 部分一致テスト
            partial_match_result = pattern_matcher.find_best_match(["TEST-ID-1"], test_patterns)
            
            # 不一致テスト
            no_match_result = pattern_matcher.find_best_match(["UNKNOWN-ID"], test_patterns)
            
            details = {
                "exact_match": {
                    "matched": exact_match_result.matched,
                    "pattern_name": exact_match_result.pattern.name if exact_match_result.pattern else None,
                    "match_type": exact_match_result.match_type,
                    "confidence": exact_match_result.confidence
                },
                "partial_match": {
                    "matched": partial_match_result.matched,
                    "pattern_name": partial_match_result.pattern.name if partial_match_result.pattern else None,
                    "match_type": partial_match_result.match_type,
                    "confidence": partial_match_result.confidence
                },
                "no_match": {
                    "matched": no_match_result.matched,
                    "match_type": no_match_result.match_type,
                    "confidence": no_match_result.confidence
                }
            }
            
            # テスト成功条件
            test_success = (
                exact_match_result.matched and 
                exact_match_result.match_type == "exact" and
                exact_match_result.pattern.name == "Dual Display" and
                not no_match_result.matched
            )
            
            message = "パターンマッチングテスト成功" if test_success else "パターンマッチングテスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("pattern_matching", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("pattern_matching", False, f"パターンマッチングテストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_command_execution(self) -> TestResult:
        """コマンド実行のテスト（ドライランのみ）"""
        import time
        start_time = time.time()
        
        try:
            self._log("コマンド実行テスト開始")
            
            command_executor = CommandExecutor(verbose=False, dry_run=True)
            
            # 有効なコマンドのテスト
            valid_pattern = ConfigPattern(
                name="Test Pattern",
                description="テスト用パターン",
                screen_ids=["TEST-ID"],
                command="displayplacer \"test command\""
            )
            
            valid_result = command_executor.execute_pattern(valid_pattern)
            
            # 無効なコマンドのテスト
            invalid_pattern = ConfigPattern(
                name="Invalid Pattern",
                description="無効なパターン",
                screen_ids=["TEST-ID"],
                command="displayplacer invalid\"syntax"  # 構文エラーのあるコマンド
            )
            
            invalid_result = command_executor.execute_pattern(invalid_pattern)
            
            details = {
                "valid_command": {
                    "success": valid_result.success,
                    "dry_run": valid_result.dry_run,
                    "pattern_name": valid_result.pattern_name
                },
                "invalid_command": {
                    "success": invalid_result.success,
                    "dry_run": invalid_result.dry_run,
                    "pattern_name": invalid_result.pattern_name,
                    "error": invalid_result.stderr
                }
            }
            
            # テスト成功条件（ドライランでは有効なコマンドは成功、無効なコマンドは失敗）
            test_success = valid_result.success and valid_result.dry_run and not invalid_result.success
            
            message = "コマンド実行テスト成功" if test_success else "コマンド実行テスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("command_execution", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("command_execution", False, f"コマンド実行テストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_logging_system(self) -> TestResult:
        """ログシステムのテスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("ログシステムテスト開始")
            
            logger = Logger(verbose=False, log_to_file=False)
            
            # 各レベルのログをテスト
            logger.info("test", "テスト情報メッセージ")
            logger.success("test", "テスト成功メッセージ")
            logger.warning("test", "テスト警告メッセージ")
            logger.error("test", "テストエラーメッセージ")
            
            # ログエントリの確認
            log_entries = logger.log_entries
            summary = logger.get_session_summary()
            
            details = {
                "total_entries": len(log_entries),
                "summary": summary,
                "has_errors": logger.has_errors(),
                "error_summary": logger.get_error_summary()
            }
            
            # テスト成功条件
            test_success = (
                len(log_entries) == 4 and
                summary["by_level"].get("INFO", 0) == 1 and
                summary["by_level"].get("SUCCESS", 0) == 1 and
                summary["by_level"].get("WARNING", 0) == 1 and
                summary["by_level"].get("ERROR", 0) == 1 and
                logger.has_errors()
            )
            
            message = "ログシステムテスト成功" if test_success else "ログシステムテスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("logging_system", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("logging_system", False, f"ログシステムテストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_layout_saver(self) -> TestResult:
        """レイアウト保存機能のテスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("レイアウト保存機能テスト開始")
            
            from .layout_saver import LayoutSaver
            
            layout_saver = LayoutSaver(verbose=False)
            
            # パターン名生成のテスト
            test_screen_ids = ["TEST-ID-1", "TEST-ID-2", "TEST-ID-3"]
            pattern_name = layout_saver.generate_pattern_name(test_screen_ids)
            
            # コマンド抽出のテスト
            mock_output = """
Persistent screen id: TEST-ID-1
Resolution: 1920x1080

Execute the command below to set your screens to the current arrangement.
displayplacer "id:TEST-ID-1 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(0,0) degree:0"
"""
            extracted_command = layout_saver.extract_current_command(mock_output)
            
            details = {
                "pattern_name_generated": pattern_name,
                "expected_pattern_name": "3_Displays_TEST-ID-_TEST-ID-_TEST-ID-",
                "command_extracted": bool(extracted_command),
                "extracted_command": extracted_command[:50] + "..." if extracted_command else ""
            }
            
            # テスト成功条件
            test_success = (
                pattern_name == "3_Displays_TEST-ID-_TEST-ID-_TEST-ID-" and
                extracted_command.startswith("displayplacer") and
                "TEST-ID-1" in extracted_command
            )
            
            message = "レイアウト保存機能テスト成功" if test_success else "レイアウト保存機能テスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("layout_saver", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("layout_saver", False, f"レイアウト保存機能テストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_daemon_management(self) -> TestResult:
        """常駐機能管理テスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("常駐機能管理テスト開始")
            
            daemon_manager = DaemonManager(verbose=self.verbose)
            
            # 初期状態の確認
            initial_status = daemon_manager.get_daemon_status()
            
            # plist ファイル生成テスト（実際にはインストールしない）
            plist_content_valid = daemon_manager._find_executable_path() is not None
            
            details = {
                "initial_installed": initial_status.is_installed,
                "initial_running": initial_status.is_running,
                "executable_found": plist_content_valid,
                "plist_path": str(daemon_manager.plist_path),
                "log_path": str(daemon_manager.log_path)
            }
            
            # テスト成功条件（実際のインストールは行わない）
            test_success = True  # 基本的な初期化が成功すれば OK
            
            message = "常駐機能管理テスト成功" if test_success else "常駐機能管理テスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("daemon_management", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("daemon_management", False, f"常駐機能管理テストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_display_monitoring(self) -> TestResult:
        """ディスプレイ監視機能テスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("ディスプレイ監視機能テスト開始")
            
            events_received = []
            
            def test_callback(event):
                events_received.append(event)
            
            display_monitor = DisplayMonitor(callback=test_callback)
            
            # 初期状態の確認
            current_displays = display_monitor.get_current_displays()
            current_count = display_monitor.get_current_display_count()
            
            details = {
                "current_display_count": current_count,
                "current_displays": current_displays[:3] if current_displays else [],  # 最初の3つのみ
                "monitor_initialized": True,
                "callback_set": test_callback is not None
            }
            
            # テスト成功条件
            test_success = (
                current_count >= 0 and
                isinstance(current_displays, list)
            )
            
            message = "ディスプレイ監視機能テスト成功" if test_success else "ディスプレイ監視機能テスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("display_monitoring", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("display_monitoring", False, f"ディスプレイ監視機能テストエラー: {e}", {"error": str(e)}, execution_time)
    
    def test_daemon_config_management(self) -> TestResult:
        """常駐設定管理テスト"""
        import time
        start_time = time.time()
        
        try:
            self._log("常駐設定管理テスト開始")
            
            config_manager = DaemonConfigManager(verbose=self.verbose)
            
            # 設定の読み込み
            config = config_manager.load_config()
            
            # 設定の検証
            config_valid = (
                'daemon' in config and
                'monitoring' in config and
                'execution' in config and
                'logging' in config
            )
            
            # デフォルト値の確認
            daemon_config = config.get('daemon', {})
            debounce_delay = daemon_config.get('debounce_delay', 0)
            auto_execute = daemon_config.get('auto_execute', False)
            
            details = {
                "config_loaded": config is not None,
                "config_valid": config_valid,
                "debounce_delay": debounce_delay,
                "auto_execute": auto_execute,
                "config_path": str(config_manager.config_path)
            }
            
            # テスト成功条件
            test_success = (
                config_valid and
                isinstance(debounce_delay, (int, float)) and
                debounce_delay >= 0
            )
            
            message = "常駐設定管理テスト成功" if test_success else "常駐設定管理テスト失敗"
            
            execution_time = time.time() - start_time
            return TestResult("daemon_config_management", test_success, message, details, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("daemon_config_management", False, f"常駐設定管理テストエラー: {e}", {"error": str(e)}, execution_time)

    def run_all_tests(self) -> List[TestResult]:
        """全テストを実行"""
        print("統合テスト開始...")
        
        self.setup_test_environment()
        
        try:
            # 各テストを実行
            tests = [
                self.test_dependency_management,
                self.test_config_management,
                self.test_display_detection,
                self.test_pattern_matching,
                self.test_command_execution,
                self.test_logging_system,
                self.test_layout_saver,
                self.test_daemon_management,
                self.test_display_monitoring,
                self.test_daemon_config_management
            ]
            
            for test_func in tests:
                result = test_func()
                self.test_results.append(result)
                
                status = "✓" if result.success else "✗"
                print(f"  {status} {result.test_name}: {result.message}")
                
                if self.verbose:
                    print(f"    実行時間: {result.execution_time:.2f}秒")
                    if not result.success:
                        print(f"    詳細: {result.details}")
        
        finally:
            self.cleanup_test_environment()
        
        return self.test_results
    
    def get_test_summary(self) -> Dict[str, Any]:
        """テストサマリーを取得"""
        if not self.test_results:
            return {"message": "テストが実行されていません"}
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - passed_tests
        
        total_time = sum(result.execution_time for result in self.test_results)
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            "total_execution_time": total_time,
            "all_passed": failed_tests == 0
        }
    
    def print_test_summary(self) -> None:
        """テストサマリーを表示"""
        summary = self.get_test_summary()
        
        if "message" in summary:
            print(summary["message"])
            return
        
        print("\n" + "="*50)
        print("統合テストサマリー")
        print("="*50)
        
        print(f"総テスト数: {summary['total_tests']}")
        print(f"成功: {summary['passed_tests']}")
        print(f"失敗: {summary['failed_tests']}")
        print(f"成功率: {summary['success_rate']:.1f}%")
        print(f"総実行時間: {summary['total_execution_time']:.2f}秒")
        
        if summary['all_passed']:
            print("\n✓ すべてのテストが成功しました")
        else:
            print("\n✗ 一部のテストが失敗しました")
            print("\n失敗したテスト:")
            for result in self.test_results:
                if not result.success:
                    print(f"  - {result.test_name}: {result.message}")


def run_integration_tests(verbose: bool = False) -> bool:
    """統合テストを実行"""
    tester = IntegrationTester(verbose=verbose)
    tester.run_all_tests()
    tester.print_test_summary()
    
    summary = tester.get_test_summary()
    return summary.get('all_passed', False)