"""
コマンド実行モジュール
displayplacerコマンドの実行と結果処理を管理
"""

import subprocess
import shlex
from typing import Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from .config_manager import ConfigPattern


@dataclass
class ExecutionResult:
    """コマンド実行結果クラス"""

    success: bool
    command: str
    pattern_name: str
    stdout: str
    stderr: str
    return_code: int
    execution_time: datetime
    dry_run: bool = False

    def get_summary(self) -> str:
        """実行結果のサマリーを取得"""
        if self.dry_run:
            return f"[ドライラン] パターン '{self.pattern_name}' のコマンドを実行予定"
        elif self.success:
            return f"✓ パターン '{self.pattern_name}' の適用が完了しました"
        else:
            return f"✗ パターン '{self.pattern_name}' の適用に失敗しました (終了コード: {self.return_code})"


class CommandExecutor:
    """コマンド実行クラス"""

    def __init__(self, verbose: bool = False, dry_run: bool = False):
        self.verbose = verbose
        self.dry_run = dry_run

    def _log(self, message: str) -> None:
        """ログ出力（詳細モード時のみ）"""
        if self.verbose:
            print(f"[コマンド実行] {message}")

    def _validate_command(self, command: str) -> Tuple[bool, str]:
        """
        コマンドの基本検証

        Args:
            command: 実行するコマンド

        Returns:
            Tuple[bool, str]: (有効フラグ, エラーメッセージ)
        """
        if not command:
            return False, "コマンドが空です"

        if not command.strip().startswith("displayplacer"):
            return False, "コマンドは 'displayplacer' で開始する必要があります"

        # 基本的な構文チェック
        try:
            # シェルコマンドとして解析可能かチェック
            shlex.split(command)
        except ValueError as e:
            return False, f"コマンド構文エラー: {e}"

        return True, ""

    def _execute_command(
        self, command: str, timeout: int = 60
    ) -> Tuple[bool, str, str, int]:
        """
        実際のコマンド実行

        Args:
            command: 実行するコマンド
            timeout: タイムアウト秒数

        Returns:
            Tuple[bool, str, str, int]: (成功フラグ, stdout, stderr, 終了コード)
        """
        try:
            self._log(f"コマンド実行開始: {command[:50]}...")

            # コマンドをシェル経由で実行
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout
            )

            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if success:
                self._log(f"コマンド実行成功 (終了コード: {result.returncode})")
            else:
                self._log(
                    f"コマンド実行失敗 (終了コード: {result.returncode}): {stderr[:100]}..."
                )

            return success, stdout, stderr, result.returncode

        except subprocess.TimeoutExpired:
            error_msg = f"コマンドがタイムアウトしました ({timeout}秒)"
            self._log(error_msg)
            return False, "", error_msg, -1
        except Exception as e:
            error_msg = f"コマンド実行エラー: {e}"
            self._log(error_msg)
            return False, "", error_msg, -1

    def execute_pattern(self, pattern: ConfigPattern) -> ExecutionResult:
        """
        パターンのコマンドを実行

        Args:
            pattern: 実行するパターン

        Returns:
            ExecutionResult: 実行結果
        """
        execution_time = datetime.now()

        self._log(f"パターン '{pattern.name}' の実行を開始")

        # コマンドの検証
        is_valid, validation_error = self._validate_command(pattern.command)
        if not is_valid:
            self._log(f"コマンド検証エラー: {validation_error}")
            return ExecutionResult(
                success=False,
                command=pattern.command,
                pattern_name=pattern.name,
                stdout="",
                stderr=validation_error,
                return_code=-1,
                execution_time=execution_time,
                dry_run=self.dry_run,
            )

        # ドライランモードの場合
        if self.dry_run:
            self._log(f"ドライランモード: コマンドを実際には実行しません")
            print(f"[ドライラン] 実行予定コマンド:")
            print(f"  {pattern.command}")

            return ExecutionResult(
                success=True,
                command=pattern.command,
                pattern_name=pattern.name,
                stdout="ドライランモード: コマンドは実行されませんでした",
                stderr="",
                return_code=0,
                execution_time=execution_time,
                dry_run=True,
            )

        # 実際のコマンド実行
        success, stdout, stderr, return_code = self._execute_command(pattern.command)

        result = ExecutionResult(
            success=success,
            command=pattern.command,
            pattern_name=pattern.name,
            stdout=stdout,
            stderr=stderr,
            return_code=return_code,
            execution_time=execution_time,
            dry_run=False,
        )

        # 結果のログ出力
        if success:
            self._log(f"パターン '{pattern.name}' の実行が完了しました")
        else:
            self._log(f"パターン '{pattern.name}' の実行に失敗しました: {stderr}")

        return result

    def execute_command_string(
        self, command: str, pattern_name: str = "Manual Command"
    ) -> ExecutionResult:
        """
        コマンド文字列を直接実行

        Args:
            command: 実行するコマンド文字列
            pattern_name: パターン名（ログ用）

        Returns:
            ExecutionResult: 実行結果
        """
        # 一時的なパターンオブジェクトを作成
        temp_pattern = ConfigPattern(
            name=pattern_name,
            description="手動実行コマンド",
            screen_ids=[],
            command=command,
        )

        return self.execute_pattern(temp_pattern)

    def get_execution_log(self, result: ExecutionResult) -> str:
        """
        実行結果の詳細ログを生成

        Args:
            result: 実行結果

        Returns:
            str: 詳細ログ
        """
        log_lines = []

        log_lines.append(
            f"実行時刻: {result.execution_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        log_lines.append(f"パターン名: {result.pattern_name}")
        log_lines.append(f"ドライラン: {'はい' if result.dry_run else 'いいえ'}")
        log_lines.append(f"実行結果: {'成功' if result.success else '失敗'}")

        if not result.dry_run:
            log_lines.append(f"終了コード: {result.return_code}")

        log_lines.append(f"実行コマンド:")
        log_lines.append(f"  {result.command}")

        if result.stdout:
            log_lines.append(f"標準出力:")
            for line in result.stdout.split("\n"):
                log_lines.append(f"  {line}")

        if result.stderr:
            log_lines.append(f"標準エラー:")
            for line in result.stderr.split("\n"):
                log_lines.append(f"  {line}")

        return "\n".join(log_lines)

    def validate_displayplacer_available(self) -> Tuple[bool, str]:
        """
        displayplacerコマンドが利用可能かチェック

        Returns:
            Tuple[bool, str]: (利用可能フラグ, エラーメッセージ)
        """
        try:
            result = subprocess.run(
                ["displayplacer", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return True, ""
            else:
                return (
                    False,
                    f"displayplacer コマンドの実行に失敗しました: {result.stderr}",
                )

        except FileNotFoundError:
            return False, "displayplacer コマンドが見つかりません"
        except subprocess.TimeoutExpired:
            return False, "displayplacer コマンドがタイムアウトしました"
        except Exception as e:
            return False, f"displayplacer の確認中にエラーが発生しました: {e}"
