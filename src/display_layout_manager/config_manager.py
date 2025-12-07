"""
設定ファイル管理モジュール
JSON形式の設定ファイルの読み込み、検証、デフォルト作成を管理
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ConfigPattern:
    """設定パターンクラス"""

    name: str
    description: str
    screen_ids: List[str]
    command: str

    def __post_init__(self):
        """初期化後の検証"""
        if not self.name:
            raise ValueError("パターン名は必須です")
        if not self.screen_ids:
            raise ValueError("screen_ids は必須です")
        if not self.command:
            raise ValueError("command は必須です")
        if not self.command.strip().startswith("displayplacer"):
            raise ValueError("command は 'displayplacer' で開始する必要があります")


@dataclass
class Configuration:
    """設定ファイル全体の構造"""

    version: str
    patterns: List[ConfigPattern]

    def __post_init__(self):
        """初期化後の検証"""
        if not self.version:
            raise ValueError("version は必須です")
        if not self.patterns:
            raise ValueError("patterns は必須です")


class ConfigManager:
    """設定ファイル管理クラス"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._config: Optional[Configuration] = None

    def _log(self, message: str) -> None:
        """ログ出力（詳細モード時のみ）"""
        if self.verbose:
            print(f"[設定管理] {message}")

    def get_default_config_path(self) -> Path:
        """デフォルト設定ファイルパスを取得"""
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "DisplayLayoutManager"
            / "config.json"
        )

    def get_config_path(self, config_arg: Optional[Path] = None) -> Path:
        """設定ファイルパスを決定（優先順位に従って）"""
        # 1. コマンドライン引数
        if config_arg:
            self._log(f"コマンドライン引数から設定ファイルパス: {config_arg}")
            return config_arg

        # 2. 環境変数
        env_config = os.environ.get("DISPLAY_LAYOUT_CONFIG")
        if env_config:
            path = Path(env_config)
            self._log(f"環境変数から設定ファイルパス: {path}")
            return path

        # 3. デフォルト
        default_path = self.get_default_config_path()
        self._log(f"デフォルト設定ファイルパス: {default_path}")
        return default_path

    def ensure_config_directory(self, config_path: Path) -> None:
        """設定ファイルディレクトリの作成"""
        config_dir = config_path.parent

        if not config_dir.exists():
            self._log(f"設定ディレクトリを作成: {config_dir}")
            config_dir.mkdir(parents=True, exist_ok=True)
            # macOS標準の権限設定
            os.chmod(config_dir, 0o700)
        else:
            self._log(f"設定ディレクトリは既に存在: {config_dir}")

    def create_default_config(self, config_path: Path) -> None:
        """デフォルト設定ファイルを作成"""
        self._log("デフォルト設定ファイルを作成中...")

        # 空の設定ファイルを作成
        default_config = {"version": "1.0", "patterns": []}

        # ディレクトリの作成
        self.ensure_config_directory(config_path)

        # ファイルの作成
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)

        # macOS標準の権限設定
        os.chmod(config_path, 0o600)

        print(f"デフォルト設定ファイルを作成しました: {config_path}")
        print("現在のディスプレイレイアウトを保存するには: display-layout-manager --save-current")
        print("接続されたディスプレイを確認するには: display-layout-manager --show-displays")

    def validate_config_structure(self, config_data: Dict[str, Any]) -> List[str]:
        """設定ファイル構造の検証"""
        errors = []

        # 必須フィールドの確認
        if "version" not in config_data:
            errors.append("必須フィールド 'version' が見つかりません")
        elif not isinstance(config_data["version"], str):
            errors.append("'version' は文字列である必要があります")

        if "patterns" not in config_data:
            errors.append("必須フィールド 'patterns' が見つかりません")
            return errors  # patternsがない場合は以降の検証をスキップ

        if not isinstance(config_data["patterns"], list):
            errors.append("'patterns' は配列である必要があります")
            return errors

        if len(config_data["patterns"]) == 0:
            errors.append("'patterns' は空にできません。少なくとも1つのパターンが必要です")
            return errors

        # 各パターンの検証
        for i, pattern in enumerate(config_data["patterns"]):
            if not isinstance(pattern, dict):
                errors.append(f"パターン {i+1}: パターンはオブジェクトである必要があります")
                continue

            # パターンの必須フィールド確認
            required_fields = ["name", "screen_ids", "command"]
            for field in required_fields:
                if field not in pattern:
                    errors.append(f"パターン {i+1}: 必須フィールド '{field}' が見つかりません")
                elif field == "name" and not isinstance(pattern[field], str):
                    errors.append(f"パターン {i+1}: '{field}' は文字列である必要があります")
                elif field == "screen_ids":
                    if not isinstance(pattern[field], list):
                        errors.append(f"パターン {i+1}: '{field}' は配列である必要があります")
                    elif len(pattern[field]) == 0:
                        errors.append(f"パターン {i+1}: '{field}' は空にできません")
                    elif not all(isinstance(sid, str) for sid in pattern[field]):
                        errors.append(f"パターン {i+1}: '{field}' の全要素は文字列である必要があります")
                elif field == "command":
                    if not isinstance(pattern[field], str):
                        errors.append(f"パターン {i+1}: '{field}' は文字列である必要があります")
                    elif not pattern[field].strip().startswith("displayplacer"):
                        errors.append(
                            f"パターン {i+1}: '{field}' は 'displayplacer' で開始する必要があります"
                        )

            # オプションフィールドの検証
            if "description" in pattern and not isinstance(pattern["description"], str):
                errors.append(f"パターン {i+1}: 'description' は文字列である必要があります")

        return errors

    def load_config(
        self, config_path: Path
    ) -> Tuple[bool, Optional[Configuration], List[str]]:
        """
        設定ファイルを読み込み

        Returns:
            Tuple[bool, Optional[Configuration], List[str]]: (成功フラグ, 設定オブジェクト, エラーリスト)
        """
        self._log(f"設定ファイルを読み込み中: {config_path}")

        # ファイル存在確認
        if not config_path.exists():
            return False, None, [f"設定ファイルが見つかりません: {config_path}"]

        try:
            # JSONファイルの読み込み
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            self._log("JSON解析完了")

            # 構造検証
            validation_errors = self.validate_config_structure(config_data)
            if validation_errors:
                return False, None, validation_errors

            # Configurationオブジェクトの作成
            patterns = []
            for pattern_data in config_data["patterns"]:
                pattern = ConfigPattern(
                    name=pattern_data["name"],
                    description=pattern_data.get("description", ""),
                    screen_ids=pattern_data["screen_ids"],
                    command=pattern_data["command"],
                )
                patterns.append(pattern)

            config = Configuration(version=config_data["version"], patterns=patterns)

            self._log(f"設定ファイル読み込み完了: {len(patterns)}個のパターン")
            return True, config, []

        except json.JSONDecodeError as e:
            error_msg = f"JSON構文エラー: {e.msg} (行 {e.lineno}, 列 {e.colno})"
            return False, None, [error_msg]
        except Exception as e:
            error_msg = f"設定ファイル読み込みエラー: {e}"
            return False, None, [error_msg]

    def validate_config_file(self, config_path: Path) -> Tuple[bool, List[str]]:
        """
        設定ファイルの検証のみ実行

        Returns:
            Tuple[bool, List[str]]: (有効フラグ, エラーリスト)
        """
        success, config, errors = self.load_config(config_path)
        return success, errors

    def ensure_config(
        self, config_path: Path
    ) -> Tuple[bool, Optional[Configuration], List[str]]:
        """
        設定ファイルを確保（存在しない場合は作成）

        Returns:
            Tuple[bool, Optional[Configuration], List[str]]: (成功フラグ, 設定オブジェクト, エラーリスト)
        """
        if not config_path.exists():
            print(f"設定ファイルが見つかりません: {config_path}")
            print("デフォルト設定ファイルを作成します...")

            try:
                self.create_default_config(config_path)
                # 作成後に読み込み
                return self.load_config(config_path)
            except Exception as e:
                return False, None, [f"デフォルト設定ファイル作成エラー: {e}"]
        else:
            return self.load_config(config_path)

    def get_patterns(self) -> List[ConfigPattern]:
        """現在の設定パターンを取得"""
        if self._config is None:
            return []
        return self._config.patterns

    def get_pattern_by_name(self, name: str) -> Optional[ConfigPattern]:
        """名前でパターンを検索"""
        for pattern in self.get_patterns():
            if pattern.name == name:
                return pattern
        return None

    def set_config(self, config: Configuration) -> None:
        """設定オブジェクトを設定"""
        self._config = config
