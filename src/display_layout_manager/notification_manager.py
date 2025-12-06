"""
Display Layout Manager - Notification Manager

macOS 通知センターとの連携
"""

import subprocess


class NotificationManager:
    """macOS 通知管理クラス"""
    
    def show_success(self, title: str, message: str):
        """
        成功通知を表示
        
        Args:
            title: 通知タイトル
            message: 通知メッセージ
        """
        self._show_notification(title, message, sound="Glass")
    
    def show_error(self, title: str, message: str):
        """
        エラー通知を表示
        
        Args:
            title: 通知タイトル
            message: 通知メッセージ
        """
        self._show_notification(title, message, sound="Basso")
    
    def show_info(self, title: str, message: str):
        """
        情報通知を表示
        
        Args:
            title: 通知タイトル
            message: 通知メッセージ
        """
        self._show_notification(title, message, sound="default")
    
    def _show_notification(self, title: str, message: str, sound: str = "default"):
        """
        macOS 通知センターに通知を表示
        
        Args:
            title: 通知タイトル
            message: 通知メッセージ
            sound: 通知音（Glass, Basso, default等）
        """
        try:
            # メッセージ内の特殊文字をエスケープ
            escaped_message = message.replace('"', '\\"').replace("'", "\\'")
            escaped_title = title.replace('"', '\\"').replace("'", "\\'")
            
            script = f'''
            display notification "{escaped_message}" with title "{escaped_title}" sound name "{sound}"
            '''
            subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=5
            )
        except Exception as e:
            # 通知の失敗は致命的ではないので、エラーを無視
            print(f"通知の表示に失敗しました: {e}")
