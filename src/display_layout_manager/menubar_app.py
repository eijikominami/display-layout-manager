"""
Display Layout Manager - Menu Bar Application

macOS メニューバーアプリケーションの実装
"""

import rumps
from .cli_bridge import CLIBridge
from .notification_manager import NotificationManager
from .auto_launch_manager import AutoLaunchManager


class DisplayLayoutMenuBar(rumps.App):
    """Display Layout Manager メニューバーアプリケーション"""
    
    def __init__(self):
        super(DisplayLayoutMenuBar, self).__init__(
            "Display Layout Manager",
            icon=None,  # TODO: アイコンを追加
            quit_button=None  # カスタム終了ボタンを使用
        )
        
        # コンポーネントの初期化
        self.cli_bridge = CLIBridge(verbose=False)
        self.notification_manager = NotificationManager()
        self.auto_launch_manager = AutoLaunchManager()
        
        self.menu = self._build_menu()
    
    def _build_menu(self):
        """メニュー構造を構築"""
        return [
            rumps.MenuItem("レイアウトを適用", callback=self.apply_layout),
            rumps.MenuItem("現在の設定を保存", callback=self.save_current),
            rumps.separator,
            rumps.MenuItem("接続されたディスプレイ", callback=self.show_displays),
            rumps.separator,
            rumps.MenuItem("ログイン時に起動", callback=self.toggle_auto_launch),
            rumps.separator,
            rumps.MenuItem("終了", callback=self.quit_application)
        ]
    
    @rumps.clicked("レイアウトを適用")
    def apply_layout(self, _):
        """レイアウト適用アクション"""
        try:
            result = self.cli_bridge.execute_apply_layout()
            
            if result.success:
                self.notification_manager.show_success(
                    "レイアウトを適用しました",
                    f"パターン: {result.pattern_name}"
                )
            else:
                self.notification_manager.show_error(
                    "レイアウト適用に失敗しました",
                    result.error_message or "不明なエラー"
                )
        except Exception as e:
            self.notification_manager.show_error(
                "エラーが発生しました",
                str(e)
            )
    
    @rumps.clicked("現在の設定を保存")
    def save_current(self, _):
        """現在の設定保存アクション"""
        try:
            result = self.cli_bridge.execute_save_current()
            
            if result.success:
                self.notification_manager.show_success(
                    "設定を保存しました",
                    f"パターン: {result.pattern_name}"
                )
            else:
                self.notification_manager.show_error(
                    "設定保存に失敗しました",
                    result.error_message or "不明なエラー"
                )
        except Exception as e:
            self.notification_manager.show_error(
                "エラーが発生しました",
                str(e)
            )
    
    @rumps.clicked("接続されたディスプレイ")
    def show_displays(self, _):
        """接続されたディスプレイ表示アクション"""
        try:
            result = self.cli_bridge.get_current_displays()
            
            if result.success:
                self.notification_manager.show_info(
                    "接続されたディスプレイ",
                    result.details or "情報なし"
                )
            else:
                self.notification_manager.show_error(
                    "ディスプレイ情報の取得に失敗しました",
                    result.error_message or "不明なエラー"
                )
        except Exception as e:
            self.notification_manager.show_error(
                "エラーが発生しました",
                str(e)
            )
    
    @rumps.clicked("ログイン時に起動")
    def toggle_auto_launch(self, sender):
        """自動起動の切り替えアクション"""
        # TODO: タスク 17 で実装
        rumps.notification(
            title="Display Layout Manager",
            subtitle="自動起動",
            message="この機能は実装中です"
        )
    
    @rumps.clicked("終了")
    def quit_application(self, _):
        """アプリケーション終了アクション"""
        rumps.quit_application()
