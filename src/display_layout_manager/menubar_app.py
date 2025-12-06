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
            "🖥️",  # ディスプレイの絵文字アイコン
            quit_button=None  # カスタム終了ボタンを使用
        )
        
        # コンポーネントの初期化
        self.cli_bridge = CLIBridge(verbose=False)
        self.notification_manager = NotificationManager()
        self.auto_launch_manager = AutoLaunchManager()
        
        self.menu = self._build_menu()
    
    def _build_menu(self):
        """メニュー構造を構築"""
        # 自動起動メニュー項目
        auto_launch_item = rumps.MenuItem(
            "ログイン時に起動",
            callback=self.toggle_auto_launch
        )
        # 現在の状態を反映
        auto_launch_item.state = self.auto_launch_manager.is_enabled()
        
        return [
            rumps.MenuItem("レイアウトを適用", callback=self.apply_layout),
            rumps.MenuItem("現在の設定を保存", callback=self.save_current),
            rumps.separator,
            rumps.MenuItem("接続されたディスプレイ", callback=self.show_displays),
            rumps.separator,
            auto_launch_item,
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
        try:
            if self.auto_launch_manager.is_enabled():
                # 無効化
                self.auto_launch_manager.disable()
                sender.state = False
                self.notification_manager.show_success(
                    "自動起動を無効化しました",
                    "ログイン時に自動起動しなくなります"
                )
            else:
                # 有効化
                self.auto_launch_manager.enable()
                sender.state = True
                self.notification_manager.show_success(
                    "自動起動を有効化しました",
                    "次回ログイン時から自動起動します"
                )
        except Exception as e:
            self.notification_manager.show_error(
                "自動起動の切り替えに失敗しました",
                str(e)
            )
    
    @rumps.clicked("終了")
    def quit_application(self, _):
        """アプリケーション終了アクション"""
        rumps.quit_application()
