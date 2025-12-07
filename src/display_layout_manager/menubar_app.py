"""
Display Layout Manager - Menu Bar Application

macOS メニューバーアプリケーションの実装
"""

import rumps

from .auto_launch_manager import AutoLaunchManager
from .cli_bridge import CLIBridge
from .i18n import LocaleDetector, MessageManager


class DisplayLayoutMenuBar(rumps.App):
    """Display Layout Manager メニューバーアプリケーション"""

    def __init__(self):
        # Initialize i18n first
        self.locale_detector = LocaleDetector()
        self.msg = MessageManager(self.locale_detector)

        super(DisplayLayoutMenuBar, self).__init__(
            "Display Layout Manager",  # Application name
            title="⧈",  # Menu bar icon (U+29C8 SQUARED SQUARE)
            quit_button=None,  # カスタム終了ボタンを使用
        )

        # コンポーネントの初期化
        self.cli_bridge = CLIBridge(verbose=False)
        self.auto_launch_manager = AutoLaunchManager()

        self.menu = self._build_menu()

        # 初期状態を反映
        self._update_auto_launch_state()

    def _build_menu(self):
        """メニュー構造を構築"""
        return [
            rumps.MenuItem(
                self.msg.get("menu_apply_layout"), callback=self.apply_layout
            ),
            rumps.MenuItem(
                self.msg.get("menu_save_current"), callback=self.save_current
            ),
            rumps.separator,
            rumps.MenuItem(
                self.msg.get("menu_auto_launch"), callback=self.toggle_auto_launch
            ),
            rumps.separator,
            rumps.MenuItem(self.msg.get("menu_quit"), callback=self.quit_application),
        ]

    def _update_auto_launch_state(self):
        """自動起動メニュー項目の状態を更新"""
        is_enabled = self.auto_launch_manager.is_enabled()
        menu_item = self.menu[self.msg.get("menu_auto_launch")]
        if menu_item:
            menu_item.state = 1 if is_enabled else 0

    def apply_layout(self, _):
        """レイアウト適用アクション（サイレント実行）"""
        try:
            self.cli_bridge.execute_apply_layout()
            # 通知は表示しない（ログファイルに記録される）
        except Exception:
            # エラー時もサイレント（ログファイルに記録される）
            pass

    def save_current(self, _):
        """現在の設定保存アクション（サイレント実行）"""
        try:
            self.cli_bridge.execute_save_current()
            # 通知は表示しない（ログファイルに記録される）
        except Exception:
            # エラー時もサイレント（ログファイルに記録される）
            pass

    def toggle_auto_launch(self, sender):
        """自動起動の切り替えアクション"""
        try:
            if self.auto_launch_manager.is_enabled():
                # 無効化
                self.auto_launch_manager.disable()
                sender.state = 0
            else:
                # 有効化
                self.auto_launch_manager.enable()
                sender.state = 1
            # 通知は表示しない（チェックマークで状態を表示）
        except Exception:
            # エラー時もサイレント（ログファイルに記録される）
            pass

    def quit_application(self, _):
        """アプリケーション終了アクション"""
        rumps.quit_application()
