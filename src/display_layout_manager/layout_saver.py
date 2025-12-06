"""
レイアウト保存モジュール
現在のディスプレイレイアウトを設定ファイルに保存する機能を提供
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from .config_manager import ConfigManager, ConfigPattern, Configuration
from .display_manager import DisplayManager


@dataclass
class SaveResult:
    """保存結果クラス"""

    success: bool
    pattern_name: str
    action: str  # "created", "updated"
    screen_count: int
    screen_ids: List[str]
    message: str
    error_details: Optional[str] = None


class LayoutSaver:
    """レイアウト保存クラス"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.display_manager = DisplayManager(verbose=verbose)
        self.config_manager = ConfigManager(verbose=verbose)

    def _log(self, message: str) -> None:
        """ログ出力（詳細モード時のみ）"""
        if self.verbose:
            print(f"[レイアウト保存] {message}")

    def generate_pattern_name(self, screen_ids: List[str]) -> str:
        """Screen IDsからユニークなパターン名を生成"""
        # Screen IDsをソートして一貫性を保つ
        sorted_ids = sorted(screen_ids)

        # 各IDの最初の8文字を使用
        short_ids = [sid[:8] for sid in sorted_ids]

        # ディスプレイ数とIDの組み合わせでパターン名を作成
        display_count = len(screen_ids)
        if display_count == 1:
            return f"Single_Display_{short_ids[0]}"
        else:
            # 複数ディスプレイの場合
            id_hash = "_".join(short_ids)
            return f"{display_count}_Displays_{id_hash}"

    def extract_current_command(self, displayplacer_output: str) -> str:
        """displayplacer listの出力から現在の設定コマンドを抽出"""
        lines = displayplacer_output.split("\n")

        # "Execute the command below" の後の行を探す
        for i, line in enumerate(lines):
            if "Execute the command below" in line:
                # 次の行以降でdisplayplacerコマンドを探す
                for j in range(i + 1, len(lines)):
                    potential_command = lines[j].strip()
                    if potential_command.startswith("displayplacer"):
                        self._log(f"現在設定コマンド抽出: {potential_command[:50]}...")
                        return potential_command

        # 最後の行がdisplayplacerコマンドの場合もある
        for line in reversed(lines):
            line = line.strip()
            if line.startswith("displayplacer"):
                self._log(f"現在設定コマンド抽出（最終行）: {line[:50]}...")
                return line

        # 見つからない場合は空文字列を返す
        self._log("現在設定コマンドが見つかりませんでした")
        return ""

    def find_existing_pattern_by_screen_ids(
        self, screen_ids: List[str], patterns: List[ConfigPattern]
    ) -> Optional[ConfigPattern]:
        """同じScreen IDsを持つ既存パターンを検索"""
        current_sorted = sorted(screen_ids)

        for pattern in patterns:
            pattern_sorted = sorted(pattern.screen_ids)
            if current_sorted == pattern_sorted:
                self._log(f"既存パターン発見: {pattern.name}")
                return pattern

        self._log("既存パターンなし")
        return None

    def save_current_layout(self, config_path: Path) -> SaveResult:
        """現在のディスプレイレイアウトを保存"""
        self._log("現在のレイアウト保存を開始")

        try:
            # 現在のディスプレイ構成を取得
            success, current_config, error = self.display_manager.get_current_displays()
            if not success:
                return SaveResult(
                    success=False,
                    pattern_name="",
                    action="",
                    screen_count=0,
                    screen_ids=[],
                    message="ディスプレイ検出に失敗しました",
                    error_details=error,
                )

            screen_ids = current_config.screen_ids
            screen_count = len(screen_ids)

            self._log(f"検出されたディスプレイ: {screen_count}個")

            # パターン名を生成
            pattern_name = self.generate_pattern_name(screen_ids)
            self._log(f"生成されたパターン名: {pattern_name}")

            # 現在の設定コマンドを抽出
            current_command = self.extract_current_command(current_config.raw_output)
            if not current_command:
                return SaveResult(
                    success=False,
                    pattern_name=pattern_name,
                    action="",
                    screen_count=screen_count,
                    screen_ids=screen_ids,
                    message="現在の設定コマンドを抽出できませんでした",
                    error_details="displayplacer listの出力から設定コマンドが見つかりません",
                )

            # 既存の設定を読み込み
            success, config, errors = self.config_manager.ensure_config(config_path)
            if not success:
                return SaveResult(
                    success=False,
                    pattern_name=pattern_name,
                    action="",
                    screen_count=screen_count,
                    screen_ids=screen_ids,
                    message="設定ファイルの読み込みに失敗しました",
                    error_details="; ".join(errors),
                )

            # 既存パターンをチェック
            existing_pattern = self.find_existing_pattern_by_screen_ids(
                screen_ids, config.patterns
            )

            # 新しいパターンを作成
            new_pattern = ConfigPattern(
                name=pattern_name,
                description=f"自動生成: {screen_count}個のディスプレイ構成",
                screen_ids=screen_ids,
                command=current_command,
            )

            action = "updated" if existing_pattern else "created"

            # パターンを追加または更新
            if existing_pattern:
                # 既存パターンを置き換え
                for i, pattern in enumerate(config.patterns):
                    if pattern.name == existing_pattern.name:
                        config.patterns[i] = new_pattern
                        break
            else:
                # 新しいパターンを追加
                config.patterns.append(new_pattern)

            # 設定ファイルに保存
            save_success = self.save_config_to_file(config, config_path)
            if not save_success:
                return SaveResult(
                    success=False,
                    pattern_name=pattern_name,
                    action=action,
                    screen_count=screen_count,
                    screen_ids=screen_ids,
                    message="設定ファイルの保存に失敗しました",
                    error_details="ファイル書き込みエラー",
                )

            # 成功結果を返す
            action_text = "更新" if action == "updated" else "作成"
            return SaveResult(
                success=True,
                pattern_name=pattern_name,
                action=action,
                screen_count=screen_count,
                screen_ids=screen_ids,
                message=f"パターン '{pattern_name}' を{action_text}しました",
            )

        except Exception as e:
            self._log(f"保存処理中にエラー: {e}")
            return SaveResult(
                success=False,
                pattern_name="",
                action="",
                screen_count=0,
                screen_ids=[],
                message="予期しないエラーが発生しました",
                error_details=str(e),
            )

    def save_config_to_file(self, config: Configuration, config_path: Path) -> bool:
        """設定をファイルに保存"""
        try:
            # 設定ディレクトリを確保
            self.config_manager.ensure_config_directory(config_path)

            # JSON形式で保存
            config_data = {
                "version": config.version,
                "patterns": [
                    {
                        "name": pattern.name,
                        "description": pattern.description,
                        "screen_ids": pattern.screen_ids,
                        "command": pattern.command,
                    }
                    for pattern in config.patterns
                ],
            }

            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)

            self._log(f"設定ファイル保存完了: {config_path}")
            return True

        except Exception as e:
            self._log(f"設定ファイル保存エラー: {e}")
            return False

    def display_save_result(self, result: SaveResult) -> None:
        """保存結果をユーザーに表示"""
        if result.success:
            print("現在のディスプレイ構成を保存中...")
            print(f"検出されたディスプレイ: {result.screen_count}個")

            if self.verbose:
                for i, screen_id in enumerate(result.screen_ids, 1):
                    print(f"  {i}. {screen_id}")

            action_symbol = "✓"
            print(f"{action_symbol} {result.message}")
        else:
            print("現在のディスプレイ構成の保存に失敗しました")
            print(f"エラー: {result.message}")

            if result.error_details and self.verbose:
                print(f"詳細: {result.error_details}")

    def save_current_with_feedback(self, config_path: Path) -> bool:
        """現在のレイアウトを保存してユーザーにフィードバック"""
        result = self.save_current_layout(config_path)
        self.display_save_result(result)
        return result.success
