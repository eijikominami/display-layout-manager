# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2025-12-06

### Removed
- **常駐監視機能**: macOS のバックグラウンドプロセスでは NSApplication 通知が動作しないため削除
- **デーモン関連コマンド**: `--daemon`, `--enable-daemon`, `--disable-daemon` 等を削除
- **PyObjC 依存関係**: 常駐機能削除に伴い pyobjc-framework-Cocoa を削除
- **デーモン関連モジュール**: display_monitor.py, event_processor.py, daemon_manager.py 等を削除

### Changed
- **requirements.txt**: 外部依存関係なし（標準ライブラリのみ使用）に変更
- **README.md**: 常駐機能に関する記載を削除
- **Homebrew Formula**: デーモン関連のセットアップコードを削除

### Migration Guide for Existing Users

v1.1.0〜v1.1.4 で常駐機能を有効化していたユーザーは、以下のファイルを手動で削除してください：

```bash
# LaunchAgent を停止・削除
launchctl unload ~/Library/LaunchAgents/com.eijikominami.display-layout-manager.plist
rm ~/Library/LaunchAgents/com.eijikominami.display-layout-manager.plist

# デーモン設定ファイルを削除（オプション）
rm ~/Library/Application\ Support/DisplayLayoutManager/daemon.json

# デーモンログファイルを削除（オプション）
rm ~/Library/Logs/DisplayLayoutManager/daemon.log
rm ~/Library/Logs/DisplayLayoutManager/daemon_error.log
```

**注意**: 基本機能（`display-layout-manager` コマンドによる手動レイアウト適用）は引き続き動作します。

## [1.1.4] - 2025-12-06

### Changed
- **Homebrew インストール**: post_install での自動常駐機能有効化を削除
- **ユーザー体験**: インストール後に手動で `--enable-daemon` 実行が必要に変更
- **権限問題解決**: macOS セキュリティ制限による権限エラーを回避

### Fixed
- **要件定義書**: 要件16の受け入れ基準を実装に合わせて修正
- **README.md**: 常駐機能の有効化手順を正確に更新
- **GitHub Actions**: PyObjC リソースが自動削除されないように修正

### Added
- **開発ガイドライン**: 実装変更時の仕様書・ドキュメント整合性確認プロセスを追加
- **品質保証**: コミット前品質保証メカニズムをステアリングに追加

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

## [1.1.0] - 2025-12-06

### Added
- **常駐監視機能**: ディスプレイ変更の自動検知と自動レイアウト適用（後に削除）
- **LaunchAgent 統合**: ログイン時の自動起動とクラッシュ時の自動再起動（後に削除）
- **ディスプレイ変更監視**: NSApplication.didChangeScreenParametersNotification を使用（後に削除）
- **イベント処理システム**: デバウンス機能付きイベント処理（後に削除）
- **設定の動的リロード**: daemon.json 設定ファイルの変更を自動検知（後に削除）
- **非同期コマンド実行**: レイアウト適用の非同期処理とキュー管理（後に削除）
- **包括的な管理コマンド**: 常駐機能管理コマンド（後に削除）

### Note
- v1.1.0 で追加された常駐監視機能は、macOS のバックグラウンドプロセスでは NSApplication 通知が正しく動作しないことが判明したため、後のバージョンで削除されました

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
