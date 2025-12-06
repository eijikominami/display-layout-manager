"""
Display Layout Manager - Auto Launch Manager

ログイン時の自動起動管理
"""

import os
import subprocess
import plistlib
import shutil
from pathlib import Path


class AutoLaunchManager:
    """ログイン時の自動起動管理クラス"""
    
    def __init__(self):
        self.launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
        self.plist_path = self.launch_agents_dir / "com.eijikominami.display-layout-manager.plist"
    
    def is_enabled(self) -> bool:
        """
        自動起動が有効かチェック
        
        Returns:
            bool: 自動起動が有効な場合 True
        """
        return self.plist_path.exists()
    
    def enable(self):
        """
        自動起動を有効化
        
        Raises:
            Exception: 有効化に失敗した場合
        """
        try:
            # LaunchAgents ディレクトリを作成
            self.launch_agents_dir.mkdir(parents=True, exist_ok=True)
            
            # 実行ファイルのパスを取得
            executable_path = self._find_executable()
            if not executable_path:
                raise Exception("display-layout-manager-menubar が見つかりません")
            
            # plist ファイルを作成
            plist_data = {
                "Label": "com.eijikominami.display-layout-manager",
                "ProgramArguments": [executable_path],
                "RunAtLoad": True,
                "KeepAlive": False,
                "StandardOutPath": str(Path.home() / "Library" / "Logs" / "DisplayLayoutManager" / "menubar.log"),
                "StandardErrorPath": str(Path.home() / "Library" / "Logs" / "DisplayLayoutManager" / "menubar-error.log"),
            }
            
            # plist ファイルを書き込み
            with open(self.plist_path, 'wb') as f:
                plistlib.dump(plist_data, f)
            
            # ファイル権限を設定
            os.chmod(self.plist_path, 0o644)
            
            # launchctl に登録
            subprocess.run(
                ["launchctl", "load", str(self.plist_path)],
                check=True,
                capture_output=True,
                text=True
            )
            
            print(f"✓ 自動起動を有効化しました: {self.plist_path}")
        
        except subprocess.CalledProcessError as e:
            raise Exception(f"launchctl の実行に失敗しました: {e.stderr}")
        except Exception as e:
            raise Exception(f"自動起動の有効化に失敗しました: {e}")
    
    def disable(self):
        """
        自動起動を無効化
        
        Raises:
            Exception: 無効化に失敗した場合
        """
        try:
            if not self.plist_path.exists():
                print("自動起動は既に無効化されています")
                return
            
            # launchctl から削除
            try:
                subprocess.run(
                    ["launchctl", "unload", str(self.plist_path)],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError:
                # unload が失敗しても続行（既に unload されている可能性）
                pass
            
            # plist ファイルを削除
            self.plist_path.unlink()
            
            print(f"✓ 自動起動を無効化しました: {self.plist_path}")
        
        except Exception as e:
            raise Exception(f"自動起動の無効化に失敗しました: {e}")
    
    def _find_executable(self) -> str:
        """
        display-layout-manager-menubar の実行ファイルパスを検索
        
        Returns:
            str: 実行ファイルのパス
        """
        # 検索パス
        search_paths = [
            "/opt/homebrew/bin/display-layout-manager-menubar",  # Apple Silicon
            "/usr/local/bin/display-layout-manager-menubar",     # Intel Mac
            str(Path.home() / ".local" / "bin" / "display-layout-manager-menubar"),  # pip --user
        ]
        
        # which コマンドで検索
        try:
            result = subprocess.run(
                ["which", "display-layout-manager-menubar"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            pass
        
        # 検索パスから探す
        for path in search_paths:
            if Path(path).exists():
                return path
        
        return ""
