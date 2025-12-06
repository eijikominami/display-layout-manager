"""
Event Processor Module

ディスプレイ変更イベントの処理とデバウンス機能を提供するモジュール。
連続するイベントを統合し、適切なタイミングでコマンド実行をトリガーする。
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Callable, List, Optional, Dict, Any
from dataclasses import dataclass, field
from .display_monitor import DisplayChangeEvent


@dataclass
class ProcessedEvent:
    """処理済みイベントを表すデータクラス"""
    original_events: List[DisplayChangeEvent]
    final_event_type: str
    timestamp: datetime
    screen_count: int
    screen_ids: List[str]
    debounce_duration: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class EventProcessor:
    """ディスプレイ変更イベントの処理とデバウンス機能を提供するクラス"""
    
    def __init__(self, 
                 callback: Callable[[ProcessedEvent], None],
                 debounce_delay: float = 2.0,
                 max_events_in_queue: int = 100):
        """
        初期化
        
        Args:
            callback: 処理済みイベント発生時に呼び出されるコールバック関数
            debounce_delay: デバウンス遅延時間（秒）
            max_events_in_queue: キューに保持する最大イベント数
        """
        self.callback = callback
        self.debounce_delay = debounce_delay
        self.max_events_in_queue = max_events_in_queue
        
        self._pending_events: List[DisplayChangeEvent] = []
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()
        self._is_processing = False
        
        # 統計情報
        self._stats = {
            'total_events_received': 0,
            'total_events_processed': 0,
            'total_debounced_groups': 0,
            'last_processed_time': None
        }
    
    def process_event(self, event: DisplayChangeEvent) -> None:
        """
        イベントを処理（デバウンス付き）
        
        Args:
            event: 処理するディスプレイ変更イベント
        """
        with self._lock:
            self._stats['total_events_received'] += 1
            
            # キューサイズ制限
            if len(self._pending_events) >= self.max_events_in_queue:
                # 古いイベントを削除
                self._pending_events = self._pending_events[-(self.max_events_in_queue // 2):]
                print(f"警告: イベントキューが満杯のため、古いイベントを削除しました")
            
            # イベントをキューに追加
            self._pending_events.append(event)
            
            # 既存のタイマーをキャンセル
            if self._timer:
                self._timer.cancel()
            
            # 新しいタイマーを開始
            self._timer = threading.Timer(
                self.debounce_delay,
                self._execute_delayed_processing
            )
            self._timer.start()
    
    def _execute_delayed_processing(self) -> None:
        """遅延実行される実際の処理"""
        with self._lock:
            if not self._pending_events:
                return
            
            if self._is_processing:
                return
            
            self._is_processing = True
            
            try:
                # 保留中のイベントをコピーしてクリア
                events_to_process = self._pending_events.copy()
                self._pending_events.clear()
                
                # 処理済みイベントを作成
                processed_event = self._create_processed_event(events_to_process)
                
                # 統計情報を更新
                self._stats['total_events_processed'] += len(events_to_process)
                self._stats['total_debounced_groups'] += 1
                self._stats['last_processed_time'] = datetime.now()
                
                # コールバックを呼び出し
                try:
                    self.callback(processed_event)
                except Exception as e:
                    print(f"イベント処理コールバック実行中にエラー: {e}")
                    
            except Exception as e:
                print(f"遅延処理実行中にエラー: {e}")
            finally:
                self._is_processing = False
    
    def _create_processed_event(self, events: List[DisplayChangeEvent]) -> ProcessedEvent:
        """複数のイベントから処理済みイベントを作成"""
        if not events:
            raise ValueError("イベントリストが空です")
        
        # 最新のイベントを基準とする
        latest_event = events[-1]
        
        # 最終的なイベントタイプを決定
        final_event_type = self._determine_final_event_type(events)
        
        # メタデータを作成
        metadata = {
            'original_event_count': len(events),
            'event_types': [e.event_type for e in events],
            'time_span': (events[-1].timestamp - events[0].timestamp).total_seconds(),
            'first_event_time': events[0].timestamp.isoformat(),
            'last_event_time': events[-1].timestamp.isoformat()
        }
        
        # 処理済みイベントを作成
        processed_event = ProcessedEvent(
            original_events=events,
            final_event_type=final_event_type,
            timestamp=latest_event.timestamp,
            screen_count=latest_event.screen_count,
            screen_ids=latest_event.screen_ids,
            debounce_duration=self.debounce_delay,
            metadata=metadata
        )
        
        return processed_event
    
    def _determine_final_event_type(self, events: List[DisplayChangeEvent]) -> str:
        """複数のイベントから最終的なイベントタイプを決定"""
        if not events:
            return "unknown"
        
        if len(events) == 1:
            return events[0].event_type
        
        # 複数のイベントがある場合の判定ロジック
        event_types = [e.event_type for e in events]
        
        # 追加と削除が混在している場合
        if "added" in event_types and "removed" in event_types:
            # 最終的なディスプレイ数で判定
            first_count = events[0].previous_screen_count or events[0].screen_count
            last_count = events[-1].screen_count
            
            if last_count > first_count:
                return "added"
            elif last_count < first_count:
                return "removed"
            else:
                return "configuration_changed"
        
        # 同じタイプのイベントが連続している場合
        if len(set(event_types)) == 1:
            return event_types[0]
        
        # その他の場合は設定変更として扱う
        return "configuration_changed"
    
    def set_debounce_delay(self, delay: float) -> None:
        """デバウンス遅延時間を設定"""
        if delay < 0:
            raise ValueError("デバウンス遅延時間は0以上である必要があります")
        
        with self._lock:
            self.debounce_delay = delay
    
    def get_debounce_delay(self) -> float:
        """現在のデバウンス遅延時間を取得"""
        return self.debounce_delay
    
    def get_pending_event_count(self) -> int:
        """保留中のイベント数を取得"""
        with self._lock:
            return len(self._pending_events)
    
    def get_statistics(self) -> Dict[str, Any]:
        """統計情報を取得"""
        with self._lock:
            return self._stats.copy()
    
    def clear_pending_events(self) -> int:
        """保留中のイベントをクリア"""
        with self._lock:
            count = len(self._pending_events)
            self._pending_events.clear()
            
            # タイマーもキャンセル
            if self._timer:
                self._timer.cancel()
                self._timer = None
            
            return count
    
    def is_processing(self) -> bool:
        """現在処理中かどうかを確認"""
        return self._is_processing
    
    def shutdown(self) -> None:
        """プロセッサーをシャットダウン"""
        with self._lock:
            # タイマーをキャンセル
            if self._timer:
                self._timer.cancel()
                self._timer = None
            
            # 保留中のイベントをクリア
            self._pending_events.clear()
            
            print("Event Processor がシャットダウンされました")


class EventFilter:
    """イベントフィルタリング機能を提供するクラス"""
    
    def __init__(self):
        """初期化"""
        self.excluded_event_types: List[str] = []
        self.min_screen_count = 0
        self.max_screen_count = 10
        self.excluded_screen_ids: List[str] = []
    
    def should_process_event(self, event: DisplayChangeEvent) -> bool:
        """イベントを処理すべきかどうかを判定"""
        # イベントタイプのフィルタリング
        if event.event_type in self.excluded_event_types:
            return False
        
        # ディスプレイ数のフィルタリング
        if event.screen_count < self.min_screen_count:
            return False
        
        if event.screen_count > self.max_screen_count:
            return False
        
        # 除外対象のScreen IDが含まれているかチェック
        for excluded_id in self.excluded_screen_ids:
            if excluded_id in event.screen_ids:
                return False
        
        return True
    
    def set_excluded_event_types(self, event_types: List[str]) -> None:
        """除外するイベントタイプを設定"""
        self.excluded_event_types = event_types.copy()
    
    def set_screen_count_range(self, min_count: int, max_count: int) -> None:
        """処理対象のディスプレイ数範囲を設定"""
        if min_count < 0 or max_count < min_count:
            raise ValueError("無効なディスプレイ数範囲です")
        
        self.min_screen_count = min_count
        self.max_screen_count = max_count
    
    def set_excluded_screen_ids(self, screen_ids: List[str]) -> None:
        """除外するScreen IDを設定"""
        self.excluded_screen_ids = screen_ids.copy()