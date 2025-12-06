"""
エラーハンドリング強化モジュール
包括的なエラー処理とユーザーフレンドリーなエラーメッセージを提供
"""

import sys
import traceback
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ErrorCategory(Enum):
    """エラーカテゴリ"""

    DEPENDENCY = "dependency"
    CONFIG = "config"
    DISPLAY = "display"
    PATTERN = "pattern"
    COMMAND = "command"
    SYSTEM = "system"
    NETWORK = "network"
    PERMISSION = "permission"


@dataclass
class ErrorInfo:
    """エラー情報クラス"""

    category: ErrorCategory
    code: str
    message: str
    details: Optional[str] = None
    suggestions: Optional[List[str]] = None
    technical_details: Optional[str] = None


class ErrorHandler:
    """エラーハンドリングクラス"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.error_catalog = self._build_error_catalog()

    def _build_error_catalog(self) -> Dict[str, ErrorInfo]:
        """エラーカタログを構築"""
        return {
            # 依存関係エラー
            "HOMEBREW_NOT_FOUND": ErrorInfo(
                category=ErrorCategory.DEPENDENCY,
                code="HOMEBREW_NOT_FOUND",
                message="Homebrew が見つかりません",
                details="Display Layout Manager は Homebrew を使用して依存関係を管理します",
                suggestions=[
                    "以下のコマンドで Homebrew をインストールしてください:",
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                    "インストール後、シェルを再起動してください",
                ],
            ),
            "DISPLAYPLACER_NOT_FOUND": ErrorInfo(
                category=ErrorCategory.DEPENDENCY,
                code="DISPLAYPLACER_NOT_FOUND",
                message="displayplacer が見つかりません",
                details="ディスプレイレイアウトの制御に displayplacer が必要です",
                suggestions=[
                    "以下のコマンドでインストールしてください:",
                    "brew install jakehilborn/jakehilborn/displayplacer",
                    "または手動でダウンロード: https://github.com/jakehilborn/displayplacer/releases",
                ],
            ),
            "GNU_GREP_NOT_FOUND": ErrorInfo(
                category=ErrorCategory.DEPENDENCY,
                code="GNU_GREP_NOT_FOUND",
                message="GNU grep が見つかりません",
                details="テキスト処理に GNU grep が必要です",
                suggestions=[
                    "以下のコマンドでインストールしてください:",
                    "brew install grep",
                    'PATH を設定: export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"',
                ],
            ),
            # 設定ファイルエラー
            "CONFIG_FILE_NOT_FOUND": ErrorInfo(
                category=ErrorCategory.CONFIG,
                code="CONFIG_FILE_NOT_FOUND",
                message="設定ファイルが見つかりません",
                details="指定された設定ファイルが存在しません",
                suggestions=[
                    "設定ファイルのパスを確認してください",
                    "--config オプションで正しいパスを指定してください",
                    "デフォルト設定ファイルを作成する場合は引数なしで実行してください",
                ],
            ),
            "CONFIG_SYNTAX_ERROR": ErrorInfo(
                category=ErrorCategory.CONFIG,
                code="CONFIG_SYNTAX_ERROR",
                message="設定ファイルの構文エラー",
                details="JSON 形式が正しくありません",
                suggestions=[
                    "JSON 構文を確認してください",
                    "オンライン JSON バリデーターを使用してください",
                    "コンマ、括弧、引用符の対応を確認してください",
                ],
            ),
            "CONFIG_VALIDATION_ERROR": ErrorInfo(
                category=ErrorCategory.CONFIG,
                code="CONFIG_VALIDATION_ERROR",
                message="設定ファイルの内容が無効です",
                details="必須フィールドが不足しているか、値が無効です",
                suggestions=[
                    "必須フィールド (version, patterns) を確認してください",
                    "各パターンに name, screen_ids, command が含まれているか確認してください",
                    "command が 'displayplacer' で開始しているか確認してください",
                ],
            ),
            # ディスプレイエラー
            "DISPLAY_DETECTION_FAILED": ErrorInfo(
                category=ErrorCategory.DISPLAY,
                code="DISPLAY_DETECTION_FAILED",
                message="ディスプレイの検出に失敗しました",
                details="displayplacer list コマンドの実行に失敗しました",
                suggestions=[
                    "displayplacer が正しくインストールされているか確認してください",
                    "ディスプレイが接続されているか確認してください",
                    "システムの表示設定を確認してください",
                ],
            ),
            "NO_DISPLAYS_FOUND": ErrorInfo(
                category=ErrorCategory.DISPLAY,
                code="NO_DISPLAYS_FOUND",
                message="ディスプレイが検出されませんでした",
                details="Persistent Screen ID を抽出できませんでした",
                suggestions=[
                    "ディスプレイが正しく接続されているか確認してください",
                    "システム環境設定 > ディスプレイ で認識されているか確認してください",
                    "displayplacer list を手動で実行して出力を確認してください",
                ],
            ),
            # パターンマッチングエラー
            "NO_PATTERN_MATCH": ErrorInfo(
                category=ErrorCategory.PATTERN,
                code="NO_PATTERN_MATCH",
                message="マッチするパターンが見つかりません",
                details="現在のディスプレイ構成に対応するパターンがありません",
                suggestions=[
                    "現在のディスプレイ構成を確認: --show-displays",
                    "設定ファイルに現在の構成に対応するパターンを追加してください",
                    "既存パターンの screen_ids を現在の値に更新してください",
                ],
            ),
            # コマンド実行エラー
            "COMMAND_EXECUTION_FAILED": ErrorInfo(
                category=ErrorCategory.COMMAND,
                code="COMMAND_EXECUTION_FAILED",
                message="displayplacer コマンドの実行に失敗しました",
                details="ディスプレイレイアウトの適用中にエラーが発生しました",
                suggestions=[
                    "コマンドの構文を確認してください",
                    "Screen ID が正しいか確認してください",
                    "解像度やリフレッシュレートが対応しているか確認してください",
                    "--dry-run オプションでコマンドを事前確認してください",
                ],
            ),
            "COMMAND_TIMEOUT": ErrorInfo(
                category=ErrorCategory.COMMAND,
                code="COMMAND_TIMEOUT",
                message="コマンドの実行がタイムアウトしました",
                details="displayplacer コマンドの実行に時間がかかりすぎています",
                suggestions=[
                    "システムの負荷を確認してください",
                    "ディスプレイの接続を確認してください",
                    "コマンドを手動で実行して問題を特定してください",
                ],
            ),
            # システムエラー
            "PERMISSION_DENIED": ErrorInfo(
                category=ErrorCategory.PERMISSION,
                code="PERMISSION_DENIED",
                message="権限が不足しています",
                details="ファイルまたはディレクトリへのアクセス権限がありません",
                suggestions=[
                    "ファイルの権限を確認してください",
                    "管理者権限で実行してください",
                    "ファイルの所有者を確認してください",
                ],
            ),
            "UNEXPECTED_ERROR": ErrorInfo(
                category=ErrorCategory.SYSTEM,
                code="UNEXPECTED_ERROR",
                message="予期しないエラーが発生しました",
                details="内部エラーが発生しました",
                suggestions=[
                    "--verbose オプションで詳細情報を確認してください",
                    "ログファイルを確認してください",
                    "問題が継続する場合は GitHub で報告してください",
                ],
            ),
        }

    def get_error_info(self, error_code: str) -> Optional[ErrorInfo]:
        """エラー情報を取得"""
        return self.error_catalog.get(error_code)

    def handle_error(
        self,
        error_code: str,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None,
    ) -> None:
        """エラーを処理して表示"""
        error_info = self.get_error_info(error_code)

        if not error_info:
            # 未知のエラーコード
            error_info = self.error_catalog["UNEXPECTED_ERROR"]

        # エラーメッセージの表示
        print(f"\nエラー: {error_info.message}", file=sys.stderr)

        if error_info.details:
            print(f"詳細: {error_info.details}", file=sys.stderr)

        # コンテキスト情報の表示
        if context:
            print("追加情報:", file=sys.stderr)
            for key, value in context.items():
                print(f"  {key}: {value}", file=sys.stderr)

        # 解決策の表示
        if error_info.suggestions:
            print("\n解決策:", file=sys.stderr)
            for i, suggestion in enumerate(error_info.suggestions, 1):
                print(f"  {i}. {suggestion}", file=sys.stderr)

        # 詳細モードでの技術的詳細
        if self.verbose:
            if error_info.technical_details:
                print(f"\n技術的詳細: {error_info.technical_details}", file=sys.stderr)

            if exception:
                print(f"\n例外詳細: {exception}", file=sys.stderr)
                print("スタックトレース:", file=sys.stderr)
                traceback.print_exc()

    def handle_exception(
        self, exception: Exception, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """例外を処理してエラーコードを返す"""
        exception_type = type(exception).__name__
        exception_message = str(exception).lower()

        # 例外の種類とメッセージから適切なエラーコードを推定
        if "permission" in exception_message or "access" in exception_message:
            error_code = "PERMISSION_DENIED"
        elif "timeout" in exception_message:
            error_code = "COMMAND_TIMEOUT"
        elif "json" in exception_message or "syntax" in exception_message:
            error_code = "CONFIG_SYNTAX_ERROR"
        elif (
            "file not found" in exception_message or "no such file" in exception_message
        ):
            error_code = "CONFIG_FILE_NOT_FOUND"
        else:
            error_code = "UNEXPECTED_ERROR"

        # エラーハンドリング
        self.handle_error(error_code, context, exception)

        return error_code

    def create_error_report(
        self,
        error_code: str,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None,
    ) -> Dict[str, Any]:
        """エラーレポートを作成"""
        error_info = (
            self.get_error_info(error_code) or self.error_catalog["UNEXPECTED_ERROR"]
        )

        report = {
            "error_code": error_code,
            "category": error_info.category.value,
            "message": error_info.message,
            "details": error_info.details,
            "suggestions": error_info.suggestions,
            "context": context or {},
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        }

        if exception:
            report["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "traceback": traceback.format_exc() if self.verbose else None,
            }

        return report

    def is_recoverable_error(self, error_code: str) -> bool:
        """エラーが回復可能かどうか判定"""
        recoverable_errors = {
            "CONFIG_FILE_NOT_FOUND",
            "NO_PATTERN_MATCH",
            "DISPLAY_DETECTION_FAILED",
        }
        return error_code in recoverable_errors

    def get_exit_code(self, error_code: str) -> int:
        """エラーコードに対応する終了コードを取得"""
        exit_codes = {
            "HOMEBREW_NOT_FOUND": 2,
            "DISPLAYPLACER_NOT_FOUND": 2,
            "GNU_GREP_NOT_FOUND": 2,
            "CONFIG_FILE_NOT_FOUND": 3,
            "CONFIG_SYNTAX_ERROR": 3,
            "CONFIG_VALIDATION_ERROR": 3,
            "DISPLAY_DETECTION_FAILED": 4,
            "NO_DISPLAYS_FOUND": 4,
            "NO_PATTERN_MATCH": 5,
            "COMMAND_EXECUTION_FAILED": 6,
            "COMMAND_TIMEOUT": 6,
            "PERMISSION_DENIED": 7,
            "UNEXPECTED_ERROR": 1,
        }
        return exit_codes.get(error_code, 1)
