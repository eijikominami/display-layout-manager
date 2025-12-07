[**English**](ARCHITECTURE.md) / 日本語

# アーキテクチャドキュメント

## システム概要

Display Layout Manager は、macOS のディスプレイレイアウトを自動的に管理するためのツールです。CLI とメニューバーアプリの2つのインターフェースを提供し、ディスプレイ構成の検出、パターンマッチング、レイアウト適用を自動化します。

## アーキテクチャ図

```
┌─────────────────────────────────────────────────────────────┐
│                     ユーザーインターフェース                    │
├──────────────────────────┬──────────────────────────────────┤
│   CLI (main.py)          │  Menu Bar App (menubar_app.py)   │
│   - コマンドライン引数解析  │  - rumps ベースの GUI            │
│   - 対話的操作            │  - メニュー項目管理               │
└──────────────┬───────────┴────────────┬─────────────────────┘
               │                        │
               └────────┬───────────────┘
                        │
         ┌──────────────┴──────────────┐
         │   CLI Bridge (cli_bridge.py) │
         │   - UI層とビジネスロジックの橋渡し │
         └──────────────┬──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │      ビジネスロジック層        │
         ├─────────────────────────────┤
         │  Config Manager              │
         │  - 設定ファイル読み込み        │
         │  - JSON パース・検証          │
         ├─────────────────────────────┤
         │  Display Manager             │
         │  - ディスプレイ検出            │
         │  - Screen ID 抽出            │
         ├─────────────────────────────┤
         │  Pattern Matcher             │
         │  - パターンマッチング          │
         │  - 最適レイアウト選択          │
         ├─────────────────────────────┤
         │  Layout Saver                │
         │  - 現在レイアウト保存          │
         │  - 設定ファイル更新            │
         ├─────────────────────────────┤
         │  Command Executor            │
         │  - displayplacer 実行         │
         │  - コマンド検証                │
         ├─────────────────────────────┤
         │  Dependency Manager          │
         │  - 依存関係チェック            │
         │  - 自動インストール            │
         ├─────────────────────────────┤
         │  Auto Launch Manager         │
         │  - LaunchAgent 管理           │
         │  - 自動起動設定                │
         └──────────────┬──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │      インフラストラクチャ層    │
         ├─────────────────────────────┤
         │  Logger (logger.py)          │
         │  - 構造化ログ出力              │
         │  - ファイルローテーション       │
         ├─────────────────────────────┤
         │  Error Handler               │
         │  - エラーハンドリング          │
         │  - ユーザーフレンドリーメッセージ │
         └──────────────┬──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │      外部依存                 │
         ├─────────────────────────────┤
         │  displayplacer               │
         │  - ディスプレイ設定ツール       │
         ├─────────────────────────────┤
         │  GNU grep                    │
         │  - テキスト検索                │
         ├─────────────────────────────┤
         │  Homebrew                    │
         │  - パッケージ管理              │
         └─────────────────────────────┘
```

## コンポーネント詳細

### 1. ユーザーインターフェース層

#### CLI (main.py)
- **責務**: コマンドライン引数の解析、ユーザー入力の処理
- **主要機能**:
  - `argparse` による引数解析
  - 各種オプション（`--show-displays`, `--save-current`, `--dry-run` など）の処理
  - CLI Bridge への処理委譲
- **依存関係**: `cli_bridge.CLIBridge`, `logger.Logger`

#### Menu Bar App (menubar_app.py)
- **責務**: macOS メニューバーアプリケーションの提供
- **主要機能**:
  - `rumps` フレームワークを使用した GUI
  - メニュー項目の動的生成
  - ユーザーアクションのハンドリング
  - 自動起動設定の管理
- **依存関係**: `rumps`, `cli_bridge.CLIBridge`, `auto_launch_manager.AutoLaunchManager`

### 2. ビジネスロジック層

#### CLI Bridge (cli_bridge.py)
- **責務**: UI層とビジネスロジック層の橋渡し
- **主要機能**:
  - 各種操作の統合（レイアウト適用、保存、表示など）
  - エラーハンドリングの統一
  - ログ出力の統一
- **依存関係**: すべてのビジネスロジックコンポーネント

#### Config Manager (config_manager.py)
- **責務**: 設定ファイルの管理
- **主要機能**:
  - JSON 設定ファイルの読み込み
  - 設定ファイルの検証
  - デフォルト設定の生成
  - 設定ファイルの更新
- **データ構造**:
  ```python
  {
      "version": str,
      "patterns": [
          {
              "name": str,
              "description": str,
              "screen_ids": List[str],
              "command": str
          }
      ]
  }
  ```

#### Display Manager (display_manager.py)
- **責務**: ディスプレイ情報の取得
- **主要機能**:
  - `displayplacer list` コマンドの実行
  - Persistent Screen ID の抽出
  - 現在のディスプレイ構成の取得
- **依存関係**: `subprocess`, `re`

#### Pattern Matcher (pattern_matcher.py)
- **責務**: ディスプレイ構成とパターンのマッチング
- **主要機能**:
  - Screen ID セットの比較
  - 最適パターンの選択
  - マッチング結果の返却
- **アルゴリズム**: セットの完全一致（順序不問）

#### Layout Saver (layout_saver.py)
- **責務**: 現在のレイアウトの保存
- **主要機能**:
  - 現在のディスプレイ構成の取得
  - `displayplacer list` からコマンドの抽出
  - パターン名の自動生成
  - 設定ファイルへの追加・更新
- **命名規則**: `{count}_Displays_{id1}_{id2}_{id3}`

#### Command Executor (command_executor.py)
- **責務**: displayplacer コマンドの実行
- **主要機能**:
  - コマンドの検証
  - ドライランモードのサポート
  - コマンド実行とエラーハンドリング
- **依存関係**: `subprocess`

#### Dependency Manager (dependency_manager.py)
- **責務**: 外部依存関係の管理
- **主要機能**:
  - Homebrew の存在確認
  - displayplacer の存在確認とインストール
  - GNU grep の存在確認とインストール
  - インストール状況のレポート
- **依存関係**: `subprocess`, `shutil`

#### Auto Launch Manager (auto_launch_manager.py)
- **責務**: ログイン時の自動起動管理
- **主要機能**:
  - LaunchAgent plist ファイルの作成
  - 自動起動の有効化・無効化
  - 現在の状態確認
- **ファイル**: `~/Library/LaunchAgents/com.displaylayoutmanager.menubar.plist`

### 3. インフラストラクチャ層

#### Logger (logger.py)
- **責務**: ログ出力の管理
- **主要機能**:
  - 構造化ログ（JSON 形式）
  - ファイルローテーション（日次）
  - コンソール出力とファイル出力の両立
  - ログレベル管理
- **ログファイル**: `~/Library/Logs/DisplayLayoutManager/`

#### Error Handler (error_handler.py)
- **責務**: エラーハンドリングの統一
- **主要機能**:
  - カスタム例外クラスの定義
  - ユーザーフレンドリーなエラーメッセージ
  - トラブルシューティングガイドの提供
- **例外階層**:
  ```
  DisplayLayoutError (基底クラス)
  ├── ConfigError (設定ファイルエラー)
  ├── DisplayDetectionError (ディスプレイ検出エラー)
  ├── PatternMatchError (パターンマッチングエラー)
  ├── CommandExecutionError (コマンド実行エラー)
  └── DependencyError (依存関係エラー)
  ```

## データフロー

### レイアウト適用フロー

```
1. ユーザー入力
   ↓
2. CLI / Menu Bar App
   ↓
3. CLI Bridge.apply_layout()
   ↓
4. Dependency Manager.check_dependencies()
   ├→ Homebrew チェック
   ├→ displayplacer チェック
   └→ GNU grep チェック
   ↓
5. Config Manager.load_config()
   ├→ 設定ファイル読み込み
   └→ JSON パース・検証
   ↓
6. Display Manager.get_current_displays()
   ├→ displayplacer list 実行
   └→ Screen ID 抽出
   ↓
7. Pattern Matcher.find_matching_pattern()
   ├→ Screen ID セット比較
   └→ 最適パターン選択
   ↓
8. Command Executor.execute()
   ├→ コマンド検証
   └→ displayplacer 実行
   ↓
9. 結果返却
```

### レイアウト保存フロー

```
1. ユーザー入力 (--save-current)
   ↓
2. CLI / Menu Bar App
   ↓
3. CLI Bridge.save_current_layout()
   ↓
4. Display Manager.get_current_displays()
   ├→ displayplacer list 実行
   └→ Screen ID 抽出
   ↓
5. Layout Saver.save_current_layout()
   ├→ 現在のコマンド取得
   ├→ パターン名生成
   └→ 設定ファイル更新
   ↓
6. Config Manager.save_config()
   ├→ JSON シリアライズ
   └→ ファイル書き込み
   ↓
7. 結果返却
```

## 設計原則

### 1. 単一責任の原則 (SRP)
各コンポーネントは1つの責務のみを持ちます。例えば、`ConfigManager` は設定ファイルの管理のみを担当し、ディスプレイ検出は `DisplayManager` が担当します。

### 2. 依存性逆転の原則 (DIP)
高レベルモジュール（CLI Bridge）は低レベルモジュール（各マネージャー）に依存しますが、インターフェースを通じて疎結合を保ちます。

### 3. 開放閉鎖の原則 (OCP)
新しい機能（例：新しいパターンマッチングアルゴリズム）は、既存コードを変更せずに追加できるように設計されています。

### 4. エラーハンドリング
すべてのエラーは適切にキャッチされ、ユーザーフレンドリーなメッセージとトラブルシューティングガイドが提供されます。

### 5. ログ出力
すべての重要な操作はログに記録され、デバッグとトラブルシューティングを容易にします。

## テスト戦略

### 単体テスト
各コンポーネントは独立してテスト可能です：
- `test_config_manager.py`: 設定ファイルの読み込み・検証
- `test_display_manager.py`: ディスプレイ検出
- `test_pattern_matcher.py`: パターンマッチング
- `test_command_executor.py`: コマンド実行
- `test_layout_saver.py`: レイアウト保存

### 統合テスト
- `test_cli_components.py`: CLI コンポーネントの統合テスト
- `test_menubar_integration.py`: メニューバーアプリの統合テスト
- `integration_test.py`: エンドツーエンドテスト

### テストカバレッジ
- 目標: 70%以上
- 現在: CI/CD で自動測定
- レポート: Codecov で可視化

## パフォーマンス考慮事項

### 起動時間
- 依存関係チェック: ~100ms
- 設定ファイル読み込み: ~10ms
- ディスプレイ検出: ~200ms
- 合計: ~300ms

### メモリ使用量
- CLI: ~20MB
- Menu Bar App: ~30MB

### ディスク使用量
- アプリケーション: ~3.5MB
- ログファイル: ~1MB/日（自動ローテーション）

## セキュリティ考慮事項

### ファイルパーミッション
- 設定ファイル: `0600` (ユーザーのみ読み書き可能)
- ログファイル: `0600` (ユーザーのみ読み書き可能)
- LaunchAgent plist: `0644` (標準パーミッション)

### コマンド実行
- `subprocess` を使用した安全なコマンド実行
- シェルインジェクション対策
- コマンド検証

### 依存関係
- 信頼できるソース（Homebrew）からのみインストール
- バージョン固定による再現性確保

## 拡張性

### 新しいパターンマッチングアルゴリズム
`PatternMatcher` クラスを拡張することで、より高度なマッチングロジックを追加できます。

### 新しいインターフェース
CLI Bridge を使用することで、新しい UI（例：Web インターフェース）を簡単に追加できます。

### プラグインシステム
将来的には、カスタムプラグインをサポートする拡張ポイントを提供する予定です。

## 今後の改善計画

1. **プロファイル機能**: 複数の設定プロファイルをサポート
2. **クラウド同期**: iCloud を使用した設定の同期
3. **ホットキーサポート**: キーボードショートカットでレイアウト切り替え
4. **通知機能**: レイアウト適用時の通知表示
5. **プラグインシステム**: カスタム機能の追加をサポート
