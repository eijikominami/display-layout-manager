"""
ディスプレイ管理モジュール
displayplacerコマンドを使用してディスプレイ情報を取得・管理
"""

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple


@dataclass
class DisplayConfiguration:
    """ディスプレイ構成クラス"""

    screen_ids: List[str]
    timestamp: datetime
    raw_output: str

    def __post_init__(self):
        """初期化後の処理"""
        # Screen IDsをソートして一貫性を保つ
        self.screen_ids = sorted(self.screen_ids)


class DisplayManager:
    """ディスプレイ管理クラス"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._current_config: Optional[DisplayConfiguration] = None

    def _log(self, message: str) -> None:
        """ログ出力（詳細モード時のみ）"""
        if self.verbose:
            print(f"[ディスプレイ] {message}")

    def _run_command(
        self, command: List[str], timeout: int = 30
    ) -> Tuple[bool, str, str]:
        """
        コマンドを実行し、結果を返す

        Returns:
            Tuple[bool, str, str]: (成功フラグ, stdout, stderr)
        """
        try:
            self._log(f"コマンド実行: {' '.join(command)}")
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=timeout
            )

            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if success:
                self._log(f"コマンド成功: {len(stdout)}文字の出力")
            else:
                self._log(f"コマンド失敗 (終了コード: {result.returncode}): {stderr[:100]}...")

            return success, stdout, stderr

        except subprocess.TimeoutExpired:
            self._log(f"コマンドタイムアウト: {' '.join(command)}")
            return False, "", "コマンドがタイムアウトしました"
        except Exception as e:
            self._log(f"コマンド実行エラー: {e}")
            return False, "", str(e)

    def extract_screen_ids(self, displayplacer_output: str) -> List[str]:
        """
        displayplacer listの出力からPersistent Screen IDを抽出

        Args:
            displayplacer_output: displayplacer listコマンドの出力

        Returns:
            List[str]: 抽出されたScreen IDのリスト
        """
        screen_ids = []

        # Persistent Screen IDを抽出する正規表現
        # 例: "Persistent screen id: 37D8832A-2D66-02CA-B9F7-8F30A301B230"
        id_pattern = r"Persistent screen id:\s*([A-F0-9-]+)"

        matches = re.findall(id_pattern, displayplacer_output, re.IGNORECASE)

        for match in matches:
            screen_id = match.strip()
            if screen_id and screen_id not in screen_ids:
                screen_ids.append(screen_id)
                self._log(f"Screen ID検出: {screen_id}")

        return sorted(screen_ids)  # 一貫性のためソート

    def get_current_displays(self) -> Tuple[bool, Optional[DisplayConfiguration], str]:
        """
        現在のディスプレイ構成を取得

        Returns:
            Tuple[bool, Optional[DisplayConfiguration], str]: (成功フラグ, 構成オブジェクト, エラーメッセージ)
        """
        self._log("現在のディスプレイ構成を取得中...")

        # displayplacer listコマンドを実行
        success, stdout, stderr = self._run_command(["displayplacer", "list"])

        if not success:
            error_msg = f"displayplacer listコマンドの実行に失敗しました: {stderr}"
            self._log(error_msg)
            return False, None, error_msg

        if not stdout:
            error_msg = "displayplacer listコマンドの出力が空です"
            self._log(error_msg)
            return False, None, error_msg

        # Screen IDを抽出
        screen_ids = self.extract_screen_ids(stdout)

        if not screen_ids:
            error_msg = "Screen IDを抽出できませんでした。displayplacerの出力形式が予期しないものです"
            self._log(error_msg)
            self._log(f"実際の出力: {stdout[:200]}...")
            return False, None, error_msg

        # DisplayConfigurationオブジェクトを作成
        config = DisplayConfiguration(
            screen_ids=screen_ids, timestamp=datetime.now(), raw_output=stdout
        )

        self._current_config = config
        self._log(f"ディスプレイ構成取得完了: {len(screen_ids)}個のディスプレイ")

        return True, config, ""

    def show_current_displays(self) -> bool:
        """
        現在のディスプレイ構成を表示

        Returns:
            bool: 成功フラグ
        """
        print("現在のディスプレイ構成を取得中...")

        success, config, error = self.get_current_displays()

        if not success:
            print(f"エラー: {error}")
            return False

        print(f"\n検出されたディスプレイ: {len(config.screen_ids)}個")
        print(f"取得時刻: {config.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        print("\nPersistent Screen IDs:")
        for i, screen_id in enumerate(config.screen_ids, 1):
            print(f"  {i}. {screen_id}")

        if self.verbose:
            print(f"\n--- displayplacer list の生出力 ---")
            print(config.raw_output)
            print("--- 生出力終了 ---")

        return True

    def get_screen_ids(self) -> List[str]:
        """
        現在のScreen IDリストを取得（キャッシュされた値を使用）

        Returns:
            List[str]: Screen IDのリスト
        """
        if self._current_config is None:
            success, config, _ = self.get_current_displays()
            if not success:
                return []

        return self._current_config.screen_ids if self._current_config else []

    def refresh_display_config(self) -> bool:
        """
        ディスプレイ構成を強制的に再取得

        Returns:
            bool: 成功フラグ
        """
        self._log("ディスプレイ構成を再取得中...")
        success, config, error = self.get_current_displays()

        if success:
            self._log("ディスプレイ構成の再取得完了")
        else:
            self._log(f"ディスプレイ構成の再取得失敗: {error}")

        return success

    def validate_displayplacer_output(self, output: str) -> Tuple[bool, List[str]]:
        """
        displayplacerの出力を検証

        Args:
            output: displayplacerコマンドの出力

        Returns:
            Tuple[bool, List[str]]: (有効フラグ, 問題のリスト)
        """
        issues = []

        if not output:
            issues.append("出力が空です")
            return False, issues

        # 基本的な出力形式の確認
        if "Persistent screen id:" not in output:
            issues.append("'Persistent screen id:' が見つかりません")

        # Screen IDの形式確認
        screen_ids = self.extract_screen_ids(output)
        if not screen_ids:
            issues.append("有効なScreen IDが見つかりません")

        # 重複チェック
        if len(screen_ids) != len(set(screen_ids)):
            issues.append("重複するScreen IDが検出されました")

        # Screen IDの形式チェック（UUID形式）
        uuid_pattern = r"^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$"
        for screen_id in screen_ids:
            if not re.match(uuid_pattern, screen_id, re.IGNORECASE):
                issues.append(f"無効なScreen ID形式: {screen_id}")

        return len(issues) == 0, issues
