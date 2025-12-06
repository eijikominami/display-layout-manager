"""
Configuration Watcher Module

設定ファイルの変更監視と動的リロード機能を提供するモジュール。
ファイルシステムの変更を監視し、設定の動的リロードを実現する。
"""

import threading
import time
import json
from pathlib import Path
from typing import Callable, Dict, Any, Optional
from datetime import datetime
import os
import stat


class ConfigurationWatcher:
    """設定ファイルの変更監視と動的リロード機能を提供するクラス"""
    
    def __init__(self, 
                 config_path: Path, 
                 callback: Callable[[Dict[str, Any]], None],
                 check_interval: float = 1.0):
        """
        初期化
        
        Args:
            config_path: 監視する設定ファイルのパス
            callback: 設定変更時に呼び出されるコールバック関数
            check_interval: ファイル変更チェック間隔（秒）
        """
        self.config_path = config_path
        self.callback = callback
        self.check_interval = check_interval
        
        self._is_watching = False
        self._watch_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # ファイル状態の追跡
        self._last_modified_time: Optional[float] = None
        self._last_size: Optional[int] = None
        self._last_config: Optional[Dict[str, Any]] = None
        
        # 初期状態を記録
        self._update_file_state()
    
    def start_watching(self) -> bool:
        """
        設定ファイルの監視を開始
        
        Returns:
            bool: 監視開始に成功した場合 True
        """
        if self._is_watching:
            return True
        
        try:
            self._stop_event.clear()
            self._watch_thread = threading.Thread(
                target=self._watch_loop,
                daemon=True
            )
            self._watch_thread.start()
            self._is_watching = True
            
            print(f"設定ファイル監視を開始: {self.config_path}")
            return True
            
        except Exception as e:
            print(f"設定ファイル監視開始中にエラー: {e}")
            return False
    
    def stop_watching(self) -> None:
        """監視を停止"""
        if not self._is_watching:
            return
        
        self._is_watching = False
        self._stop_event.set()
        
        if self._watch_thread and self._watch_thread.is_alive():
            self._watch_thread.join(timeout=5.0)
        
        print(f"設定ファイル監視を停止: {self.config_path}")
    
    def _watch_loop(self) -> None:
        """監視ループ"""
        while not self._stop_event.is_set():
            try:
                self._check_file_changes()
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"設定ファイル監視中にエラー: {e}")
                time.sleep(5.0)  # エラー時は長めに待機
    
    def _check_file_changes(self) -> None:
        """ファイル変更をチェック"""
        if not self.config_path.exists():
            # ファイルが削除された場合
            if self._last_modified_time is not None:
                print(f"設定ファイルが削除されました: {self.config_path}")
                self._last_modified_time = None
                self._last_size = None
                self._last_config = None
            return
        
        try:
            # ファイル統計情報を取得
            file_stat = self.config_path.stat()
            current_modified_time = file_stat.st_mtime
            current_size = file_stat.st_size
            
            # 変更があったかチェック
            if (self._last_modified_time != current_modified_time or 
                self._last_size != current_size):
                
                print(f"設定ファイルの変更を検知: {self.config_path}")
                self._handle_file_change()
                
                # 状態を更新
                self._last_modified_time = current_modified_time
                self._last_size = current_size
                
        except Exception as e:
            print(f"ファイル変更チェック中にエラー: {e}")
    
    def _handle_file_change(self) -> None:
        """ファイル変更を処理"""
        try:
            # 設定ファイルを読み込み
            new_config = self._load_config_file()
            
            if new_config is None:
                print("設定ファイルの読み込みに失敗")
                return
            
            # 設定が実際に変更されたかチェック
            if new_config != self._last_config:
                print("設定内容の変更を確認、コールバックを実行")
                
                # コールバックを呼び出し
                try:
                    self.callback(new_config)
                    self._last_config = new_config
                except Exception as e:
                    print(f"設定変更コールバック実行中にエラー: {e}")
            else:
                print("設定内容に変更はありません")
                
        except Exception as e:
            print(f"ファイル変更処理中にエラー: {e}")
    
    def _load_config_file(self) -> Optional[Dict[str, Any]]:
        """設定ファイルを読み込み"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"設定ファイルのJSON構文エラー: {e}")
            return None
        except Exception as e:
            print(f"設定ファイル読み込み中にエラー: {e}")
            return None
    
    def _update_file_state(self) -> None:
        """ファイル状態を更新"""
        if not self.config_path.exists():
            self._last_modified_time = None
            self._last_size = None
            self._last_config = None
            return
        
        try:
            file_stat = self.config_path.stat()
            self._last_modified_time = file_stat.st_mtime
            self._last_size = file_stat.st_size
            self._last_config = self._load_config_file()
        except Exception as e:
            print(f"ファイル状態更新中にエラー: {e}")
    
    def get_current_config(self) -> Optional[Dict[str, Any]]:
        """現在の設定を取得"""
        return self._last_config.copy() if self._last_config else None
    
    def is_watching(self) -> bool:
        """監視中かどうかを確認"""
        return self._is_watching
    
    def force_reload(self) -> bool:
        """強制的に設定をリロード"""
        try:
            new_config = self._load_config_file()
            if new_config is not None:
                self.callback(new_config)
                self._last_config = new_config
                self._update_file_state()
                return True
            return False
        except Exception as e:
            print(f"強制リロード中にエラー: {e}")
            return False


class DaemonConfigManager:
    """常駐機能専用の設定管理クラス"""
    
    def __init__(self, verbose: bool = False):
        """
        初期化
        
        Args:
            verbose: 詳細ログを出力するかどうか
        """
        self.verbose = verbose
        self.config_path = Path.home() / "Library/Application Support/DisplayLayoutManager/daemon.json"
        self._current_config: Optional[Dict[str, Any]] = None
        self._config_watcher: Optional[ConfigurationWatcher] = None
        
        # 設定変更コールバックのリスト
        self._change_callbacks: list[Callable[[Dict[str, Any]], None]] = []
    
    def load_config(self) -> Dict[str, Any]:
        """
        常駐設定を読み込み
        
        Returns:
            Dict[str, Any]: 設定データ
        """
        if not self.config_path.exists():
            # デフォルト設定を作成
            default_config = self._create_default_config()
            self._save_config(default_config)
            return default_config
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # 設定を検証
            if self._validate_config(config):
                self._current_config = config
                return config
            else:
                print("設定ファイルが無効です。デフォルト設定を使用します。")
                return self._create_default_config()
                
        except json.JSONDecodeError as e:
            print(f"設定ファイルのJSON構文エラー: {e}")
            return self._create_default_config()
        except Exception as e:
            print(f"設定ファイル読み込み中にエラー: {e}")
            return self._create_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        設定を保存
        
        Args:
            config: 保存する設定データ
            
        Returns:
            bool: 保存に成功した場合 True
        """
        if not self._validate_config(config):
            print("無効な設定データです")
            return False
        
        return self._save_config(config)
    
    def start_watching(self) -> bool:
        """設定ファイルの監視を開始"""
        if self._config_watcher:
            return True
        
        def on_config_change(new_config: Dict[str, Any]):
            if self._validate_config(new_config):
                self._current_config = new_config
                # 登録されたコールバックを呼び出し
                for callback in self._change_callbacks:
                    try:
                        callback(new_config)
                    except Exception as e:
                        print(f"設定変更コールバック実行中にエラー: {e}")
            else:
                print("変更された設定が無効です")
        
        self._config_watcher = ConfigurationWatcher(
            config_path=self.config_path,
            callback=on_config_change,
            check_interval=1.0
        )
        
        return self._config_watcher.start_watching()
    
    def stop_watching(self) -> None:
        """設定ファイルの監視を停止"""
        if self._config_watcher:
            self._config_watcher.stop_watching()
            self._config_watcher = None
    
    def add_change_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """設定変更時のコールバックを追加"""
        self._change_callbacks.append(callback)
    
    def remove_change_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """設定変更時のコールバックを削除"""
        if callback in self._change_callbacks:
            self._change_callbacks.remove(callback)
    
    def get_current_config(self) -> Optional[Dict[str, Any]]:
        """現在の設定を取得"""
        return self._current_config.copy() if self._current_config else None
    
    def _create_default_config(self) -> Dict[str, Any]:
        """デフォルト設定を作成"""
        return {
            "version": "1.0",
            "daemon": {
                "enabled": True,
                "debounce_delay": 2.0,
                "log_level": "INFO",
                "max_execution_time": 30,
                "auto_execute": True,
                "excluded_events": [],
                "notification": {
                    "enabled": False,
                    "success": True,
                    "failure": True
                }
            },
            "monitoring": {
                "display_changes": True,
                "configuration_changes": True,
                "check_interval": 1.0
            },
            "execution": {
                "command_timeout": 30,
                "retry_count": 2,
                "retry_delay": 5.0,
                "dry_run": False
            },
            "logging": {
                "file_path": "~/Library/Logs/DisplayLayoutManager/daemon.log",
                "max_file_size": "10MB",
                "backup_count": 5,
                "format": "json"
            }
        }
    
    def _save_config(self, config: Dict[str, Any]) -> bool:
        """設定をファイルに保存"""
        try:
            # 設定ディレクトリを作成
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 設定ファイルに書き込み
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # ファイル権限を設定（所有者のみ読み書き可能）
            os.chmod(self.config_path, stat.S_IRUSR | stat.S_IWUSR)
            
            if self.verbose:
                print(f"設定を保存しました: {self.config_path}")
            
            return True
            
        except Exception as e:
            print(f"設定保存中にエラー: {e}")
            return False
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """設定データを検証"""
        try:
            # 必須フィールドの確認
            required_fields = ['version', 'daemon', 'monitoring', 'execution', 'logging']
            for field in required_fields:
                if field not in config:
                    print(f"必須フィールドが不足: {field}")
                    return False
            
            # daemon セクションの検証
            daemon_config = config.get('daemon', {})
            if not isinstance(daemon_config.get('debounce_delay'), (int, float)):
                print("daemon.debounce_delay は数値である必要があります")
                return False
            
            if daemon_config.get('debounce_delay', 0) < 0:
                print("daemon.debounce_delay は0以上である必要があります")
                return False
            
            # その他の基本的な検証
            return True
            
        except Exception as e:
            print(f"設定検証中にエラー: {e}")
            return False