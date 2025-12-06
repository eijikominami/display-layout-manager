# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.3] - 2025-12-06

### Fixed
- **GitHub Actions**: Homebrew Formula 自動更新時に PyObjC リソースが削除される問題を修正
- **PyObjC 依存関係**: Formula に pyobjc-core と pyobjc-framework-Cocoa リソースを確実に含める
- **自動化**: リリースプロセスで PyObjC 依存関係が維持されるように改善

## [1.1.2] - 2025-12-06

### Fixed
- **PyObjC インポートエラー**: NSApplication を Foundation から AppKit に修正
- **常駐機能**: デーモンモードでの PyObjC 利用可能性チェックを修正
- **リアルタイム監視**: ディスプレイ変更の即座検知が正常に動作

## [1.1.1] - 2025-12-06

### Fixed
- **PyObjC 依存関係**: pyproject.toml に pyobjc-framework-Cocoa>=10.0 を追加
- **自動インストール**: 新規インストール時に PyObjC が自動的に含まれるように修正
- **警告解消**: "PyObjC が利用できません" 警告が表示されなくなる
- **パフォーマンス向上**: ポーリング方式からリアルタイム通知に改善

## [1.0.0] - 2025-12-03

### Added
- 初回リリース
- 依存関係管理機能（Homebrew、displayplacer、GNU grep）
- 設定ファイル管理機能（JSON形式）
- ディスプレイ検出機能（Persistent Screen ID抽出）
- パターンマッチング機能（完全一致・部分一致）
- コマンド実行機能（displayplacerコマンド実行）
- ログ・フィードバック機能（構造化ログ出力）
- 統合テスト機能
- エラーハンドリング強化
- コマンドラインインターフェース
  - `--verbose`: 詳細ログ表示
  - `--dry-run`: ドライラン実行
  - `--show-displays`: 現在のディスプレイ構成表示
  - `--validate-config`: 設定ファイル検証
  - `--run-tests`: 統合テスト実行
  - `--config`: 設定ファイルパス指定

### Features
- macOS標準ディレクトリ構造対応
  - 設定ファイル: `~/Library/Application Support/DisplayLayoutManager/`
  - ログファイル: `~/Library/Logs/DisplayLayoutManager/`
- 自動依存関係インストール
- デフォルト設定ファイル自動作成
- 包括的なエラーメッセージとトラブルシューティングガイド
- 構造化ログ出力（JSON形式）
- セッションサマリー表示

### Technical Details
- Python 3.8+ 対応
- 標準ライブラリのみ使用（外部依存関係なし）
- Homebrew Formula 提供
- 統合テストスイート
- 包括的なエラーハンドリング

## [1.1.0] - 2025-12-06

### Added
- **常駐監視機能**: ディスプレイ変更の自動検知と自動レイアウト適用
- **LaunchAgent 統合**: ログイン時の自動起動とクラッシュ時の自動再起動
- **ディスプレイ変更監視**: NSApplication.didChangeScreenParametersNotification を使用
- **イベント処理システム**: デバウンス機能付きイベント処理（デフォルト2秒）
- **設定の動的リロード**: daemon.json 設定ファイルの変更を自動検知
- **非同期コマンド実行**: レイアウト適用の非同期処理とキュー管理
- **包括的な管理コマンド**:
  - `--daemon`: 常駐モードで実行
  - `--enable-daemon` / `--disable-daemon`: 常駐機能の有効化/無効化
  - `--start-daemon` / `--stop-daemon`: 手動開始/停止
  - `--status-daemon`: 常駐プロセスの状態確認
  - `--show-daemon-logs` / `--clear-daemon-logs`: ログ管理
  - `--daemon-config` / `--reload-daemon`: 設定管理

### Enhanced
- **Homebrew Formula**: インストール時の常駐機能自動セットアップ
- **ログ機能**: daemon.log と execution_history.log の追加
- **統合テスト**: 常駐機能のテストケース追加
- **エラーハンドリング**: 常駐機能固有のエラー処理

### Technical Details
- 新規モジュール:
  - `display_monitor.py`: ディスプレイ変更監視
  - `event_processor.py`: イベント処理とデバウンス
  - `daemon_manager.py`: LaunchAgent 管理
  - `configuration_watcher.py`: 設定ファイル監視
  - `command_scheduler.py`: コマンド実行スケジューラー
- PyObjC 対応（オプション）: macOS 通知システムとの統合
- メモリ・CPU 使用量最適化
- バッテリー消費量最適化

## [1.1.1] - 2025-12-06

### Fixed
- **PyObjC 依存関係**: pyproject.toml に pyobjc-framework-Cocoa>=10.0 を追加
- **自動インストール**: Homebrew インストール時に PyObjC が自動的に含まれるように修正
- **警告解消**: "PyObjC が利用できません" 警告が新規インストールで表示されなくなる
- **パフォーマンス**: ポーリング方式からリアルタイム通知方式への自動切り替え

### Technical Details
- pyproject.toml の dependencies に PyObjC を追加
- setup.py と pyproject.toml の依存関係を統一
- 最適なディスプレイ変更監視のための環境整備

## [1.1.1] - 2025-12-06

### Fixed
- **PyObjC 依存関係**: pyproject.toml に pyobjc-framework-Cocoa>=10.0 を追加
- **自動インストール**: Homebrew インストール時に PyObjC が自動的に含まれるように修正
- **パフォーマンス**: ポーリングベースからリアルタイム通知への自動切り替え

### Enhanced
- **警告解消**: "PyObjC が利用できません" 警告が新規インストールで表示されなくなる
- **最適化**: ディスプレイ変更検知のレスポンス時間とバッテリー効率が改善

## [Unreleased]

### Planned
- 単体テスト実装
- ドキュメント拡充
- GUI インターフェース
- プロファイル管理機能