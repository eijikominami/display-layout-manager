"""
Daemon Manager Module

macOS LaunchAgent を使用した常駐プロセス管理機能を提供するモジュール。
プロセスのライフサイクル管理、plist ファイル生成、状態監視を行う。
"""

import subprocess
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json
import plistlib


@dataclass
class DaemonStatus:
    """常駐プロセスの状態を表すデータクラス"""
    is_installed: bool
    is_running: bool
    is_enabled: bool
    pid: Optional[int] = None
    last_exit_code: Optional[int] = None
    last_exit_time: Optional[str] = None
    plist_path: Optional[Path] = None
    log_path: Optional[Path] = None
    error_log_path: Optional[Path] = None


class DaemonManager:
    """macOS LaunchAgent を使用した常駐プロセス管理クラス"""
    
    def __init__(self, verbose: bool = False):
        """
        初期化
        
        Args:
            verbose: 詳細ログを出力するかどうか
        """
        self.verbose = verbose
        self.label = "com.eijikominami.display-layout-manager"
        self.plist_path = Path.home() / "Library/LaunchAgents" / f"{self.label}.plist"
        self.daemon_config_path = Path.home() / "Library/Application Support/DisplayLayoutManager/daemon.json"
        
        # ログファイルパス
        self.log_dir = Path.home() / "Library/Logs/DisplayLayoutManager"
        self.log_path = self.log_dir / "daemon.log"
        self.error_log_path = self.log_dir / "daemon_error.log"
    
    def install_daemon(self) -> bool:
        """
        LaunchAgent をインストール
        
        Returns:
            bool: インストールに成功した場合 True
        """
        try:
            # plist ファイルが既に存在する場合は停止
            if self.plist_path.exists():
                self.stop_daemon()
                self.unload_daemon()
            
            # 必要なディレクトリを作成
            self._create_required_directories()
            
            # plist ファイルを生成
            if not self._generate_plist_file():
                return False
            
            # LaunchAgent を読み込み
            if not self.load_daemon():
                return False
            
            if self.verbose:
                print(f"LaunchAgent をインストールしました: {self.plist_path}")
            
            return True
            
        except Exception as e:
            print(f"LaunchAgent インストール中にエラー: {e}")
            return False
    
    def uninstall_daemon(self) -> bool:
        """
        LaunchAgent をアンインストール
        
        Returns:
            bool: アンインストールに成功した場合 True
        """
        try:
            # 実行中の場合は停止
            if self.is_daemon_running():
                self.stop_daemon()
            
            # LaunchAgent をアンロード
            self.unload_daemon()
            
            # plist ファイルを削除
            if self.plist_path.exists():
                self.plist_path.unlink()
                if self.verbose:
                    print(f"plist ファイルを削除しました: {self.plist_path}")
            
            return True
            
        except Exception as e:
            print(f"LaunchAgent アンインストール中にエラー: {e}")
            return False
    
    def start_daemon(self) -> bool:
        """
        デーモンを開始
        
        Returns:
            bool: 開始に成功した場合 True
        """
        try:
            if not self.plist_path.exists():
                print("LaunchAgent がインストールされていません")
                return False
            
            # launchctl start を実行
            result = subprocess.run(
                ['launchctl', 'start', self.label],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"デーモンを開始しました: {self.label}")
                return True
            else:
                print(f"デーモン開始に失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"デーモン開始中にエラー: {e}")
            return False
    
    def stop_daemon(self) -> bool:
        """
        デーモンを停止
        
        Returns:
            bool: 停止に成功した場合 True
        """
        try:
            # launchctl stop を実行
            result = subprocess.run(
                ['launchctl', 'stop', self.label],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"デーモンを停止しました: {self.label}")
                return True
            else:
                # 既に停止している場合もあるので、エラーは警告レベル
                if self.verbose:
                    print(f"デーモン停止: {result.stderr}")
                return True
                
        except Exception as e:
            print(f"デーモン停止中にエラー: {e}")
            return False
    
    def load_daemon(self) -> bool:
        """
        LaunchAgent を読み込み（自動起動を有効化）
        
        Returns:
            bool: 読み込みに成功した場合 True
        """
        try:
            if not self.plist_path.exists():
                print("plist ファイルが存在しません")
                return False
            
            # launchctl load を実行
            result = subprocess.run(
                ['launchctl', 'load', str(self.plist_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"LaunchAgent を読み込みました: {self.plist_path}")
                return True
            else:
                print(f"LaunchAgent 読み込みに失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"LaunchAgent 読み込み中にエラー: {e}")
            return False
    
    def unload_daemon(self) -> bool:
        """
        LaunchAgent をアンロード（自動起動を無効化）
        
        Returns:
            bool: アンロードに成功した場合 True
        """
        try:
            # launchctl unload を実行
            result = subprocess.run(
                ['launchctl', 'unload', str(self.plist_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"LaunchAgent をアンロードしました: {self.plist_path}")
                return True
            else:
                # 既にアンロードされている場合もあるので、エラーは警告レベル
                if self.verbose:
                    print(f"LaunchAgent アンロード: {result.stderr}")
                return True
                
        except Exception as e:
            print(f"LaunchAgent アンロード中にエラー: {e}")
            return False
    
    def get_daemon_status(self) -> DaemonStatus:
        """
        デーモンの状態を取得
        
        Returns:
            DaemonStatus: デーモンの現在の状態
        """
        try:
            # plist ファイルの存在確認
            is_installed = self.plist_path.exists()
            
            # launchctl list で実行状態を確認
            is_running = False
            is_enabled = False
            pid = None
            last_exit_code = None
            
            if is_installed:
                result = subprocess.run(
                    ['launchctl', 'list', self.label],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    is_enabled = True
                    # 出力を解析してPIDと終了コードを取得
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if 'PID' in line and 'Status' in line:
                            continue  # ヘッダー行をスキップ
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            try:
                                pid_str = parts[0].strip()
                                if pid_str != '-':
                                    pid = int(pid_str)
                                    is_running = True
                                
                                exit_code_str = parts[1].strip()
                                if exit_code_str != '-':
                                    last_exit_code = int(exit_code_str)
                            except (ValueError, IndexError):
                                pass
            
            return DaemonStatus(
                is_installed=is_installed,
                is_running=is_running,
                is_enabled=is_enabled,
                pid=pid,
                last_exit_code=last_exit_code,
                plist_path=self.plist_path if is_installed else None,
                log_path=self.log_path,
                error_log_path=self.error_log_path
            )
            
        except Exception as e:
            print(f"デーモン状態取得中にエラー: {e}")
            return DaemonStatus(
                is_installed=False,
                is_running=False,
                is_enabled=False
            )
    
    def is_daemon_running(self) -> bool:
        """デーモンが実行中かどうかを確認"""
        status = self.get_daemon_status()
        return status.is_running
    
    def is_daemon_installed(self) -> bool:
        """デーモンがインストールされているかどうかを確認"""
        return self.plist_path.exists()
    
    def _create_required_directories(self) -> None:
        """必要なディレクトリを作成"""
        # LaunchAgents ディレクトリ
        launch_agents_dir = self.plist_path.parent
        launch_agents_dir.mkdir(parents=True, exist_ok=True)
        
        # ログディレクトリ
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 設定ディレクトリ
        config_dir = self.daemon_config_path.parent
        config_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_plist_file(self) -> bool:
        """plist ファイルを生成"""
        try:
            # display-layout-manager の実行ファイルパスを取得
            executable_path = self._find_executable_path()
            if not executable_path:
                print("display-layout-manager の実行ファイルが見つかりません")
                return False
            
            # ユーザー名を取得
            username = os.getenv('USER', 'unknown')
            
            # plist データを作成
            plist_data = {
                'Label': self.label,
                'ProgramArguments': [
                    executable_path,
                    '--daemon'
                ],
                'RunAtLoad': True,
                'KeepAlive': {
                    'SuccessfulExit': False
                },
                'StandardOutPath': str(self.log_path),
                'StandardErrorPath': str(self.error_log_path),
                'WorkingDirectory': str(Path.home()),
                'EnvironmentVariables': {
                    'PATH': '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin',
                    'HOME': str(Path.home())
                },
                'ProcessType': 'Background',
                'LowPriorityIO': True
            }
            
            # plist ファイルに書き込み
            with open(self.plist_path, 'wb') as f:
                plistlib.dump(plist_data, f)
            
            if self.verbose:
                print(f"plist ファイルを生成しました: {self.plist_path}")
            
            return True
            
        except Exception as e:
            print(f"plist ファイル生成中にエラー: {e}")
            return False
    
    def _find_executable_path(self) -> Optional[str]:
        """display-layout-manager の実行ファイルパスを検索"""
        # 検索対象のパス
        search_paths = [
            '/opt/homebrew/bin/display-layout-manager',  # Apple Silicon Mac
            '/usr/local/bin/display-layout-manager',     # Intel Mac
            '~/.local/bin/display-layout-manager',       # pip --user
            '~/bin/display-layout-manager'               # 手動インストール
        ]
        
        for path_str in search_paths:
            path = Path(path_str).expanduser()
            if path.exists() and path.is_file():
                return str(path)
        
        # which コマンドで検索
        try:
            result = subprocess.run(
                ['which', 'display-layout-manager'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        
        return None
    
    def get_log_content(self, lines: int = 50, error_log: bool = False) -> str:
        """
        ログファイルの内容を取得
        
        Args:
            lines: 取得する行数
            error_log: エラーログを取得するかどうか
            
        Returns:
            str: ログファイルの内容
        """
        log_file = self.error_log_path if error_log else self.log_path
        
        if not log_file.exists():
            return "ログファイルが存在しません"
        
        try:
            # tail コマンドを使用して最新の行を取得
            result = subprocess.run(
                ['tail', '-n', str(lines), str(log_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"ログ読み込みエラー: {result.stderr}"
                
        except Exception as e:
            return f"ログ読み込み中にエラー: {e}"
    
    def clear_logs(self) -> bool:
        """
        ログファイルをクリア
        
        Returns:
            bool: クリアに成功した場合 True
        """
        try:
            # ログファイルが存在する場合は空にする
            if self.log_path.exists():
                self.log_path.write_text('')
            
            if self.error_log_path.exists():
                self.error_log_path.write_text('')
            
            if self.verbose:
                print("ログファイルをクリアしました")
            
            return True
            
        except Exception as e:
            print(f"ログクリア中にエラー: {e}")
            return False
    
    def reload_daemon(self) -> bool:
        """
        デーモンをリロード（設定変更を反映）
        
        Returns:
            bool: リロードに成功した場合 True
        """
        try:
            # 一度アンロードしてから再度ロード
            self.unload_daemon()
            return self.load_daemon()
            
        except Exception as e:
            print(f"デーモンリロード中にエラー: {e}")
            return False