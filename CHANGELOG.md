# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [Unreleased]

### Planned
- 単体テスト実装
- CI/CD パイプライン設定
- ドキュメント拡充
- パフォーマンス最適化