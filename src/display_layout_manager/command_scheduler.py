"""
Command Scheduler Module

display-layout-manager コマンドの非同期実行とスケジューリング機能を提供するモジュール。
実行キューの管理、結果の記録、リトライ機能を含む。
"""

import subprocess
import threading
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from queue import Queue, Empty
from .event_processor import ProcessedEvent


@dataclass
class ExecutionRequest:
    """コマンド実行リクエストを表すデータクラス"""
    request_id: str
    event: ProcessedEvent
    command: str
    pattern_name: str
    timestamp: datetime
    retry_count: int = 0
    max_retries: int = 2
    timeout: int = 30
    dry_run: bool = False


@dataclass
class ExecutionResult:
    """コマンド実行結果を表すデータクラス"""
    request_id: str
    success: bool
    command: str
    pattern_name: str
    stdout: str
    stderr: str
    return_code: int
    execution_time: float
    timestamp: datetime
    retry_count: int
    dry_run: bool = False
    error_message: Optional[str] = None


class CommandScheduler:
    """display-layout-manager コマンドの非同期実行とスケジューリングを管理するクラス"""
    
    def __init__(self, max_concurrent: int = 1):
        """初期化"""
        self.max_concurrent = max_concurrent
        self.execution_queue: Queue[ExecutionRequest] = Queue()
        self.execution_results: List[ExecutionResult] = []
        self._is_running = False
        self._worker_threads: List[threading.Thread] = []
        self._stop_event = threading.Event()
        
        # 実行履歴ログファイル
        self.history_log_path = Path.home() / "Library/Logs/DisplayLayoutManager/execution_history.log"
        self._setup_history_log()
    
    def start(self) -> bool:
        """スケジューラーを開始"""
        if self._is_running:
            return True
        
        self._is_running = True
        self._stop_event.clear()
        
        # ワーカースレッドを開始
        for i in range(self.max_concurrent):
            worker_thread = threading.Thread(
                target=self._worker_loop,
                daemon=True
            )
            worker_thread.start()
            self._worker_threads.append(worker_thread)
        
        return True
    
    def stop(self) -> None:
        """スケジューラーを停止"""
        self._is_running = False
        self._stop_event.set()
        
        for thread in self._worker_threads:
            if thread.is_alive():
                thread.join(timeout=5.0)
        
        self._worker_threads.clear()
    
    def schedule_execution(self, event: ProcessedEvent, command: str, pattern_name: str) -> str:
        """コマンド実行をスケジュール"""
        request_id = f"req_{int(time.time() * 1000)}"
        
        request = ExecutionRequest(
            request_id=request_id,
            event=event,
            command=command,
            pattern_name=pattern_name,
            timestamp=datetime.now()
        )
        
        self.execution_queue.put(request)
        return request_id
    
    def _worker_loop(self) -> None:
        """ワーカースレッドのメインループ"""
        while not self._stop_event.is_set():
            try:
                request = self.execution_queue.get(timeout=1.0)
                result = self._execute_request(request)
                self._record_result(result)
            except Empty:
                continue
            except Exception as e:
                print(f"ワーカーループ中にエラー: {e}")
    
    def _execute_request(self, request: ExecutionRequest) -> ExecutionResult:
        """リクエストを実行"""
        start_time = time.time()
        
        try:
            process = subprocess.run(
                request.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=request.timeout
            )
            
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                request_id=request.request_id,
                success=process.returncode == 0,
                command=request.command,
                pattern_name=request.pattern_name,
                stdout=process.stdout,
                stderr=process.stderr,
                return_code=process.returncode,
                execution_time=execution_time,
                timestamp=datetime.now(),
                retry_count=request.retry_count
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                request_id=request.request_id,
                success=False,
                command=request.command,
                pattern_name=request.pattern_name,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=execution_time,
                timestamp=datetime.now(),
                retry_count=request.retry_count,
                error_message=str(e)
            )
    
    def _record_result(self, result: ExecutionResult) -> None:
        """実行結果を記録"""
        self.execution_results.append(result)
        self._write_history_log(result)
    
    def _setup_history_log(self) -> None:
        """実行履歴ログファイルのセットアップ"""
        try:
            self.history_log_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"実行履歴ログディレクトリ作成中にエラー: {e}")
    
    def _write_history_log(self, result: ExecutionResult) -> None:
        """実行履歴ログに書き込み"""
        try:
            log_entry = {
                'timestamp': result.timestamp.isoformat(),
                'request_id': result.request_id,
                'pattern_name': result.pattern_name,
                'success': result.success,
                'return_code': result.return_code,
                'execution_time': result.execution_time,
                'command': result.command
            }
            
            with open(self.history_log_path, 'a', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write('\n')
                
        except Exception as e:
            print(f"実行履歴ログ書き込み中にエラー: {e}")
    
    def get_recent_results(self, count: int = 10) -> List[ExecutionResult]:
        """最近の実行結果を取得"""
        return self.execution_results[-count:] if self.execution_results else []
    
    def get_queue_size(self) -> int:
        """実行待ちキューのサイズを取得"""
        return self.execution_queue.qsize()
    
    def clear_history(self) -> bool:
        """実行履歴をクリア"""
        try:
            self.execution_results.clear()
            
            # ログファイルもクリア
            if self.history_log_path.exists():
                self.history_log_path.write_text('')
            
            return True
            
        except Exception as e:
            print(f"実行履歴クリア中にエラー: {e}")
            return False