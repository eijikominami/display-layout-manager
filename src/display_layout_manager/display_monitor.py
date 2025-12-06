"""
Display Monitor Module

macOS のディスプレイ変更イベントを監視するモジュール。
NSApplication.didChangeScreenParametersNotification を使用して
ディスプレイの追加/削除、ミラーリング/拡張モードの切り替えを検知する。
"""

import threading
import time
from datetime import datetime
from typing import Callable, List, Optional
from dataclasses import dataclass
import subprocess
import re

try:
    import objc
    from Foundation import NSNotificationCenter, NSApplication
    from AppKit import NSScreen
    OBJC_AVAILABLE = True
except ImportError:
    OBJC_AVAILABLE = False


@dataclass
class DisplayChangeEvent:
    """ディスプレイ変更イベントを表すデータクラス"""
    event_type: str  # "added", "removed", "configuration_changed"
    timestamp: datetime
    screen_count: int
    screen_ids: List[str]
    previous_screen_count: Optional[int] = None
    previous_screen_ids: Optional[List[str]] = None


class DisplayMonitor:
    """macOS ディスプレイ変更イベントの監視クラス"""
    
    def __init__(self, callback: Callable[[DisplayChangeEvent], None]):
        """
        初期化
        
        Args:
            callback: ディスプレイ変更イベント発生時に呼び出されるコールバック関数
        """
        self.callback = callback
        self.is_monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._current_screen_ids: List[str] = []
        self._current_screen_count = 0
        
        # 初期状態を取得
        self._update_current_state()
    
    def start_monitoring(self) -> bool:
        """
        ディスプレイ変更の監視を開始
        
        Returns:
            bool: 監視開始に成功した場合 True
        """
        if self.is_monitoring:
            return True
            
        if OBJC_AVAILABLE:
            return self._start_objc_monitoring()
        else:
            return self._start_polling_monitoring()
    
    def stop_monitoring(self) -> None:
        """監視を停止"""
        if not self.is_monitoring:
            return
            
        self.is_monitoring = False
        self._stop_event.set()
        
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5.0)
    
    def _start_objc_monitoring(self) -> bool:
        """PyObjC を使用した監視を開始"""
        try:
            # NSApplication の通知センターに登録
            notification_center = NSNotificationCenter.defaultCenter()
            notification_center.addObserver_selector_name_object_(
                self,
                objc.selector(self._on_display_change_objc, signature=b'v@:@'),
                "NSApplicationDidChangeScreenParametersNotification",
                None
            )
            
            self.is_monitoring = True
            return True
            
        except Exception as e:
            print(f"PyObjC 監視の開始に失敗: {e}")
            return False
    
    def _start_polling_monitoring(self) -> bool:
        """ポーリングベースの監視を開始（PyObjC が利用できない場合）"""
        try:
            self._monitor_thread = threading.Thread(
                target=self._polling_monitor_loop,
                daemon=True
            )
            self._monitor_thread.start()
            self.is_monitoring = True
            return True
            
        except Exception as e:
            print(f"ポーリング監視の開始に失敗: {e}")
            return False
    
    def _on_display_change_objc(self, notification) -> None:
        """PyObjC からの通知ハンドラ"""
        try:
            self._handle_display_change()
        except Exception as e:
            print(f"ディスプレイ変更通知の処理中にエラー: {e}")
    
    def _polling_monitor_loop(self) -> None:
        """ポーリングベースの監視ループ"""
        while not self._stop_event.is_set():
            try:
                self._check_display_changes()
                time.sleep(1.0)  # 1秒間隔でチェック
            except Exception as e:
                print(f"ポーリング監視中にエラー: {e}")
                time.sleep(5.0)  # エラー時は5秒待機
    
    def _check_display_changes(self) -> None:
        """ディスプレイ変更をチェック"""
        previous_screen_ids = self._current_screen_ids.copy()
        previous_screen_count = self._current_screen_count
        
        self._update_current_state()
        
        # 変更があった場合のみイベントを発生
        if (self._current_screen_ids != previous_screen_ids or 
            self._current_screen_count != previous_screen_count):
            self._handle_display_change(previous_screen_ids, previous_screen_count)
    
    def _handle_display_change(self, 
                              previous_screen_ids: Optional[List[str]] = None,
                              previous_screen_count: Optional[int] = None) -> None:
        """ディスプレイ変更イベントを処理"""
        if previous_screen_ids is None:
            previous_screen_ids = self._current_screen_ids.copy()
            previous_screen_count = self._current_screen_count
        
        # 現在の状態を更新
        self._update_current_state()
        
        # イベントタイプを判定
        event_type = self._determine_event_type(
            previous_screen_ids, 
            self._current_screen_ids,
            previous_screen_count,
            self._current_screen_count
        )
        
        # イベントを作成
        event = DisplayChangeEvent(
            event_type=event_type,
            timestamp=datetime.now(),
            screen_count=self._current_screen_count,
            screen_ids=self._current_screen_ids.copy(),
            previous_screen_count=previous_screen_count,
            previous_screen_ids=previous_screen_ids.copy() if previous_screen_ids else None
        )
        
        # コールバックを呼び出し
        try:
            self.callback(event)
        except Exception as e:
            print(f"ディスプレイ変更コールバック実行中にエラー: {e}")
    
    def _update_current_state(self) -> None:
        """現在のディスプレイ状態を更新"""
        try:
            screen_ids = self._get_current_screen_ids()
            self._current_screen_ids = screen_ids
            self._current_screen_count = len(screen_ids)
        except Exception as e:
            print(f"ディスプレイ状態の更新中にエラー: {e}")
    
    def _get_current_screen_ids(self) -> List[str]:
        """現在のディスプレイの Screen ID を取得"""
        try:
            # displayplacer list コマンドを実行
            result = subprocess.run(
                ['displayplacer', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"displayplacer list コマンドが失敗: {result.stderr}")
                return []
            
            # Persistent screen id を抽出
            screen_ids = []
            pattern = r'Persistent screen id: ([A-F0-9-]+)'
            matches = re.findall(pattern, result.stdout)
            
            for match in matches:
                screen_ids.append(match)
            
            return screen_ids
            
        except subprocess.TimeoutExpired:
            print("displayplacer list コマンドがタイムアウト")
            return []
        except FileNotFoundError:
            print("displayplacer コマンドが見つかりません")
            return []
        except Exception as e:
            print(f"Screen ID 取得中にエラー: {e}")
            return []
    
    def _determine_event_type(self, 
                             previous_ids: List[str], 
                             current_ids: List[str],
                             previous_count: int,
                             current_count: int) -> str:
        """イベントタイプを判定"""
        if current_count > previous_count:
            return "added"
        elif current_count < previous_count:
            return "removed"
        elif set(current_ids) != set(previous_ids):
            return "configuration_changed"
        else:
            return "configuration_changed"  # 同じディスプレイでも設定が変更された可能性
    
    def get_current_displays(self) -> List[str]:
        """現在のディスプレイ一覧を取得"""
        return self._current_screen_ids.copy()
    
    def get_current_display_count(self) -> int:
        """現在のディスプレイ数を取得"""
        return self._current_screen_count


# PyObjC が利用できない場合のダミー実装
if not OBJC_AVAILABLE:
    print("警告: PyObjC が利用できません。ポーリングベースの監視を使用します。")