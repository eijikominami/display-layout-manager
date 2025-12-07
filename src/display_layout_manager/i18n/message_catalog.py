"""
Message Catalog

Contains all user-facing messages in English and Japanese.
"""

MESSAGES = {
    "en": {
        # System messages
        "app_start": "Display Layout Manager v{version}",
        "app_complete": "Display Layout Manager execution completed",
        "app_interrupted": "Interrupted",
        "app_error": "An error occurred: {error}",
        
        # Dependency messages
        "checking_dependencies": "Checking dependencies...",
        "dependency_check_start": "Dependency check started",
        "dependency_issue": "Execution aborted due to dependency issues",
        "tool_available": "{tool} is available",
        "tool_not_found": "{tool} not found",
        "tool_found_version": "{tool} found: {version}",
        
        # Config messages
        "loading_config": "Loading configuration file...",
        "config_load_start": "Configuration file loading started: {path}",
        "config_loaded": "Configuration file loaded: {count} pattern(s)",
        "config_file_path": "Configuration file: {path}",
        "registered_patterns": "Registered patterns:",
        "pattern_info": "{index}. {name}",
        "pattern_description": "   Description: {description}",
        "pattern_screen_count": "   Screen IDs: {count}",
        "validating_config": "Validating configuration file...",
        "config_valid": "Configuration file is valid",
        "config_invalid": "Configuration file has issues:",
        
        # Display messages
        "checking_displays": "Checking display configuration...",
        "display_detection_start": "Display detection started",
        "displays_detected": "Current displays: {count} detected",
        "detected_screen_ids": "Detected Screen IDs:",
        "screen_id_item": "{index}. {screen_id}",
        
        # Pattern matching messages
        "pattern_matching": "Executing pattern matching...",
        "pattern_matching_start": "Pattern matching started",
        "pattern_match_result": "Pattern matching result:",
        "pattern_matched": "  Matched pattern: {name}",
        "pattern_match_type": "  Match type: {type}",
        "pattern_confidence": "  Confidence: {confidence:.2f}",
        "pattern_no_match": "  No matching pattern",
        "pattern_details": "  Details: {details}",
        "matching_details": "Matching details:",
        
        # Command execution messages
        "executing_command": "Executing command for matched pattern...",
        "command_execution_start": "Command execution started: {pattern}",
        "command_not_executed": "No matching pattern - command not executed",
        "execution_details": "Execution details:",
        
        # Layout save messages
        "save_layout_start": "Current layout save started",
        "save_layout_complete": "Current layout save completed",
        "save_layout_failed": "Current layout save failed",
        
        # Test messages
        "test_execution_start": "Integration test execution started",
        "test_all_success": "All integration tests passed",
        "test_failed": "Integration tests failed",
        
        # Session summary messages
        "session_summary": "Session Summary",
        "total_log_entries": "Total log entries: {count}",
        "by_level": "By level:",
        "by_component": "By component:",
        "log_file": "Log file: {path}",
        "errors_occurred": "Note: Errors occurred during execution",
        "check_log_file": "Please check the log file for details: {path}",
        
        # Menu bar messages
        "menu_apply_layout": "Apply Layout",
        "menu_save_current": "Save Current Layout",
        "menu_auto_launch": "Launch at Login",
        "menu_quit": "Quit",
        "auto_launch_enabled": "Auto-launch enabled",
        "auto_launch_disabled": "Auto-launch disabled",
        "menubar_app_quit": "Quitting menu bar application",
        "layout_applied": "Layout applied successfully",
        "layout_saved": "Layout saved as: {pattern}",
        
        # Error messages
        "error_occurred": "Error occurred: {error}",
        "config_not_found": "Configuration file not found",
        "command_failed": "Command execution failed",
        
        # Verbose mode messages
        "verbose_enabled": "Verbose logging: Enabled",
        "dry_run_enabled": "Dry-run mode: Enabled",
    },
    "ja": {
        # システムメッセージ
        "app_start": "Display Layout Manager v{version}",
        "app_complete": "Display Layout Manager の実行が完了しました",
        "app_interrupted": "中断されました",
        "app_error": "エラーが発生しました: {error}",
        
        # 依存関係メッセージ
        "checking_dependencies": "依存関係を確認中...",
        "dependency_check_start": "依存関係チェック開始",
        "dependency_issue": "依存関係の問題により実行を中止",
        "tool_available": "{tool} が利用可能です",
        "tool_not_found": "{tool} が見つかりません",
        "tool_found_version": "{tool} が見つかりました: {version}",
        
        # 設定ファイルメッセージ
        "loading_config": "設定ファイルを読み込み中...",
        "config_load_start": "設定ファイル読み込み開始: {path}",
        "config_loaded": "設定ファイル読み込み完了: {count}個のパターン",
        "config_file_path": "設定ファイル: {path}",
        "registered_patterns": "登録されているパターン:",
        "pattern_info": "{index}. {name}",
        "pattern_description": "   説明: {description}",
        "pattern_screen_count": "   Screen IDs: {count}個",
        "validating_config": "設定ファイルを検証中...",
        "config_valid": "設定ファイルは有効です",
        "config_invalid": "設定ファイルに問題があります:",
        
        # ディスプレイメッセージ
        "checking_displays": "ディスプレイ構成を確認中...",
        "display_detection_start": "ディスプレイ検出開始",
        "displays_detected": "現在のディスプレイ: {count}個検出",
        "detected_screen_ids": "検出されたScreen IDs:",
        "screen_id_item": "{index}. {screen_id}",
        
        # パターンマッチングメッセージ
        "pattern_matching": "パターンマッチングを実行中...",
        "pattern_matching_start": "パターンマッチング開始",
        "pattern_match_result": "パターンマッチング結果:",
        "pattern_matched": "  ✓ マッチしたパターン: {name}",
        "pattern_match_type": "  マッチタイプ: {type}",
        "pattern_confidence": "  信頼度: {confidence:.2f}",
        "pattern_no_match": "  ✗ マッチするパターンなし",
        "pattern_details": "  詳細: {details}",
        "matching_details": "マッチング詳細:",
        
        # コマンド実行メッセージ
        "executing_command": "マッチしたパターンのコマンドを実行します...",
        "command_execution_start": "コマンド実行開始: {pattern}",
        "command_not_executed": "マッチするパターンなし - コマンド未実行",
        "execution_details": "実行詳細:",
        
        # レイアウト保存メッセージ
        "save_layout_start": "現在レイアウト保存開始",
        "save_layout_complete": "現在レイアウト保存完了",
        "save_layout_failed": "現在レイアウト保存失敗",
        
        # テストメッセージ
        "test_execution_start": "統合テスト実行開始",
        "test_all_success": "統合テスト全て成功",
        "test_failed": "統合テスト失敗",
        
        # セッションサマリーメッセージ
        "session_summary": "セッションサマリー",
        "total_log_entries": "総ログエントリ数: {count}",
        "by_level": "レベル別:",
        "by_component": "コンポーネント別:",
        "log_file": "ログファイル: {path}",
        "errors_occurred": "注意: 実行中にエラーが発生しました",
        "check_log_file": "詳細はログファイルを確認してください: {path}",
        
        # メニューバーメッセージ
        "menu_apply_layout": "レイアウトを適用",
        "menu_save_current": "現在の設定を保存",
        "menu_auto_launch": "ログイン時に起動",
        "menu_quit": "終了",
        "auto_launch_enabled": "ログイン時の自動起動を有効化しました",
        "auto_launch_disabled": "ログイン時の自動起動を無効化しました",
        "menubar_app_quit": "メニューバーアプリケーションを終了します",
        "layout_applied": "レイアウトを適用しました",
        "layout_saved": "レイアウトを保存しました: {pattern}",
        
        # エラーメッセージ
        "error_occurred": "エラーが発生しました: {error}",
        "config_not_found": "設定ファイルが見つかりません",
        "command_failed": "コマンドの実行に失敗しました",
        
        # 詳細モードメッセージ
        "verbose_enabled": "詳細ログ: 有効",
        "dry_run_enabled": "ドライランモード: 有効",
    },
}
