"""
Display Layout Manager - CLI Bridge

メニューバーアプリケーションと既存 CLI コンポーネントの連携
"""

from dataclasses import dataclass
from typing import Optional

from .command_executor import CommandExecutor
from .config_manager import ConfigManager
from .display_manager import DisplayManager
from .layout_saver import LayoutSaver
from .pattern_matcher import PatternMatcher


@dataclass
class ActionResult:
    """アクション実行結果クラス"""

    success: bool
    pattern_name: Optional[str] = None
    error_message: Optional[str] = None
    details: Optional[str] = None


class CLIBridge:
    """CLI コンポーネントとの連携クラス"""

    def __init__(self, verbose: bool = False):
        """
        初期化

        Args:
            verbose: 詳細ログ出力フラグ
        """
        self.verbose = verbose
        self.display_manager = DisplayManager(verbose=verbose)
        self.pattern_matcher = PatternMatcher(verbose=verbose)
        self.layout_saver = LayoutSaver(verbose=verbose)
        self.command_executor = CommandExecutor(verbose=verbose)
        self.config_manager = ConfigManager(verbose=verbose)

    def execute_apply_layout(self) -> ActionResult:
        """
        レイアウト適用を実行

        Returns:
            ActionResult: 実行結果
        """
        try:
            # 設定ファイルを読み込み
            config_path = self.config_manager.get_default_config_path()
            success, config, errors = self.config_manager.load_config(config_path)
            if not success:
                return ActionResult(
                    success=False,
                    error_message=f"設定ファイルの読み込みに失敗しました: {', '.join(errors)}",
                )

            # 現在のディスプレイ構成を取得
            success, current_config, error = self.display_manager.get_current_displays()
            if not success:
                return ActionResult(
                    success=False,
                    error_message=f"ディスプレイ情報の取得に失敗しました: {error}",
                )

            # パターンマッチング
            match_result = self.pattern_matcher.find_best_match(
                current_config.screen_ids, config.patterns
            )

            if not match_result.matched:
                return ActionResult(
                    success=False,
                    error_message="一致するパターンが見つかりません",
                    details=f"検出されたディスプレイ: {len(current_config.screen_ids)}個",
                )

            # コマンド実行
            exec_result = self.command_executor.execute_pattern(match_result.pattern)

            if exec_result.success:
                return ActionResult(
                    success=True,
                    pattern_name=match_result.pattern.name,
                    details=match_result.pattern.description,
                )
            else:
                return ActionResult(
                    success=False,
                    pattern_name=match_result.pattern.name,
                    error_message="レイアウトの適用に失敗しました",
                    details=exec_result.stderr,
                )

        except Exception as e:
            return ActionResult(
                success=False, error_message=f"予期しないエラーが発生しました: {str(e)}"
            )

    def execute_save_current(self) -> ActionResult:
        """
        現在の設定を保存

        Returns:
            ActionResult: 実行結果
        """
        try:
            config_path = self.config_manager.get_default_config_path()
            save_result = self.layout_saver.save_current_layout(config_path)

            if save_result.success:
                action_text = "作成" if save_result.action == "created" else "更新"
                return ActionResult(
                    success=True,
                    pattern_name=save_result.pattern_name,
                    details=f"パターンを{action_text}しました（ディスプレイ: {save_result.screen_count}個）",
                )
            else:
                return ActionResult(
                    success=False,
                    error_message=save_result.message,
                    details=save_result.error_details,
                )

        except Exception as e:
            return ActionResult(
                success=False, error_message=f"予期しないエラーが発生しました: {str(e)}"
            )

    def get_current_displays(self) -> ActionResult:
        """
        現在接続されているディスプレイ情報を取得

        Returns:
            ActionResult: 実行結果
        """
        try:
            success, current_config, error = self.display_manager.get_current_displays()
            if not success:
                return ActionResult(
                    success=False,
                    error_message=f"ディスプレイ情報の取得に失敗しました: {error}",
                )

            display_info = f"接続されたディスプレイ: {len(current_config.screen_ids)}個\n"
            for i, screen_id in enumerate(current_config.screen_ids, 1):
                display_info += f"{i}. {screen_id[:16]}...\n"

            return ActionResult(success=True, details=display_info.strip())

        except Exception as e:
            return ActionResult(
                success=False, error_message=f"予期しないエラーが発生しました: {str(e)}"
            )
