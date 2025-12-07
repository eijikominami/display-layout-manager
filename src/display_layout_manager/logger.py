"""
ログ・フィードバック管理モジュール
構造化ログ出力とユーザーフィードバックを管理

Note: Log files are always written in English (technical records).
      CLI output is internationalized based on system locale.
"""

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .command_executor import ExecutionResult
from .display_manager import DisplayConfiguration
from .i18n import LocaleDetector, MessageManager
from .pattern_matcher import MatchResult


@dataclass
class LogEntry:
    """ログエントリクラス"""

    timestamp: str
    level: str  # "INFO", "WARNING", "ERROR", "SUCCESS"
    component: str  # "dependency", "config", "display", "pattern", "command"
    message: str
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return asdict(self)


class Logger:
    """ログ・フィードバック管理クラス"""

    def __init__(
        self, verbose: bool = False, log_to_file: bool = True, daemon_mode: bool = False
    ):
        self.verbose = verbose
        self.log_to_file = log_to_file
        self.daemon_mode = daemon_mode
        self.log_entries = []
        self._log_file_path: Optional[Path] = None

        # Initialize i18n for CLI output
        self.locale_detector = LocaleDetector()
        self.msg = MessageManager(self.locale_detector)

        if self.log_to_file:
            self._setup_log_file()

    def _setup_log_file(self) -> None:
        """ログファイルのセットアップ"""
        log_dir = Path.home() / "Library" / "Logs" / "DisplayLayoutManager"
        log_dir.mkdir(parents=True, exist_ok=True)

        if self.daemon_mode:
            # 常駐モードの場合は専用ログファイル
            self._log_file_path = log_dir / "daemon.log"
        else:
            # 通常モードの場合は日付付きログファイル
            timestamp = datetime.now().strftime("%Y%m%d")
            self._log_file_path = log_dir / f"display_layout_manager_{timestamp}.log"

        # ディレクトリの権限設定
        os.chmod(log_dir, 0o700)

    def _write_to_file(self, log_entry: LogEntry) -> None:
        """ログファイルに書き込み"""
        if not self.log_to_file or not self._log_file_path:
            return

        try:
            with open(self._log_file_path, "a", encoding="utf-8") as f:
                json.dump(log_entry.to_dict(), f, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            # ログファイル書き込みエラーは標準エラー出力のみ
            print(f"ログファイル書き込みエラー: {e}", file=__import__("sys").stderr)

    def _log(
        self,
        level: str,
        component: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Internal logging method
        
        Note: Log file messages are always in English (technical records).
              CLI output is not printed here - use print() with MessageManager in calling code.
        """
        timestamp = datetime.now().isoformat()

        log_entry = LogEntry(
            timestamp=timestamp,
            level=level,
            component=component,
            message=message,  # Always English for log files
            details=details,
        )

        self.log_entries.append(log_entry)

        if self.log_to_file:
            self._write_to_file(log_entry)

        # Note: CLI output is handled by calling code using MessageManager
        # This ensures log files are in English while CLI output is internationalized

    def info(
        self, component: str, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """情報ログ"""
        self._log("INFO", component, message, details)

    def success(
        self, component: str, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """成功ログ"""
        self._log("SUCCESS", component, message, details)

    def warning(
        self, component: str, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """警告ログ"""
        self._log("WARNING", component, message, details)

    def error(
        self, component: str, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """エラーログ"""
        self._log("ERROR", component, message, details)

    def debug(
        self, component: str, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """デバッグログ"""
        self._log("DEBUG", component, message, details)

    def log_dependency_check(
        self, tool: str, available: bool, version: Optional[str] = None
    ) -> None:
        """依存関係チェックのログ"""
        if available:
            details = {"version": version} if version else None
            self.success("dependency", f"{tool} が利用可能です", details)
        else:
            self.error("dependency", f"{tool} が見つかりません")

    def log_config_load(
        self,
        config_path: Path,
        pattern_count: int,
        success: bool,
        errors: Optional[list] = None,
    ) -> None:
        """設定ファイル読み込みのログ"""
        details = {
            "config_path": str(config_path),
            "pattern_count": pattern_count if success else 0,
        }

        if success:
            self.success(
                "config",
                f"設定ファイル読み込み完了: {pattern_count}個のパターン",
                details,
            )
        else:
            details["errors"] = errors or []
            self.error("config", "設定ファイル読み込み失敗", details)

    def log_display_detection(
        self, display_config: DisplayConfiguration, success: bool
    ) -> None:
        """ディスプレイ検出のログ"""
        if success:
            details = {
                "screen_count": len(display_config.screen_ids),
                "screen_ids": display_config.screen_ids,
                "timestamp": display_config.timestamp.isoformat(),
            }
            self.success(
                "display",
                f"ディスプレイ検出完了: {len(display_config.screen_ids)}個",
                details,
            )
        else:
            self.error("display", "ディスプレイ検出失敗")

    def log_pattern_match(
        self, match_result: MatchResult, current_screen_ids: list
    ) -> None:
        """パターンマッチングのログ"""
        details = {
            "current_screen_ids": current_screen_ids,
            "match_type": match_result.match_type,
            "confidence": match_result.confidence,
        }

        if match_result.matched:
            details.update(
                {
                    "pattern_name": match_result.pattern.name,
                    "pattern_description": match_result.pattern.description,
                }
            )
            self.success(
                "pattern", f"パターンマッチ成功: {match_result.pattern.name}", details
            )
        else:
            self.warning("pattern", "マッチするパターンなし", details)

    def log_command_execution(self, execution_result: ExecutionResult) -> None:
        """コマンド実行のログ"""
        details = {
            "pattern_name": execution_result.pattern_name,
            "command": execution_result.command,
            "return_code": execution_result.return_code,
            "dry_run": execution_result.dry_run,
            "execution_time": execution_result.execution_time.isoformat(),
        }

        if execution_result.success:
            if execution_result.dry_run:
                self.info(
                    "command", f"ドライラン: {execution_result.pattern_name}", details
                )
            else:
                self.success(
                    "command",
                    f"コマンド実行成功: {execution_result.pattern_name}",
                    details,
                )
        else:
            details.update(
                {"stdout": execution_result.stdout, "stderr": execution_result.stderr}
            )
            self.error(
                "command", f"コマンド実行失敗: {execution_result.pattern_name}", details
            )

    def get_session_summary(self) -> Dict[str, Any]:
        """セッションサマリーを取得"""
        summary = {
            "total_entries": len(self.log_entries),
            "by_level": {},
            "by_component": {},
            "session_start": (
                self.log_entries[0].timestamp if self.log_entries else None
            ),
            "session_end": self.log_entries[-1].timestamp if self.log_entries else None,
        }

        # レベル別集計
        for entry in self.log_entries:
            summary["by_level"][entry.level] = (
                summary["by_level"].get(entry.level, 0) + 1
            )
            summary["by_component"][entry.component] = (
                summary["by_component"].get(entry.component, 0) + 1
            )

        return summary

    def print_session_summary(self) -> None:
        """セッションサマリーを表示 (internationalized)"""
        if not self.log_entries:
            return

        summary = self.get_session_summary()

        print("\n" + "=" * 50)
        print(self.msg.get("session_summary"))
        print("=" * 50)

        print(self.msg.get("total_log_entries", count=summary['total_entries']))

        if summary["by_level"]:
            print(f"\n{self.msg.get('by_level')}")
            for level, count in summary["by_level"].items():
                print(f"  {level}: {count}")

        if summary["by_component"]:
            print(f"\n{self.msg.get('by_component')}")
            for component, count in summary["by_component"].items():
                print(f"  {component}: {count}")

        if self._log_file_path and self.log_to_file:
            print(f"\n{self.msg.get('log_file', path=self._log_file_path)}")

    def export_logs(self, output_path: Path) -> bool:
        """ログをファイルにエクスポート"""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for entry in self.log_entries:
                    json.dump(entry.to_dict(), f, ensure_ascii=False)
                    f.write("\n")

            print(f"ログをエクスポートしました: {output_path}")
            return True
        except Exception as e:
            print(f"ログエクスポートエラー: {e}")
            return False

    def get_error_summary(self) -> list:
        """エラーサマリーを取得"""
        errors = [entry for entry in self.log_entries if entry.level == "ERROR"]
        return [
            {"component": e.component, "message": e.message, "timestamp": e.timestamp}
            for e in errors
        ]

    def has_errors(self) -> bool:
        """エラーが発生したかチェック"""
        return any(entry.level == "ERROR" for entry in self.log_entries)

    def get_log_file_path(self) -> Optional[Path]:
        """ログファイルパスを取得"""
        return self._log_file_path
