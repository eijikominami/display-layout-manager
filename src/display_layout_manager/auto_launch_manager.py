"""
Display Layout Manager - Auto Launch Manager

ログイン時の自動起動管理
"""

import os
import subprocess
import plistlib
from pathlib import Path


class AutoLaunchManager:
    """ログイン時の自動起動管理クラス"""
    
    def __init__(self):
        self.launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
        self.plist_path = self.launch_agents_dir / "com.eijikominami.display-layout-manager.plist"
    
    def is_enabled(self) -> bool:
        """自動起動が有効かチェック"""
        return self.plist_path.exists()
    
    def enable(self):
        """自動起動を有効化"""
        # TODO: タスク 17 で完全実装
        print("自動起動の有効化機能は実装中です")
    
    def disable(self):
        """自動起動を無効化"""
        # TODO: タスク 17 で完全実装
        print("自動起動の無効化機能は実装中です")
