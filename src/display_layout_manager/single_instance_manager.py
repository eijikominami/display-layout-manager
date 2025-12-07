"""
Display Layout Manager - Single Instance Manager

メニューバーアプリの重複起動を防止する機能
"""

import os
from pathlib import Path


class SingleInstanceManager:
    """単一インスタンス管理クラス

    PIDファイルを使用してメニューバーアプリの重複起動を防止します。
    """

    def __init__(self):
        """初期化"""
        self.pid_file = (
            Path.home()
            / "Library"
            / "Application Support"
            / "DisplayLayoutManager"
            / "menubar.pid"
        )
        # ディレクトリが存在しない場合は作成
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)

    def is_already_running(self) -> bool:
        """既に起動しているかチェック

        Returns:
            bool: 既に起動している場合はTrue、そうでない場合はFalse
        """
        if not self.pid_file.exists():
            return False

        try:
            # PIDファイルからプロセスIDを読み込む
            with open(self.pid_file, "r") as f:
                pid = int(f.read().strip())

            # プロセスが実際に動作しているかチェック
            # シグナル0は存在確認のみ（プロセスを終了させない）
            os.kill(pid, 0)
            return True
        except (ValueError, ProcessLookupError, PermissionError, OSError):
            # PIDファイルが無効、またはプロセスが存在しない
            return False

    def acquire_lock(self) -> bool:
        """ロックを取得（PIDファイルを作成）

        Returns:
            bool: ロック取得に成功した場合はTrue、失敗した場合はFalse
        """
        if self.is_already_running():
            return False

        try:
            # 現在のプロセスIDを書き込む
            with open(self.pid_file, "w") as f:
                f.write(str(os.getpid()))

            # ファイル権限を600に設定（所有者のみ読み書き可能）
            os.chmod(self.pid_file, 0o600)

            return True
        except Exception:
            return False

    def release_lock(self):
        """ロックを解放（PIDファイルを削除）"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
        except Exception:
            # エラーは無視（ファイルが既に削除されている等）
            pass

    def bring_existing_to_front(self):
        """既存のインスタンスを前面に表示

        NSRunningApplication APIを使用して、既存のメニューバーアプリを
        アクティブ化します。
        """
        try:
            from AppKit import (
                NSApplicationActivateIgnoringOtherApps,
                NSRunningApplication,
            )

            # バンドル識別子で実行中のアプリケーションを取得
            bundle_id = "com.eijikominami.display-layout-manager"
            running_apps = (
                NSRunningApplication.runningApplicationsWithBundleIdentifier_(bundle_id)
            )

            if running_apps:
                # 最初に見つかったインスタンスをアクティブ化
                app = running_apps[0]
                app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
        except Exception:
            # エラーは無視（既存インスタンスが見つからない場合等）
            pass
