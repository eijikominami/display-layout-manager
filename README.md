# Display Layout Manager

macOS用のディスプレイレイアウト自動設定ツール

## 概要

Display Layout Manager は、macOS で複数のディスプレイ構成を自動的に管理するためのコマンドラインツールです。異なるディスプレイの組み合わせに応じて、事前に定義されたレイアウト設定を自動的に適用します。

## 主な機能

### 基本機能
- **自動ディスプレイ検出**: 現在接続されているディスプレイの Persistent Screen ID を自動検出
- **パターンマッチング**: ディスプレイ構成に基づいて最適なレイアウトパターンを自動選択
- **設定ファイル管理**: JSON 形式の設定ファイルで複数のレイアウトパターンを管理
- **現在レイアウト保存**: `--save-current` で現在のディスプレイ構成を簡単保存
- **依存関係管理**: 必要なツールの自動インストールと確認

### 常駐監視機能 🆕
- **自動ディスプレイ変更検知**: ミラーリング/拡張モードの切り替えやディスプレイ追加/削除を自動検知
- **バックグラウンド実行**: LaunchAgent として常駐し、ログイン時に自動開始
- **デバウンス処理**: 連続するディスプレイ変更イベントを統合（設定可能な遅延時間）
- **設定の動的リロード**: 設定ファイル変更時の自動リロード
- **包括的な管理コマンド**: 有効化/無効化、状態確認、ログ管理

### その他
- **包括的なログ**: 構造化ログ出力とセッションサマリー
- **エラーハンドリング**: ユーザーフレンドリーなエラーメッセージとトラブルシューティングガイド
- **統合テスト**: 包括的なテストスイートによる品質保証

## システム要件

- **OS**: macOS 10.14 (Mojave) 以降
- **Python**: 3.8 以降
- **依存ツール**: Homebrew、displayplacer、GNU grep（自動インストール対応）

## インストール

### Homebrew を使用（推奨）

```bash
# Homebrew tap を追加
brew tap eijikominami/display-layout-manager

# Display Layout Manager をインストール
brew install display-layout-manager
```

### pip を使用

```bash
# PyPI からインストール
pip install display-layout-manager

# または GitHub から直接インストール
pip install git+https://github.com/eijikominami/display-layout-manager.git
```

### ソースからインストール

```bash
# リポジトリをクローン
git clone https://github.com/eijikominami/display-layout-manager.git
cd display-layout-manager

# 開発モードでインストール
pip install -e .
```

## 使用方法

### 基本コマンド

```bash
# 基本実行（自動でディスプレイレイアウトを適用）
display-layout-manager

# 現在のディスプレイ構成を表示
display-layout-manager --show-displays

# 設定ファイルの検証
display-layout-manager --validate-config

# ドライラン（実際にコマンドを実行しない）
display-layout-manager --dry-run

# 詳細ログ付き実行
display-layout-manager --verbose

# 統合テストの実行
display-layout-manager --run-tests

# 現在のレイアウトを保存
display-layout-manager --save-current

# 常駐機能の管理
display-layout-manager --status-daemon      # 状態確認
display-layout-manager --enable-daemon      # 有効化
display-layout-manager --disable-daemon     # 無効化
display-layout-manager --show-daemon-logs   # ログ表示

# ヘルプ表示
display-layout-manager --help
```

### 常駐監視機能

v1.1.0 から追加された常駐監視機能により、ディスプレイ設定の変更を自動的に検知し、適切なレイアウトを自動適用できます。

#### 特徴
- **自動検知**: ミラーリング/拡張モードの切り替え、ディスプレイの追加/削除を検知
- **デバウンス処理**: 連続する変更イベントを統合（デフォルト2秒、設定可能）
- **バックグラウンド実行**: LaunchAgent として常駐、ログイン時に自動開始
- **自動再起動**: クラッシュ時の自動回復機能
- **設定リロード**: daemon.json の変更を自動検知してリロード

#### 使用方法

```bash
# 常駐機能の状態確認
display-layout-manager --status-daemon

# 常駐機能を有効化（Homebrew インストール時は自動で有効化済み）
display-layout-manager --enable-daemon

# 常駐機能を無効化
display-layout-manager --disable-daemon

# 常駐プロセスを手動で開始/停止
display-layout-manager --start-daemon
display-layout-manager --stop-daemon

# ログの確認とクリア
display-layout-manager --show-daemon-logs
display-layout-manager --clear-daemon-logs

# 常駐設定の確認
display-layout-manager --daemon-config
```

#### 常駐設定ファイル

常駐機能の設定は `~/Library/Application Support/DisplayLayoutManager/daemon.json` で管理されます：

```json
{
  "version": "1.0",
  "daemon": {
    "enabled": true,
    "debounce_delay": 2.0,
    "log_level": "INFO",
    "auto_execute": true
  },
  "monitoring": {
    "display_changes": true,
    "configuration_changes": true
  },
  "execution": {
    "command_timeout": 30,
    "retry_count": 2,
    "dry_run": false
  }
}
```

### 設定ファイル

設定ファイルは以下の場所に自動作成されます：
- **デフォルト**: `~/Library/Application Support/DisplayLayoutManager/config.json`
- **環境変数**: `DISPLAY_LAYOUT_CONFIG` で指定可能
- **コマンドライン**: `--config` オプションで指定可能

#### 設定ファイル例

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Laptop Only",
      "description": "ラップトップ単体使用",
      "screen_ids": [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230"
      ],
      "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\""
    },
    {
      "name": "Home Office Setup",
      "description": "メインディスプレイ + 外部モニター2台",
      "screen_ids": [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230",
        "3F816611-C361-483F-8FB3-CE03208D949C",
        "AE0F5F39-5D5C-4FF1-A7BA-8E5CBE679211"
      ],
      "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\" \"id:3F816611-C361-483F-8FB3-CE03208D949C res:1920x1080 hz:120 color_depth:4 enabled:true scaling:off origin:(-1278,-1080) degree:0\" \"id:AE0F5F39-5D5C-4FF1-A7BA-8E5CBE679211 res:1920x1080 hz:120 color_depth:4 enabled:true scaling:off origin:(642,-1080) degree:0\""
    }
  ]
}
```

### 設定手順

1. **現在のディスプレイ構成を確認**
   ```bash
   display-layout-manager --show-displays
   ```

2. **設定ファイルを編集**
   - 出力された Screen ID を使用してパターンを作成
   - `displayplacer list` コマンドで現在のコマンドを取得

3. **設定ファイルを検証**
   ```bash
   display-layout-manager --validate-config
   ```

4. **ドライランでテスト**
   ```bash
   display-layout-manager --dry-run --verbose
   ```

### 現在のレイアウトを自動保存

手動での設定ファイル編集を避けたい場合は、現在のディスプレイレイアウトを自動的に保存できます：

```bash
# 現在のディスプレイレイアウトを保存
display-layout-manager --save-current

# 出力例:
# 現在のディスプレイ構成を保存中...
# 検出されたディスプレイ: 3個
# ✓ パターン '3_Displays_37D8832A_3F816611_AE0F5F39' を作成しました
```

この機能の特徴：
- **自動パターン名生成**: Screen IDsから一意の名前を自動生成
- **自動上書き**: 同じディスプレイ構成が既に存在する場合は自動更新
- **現在設定の抽出**: displayplacerから現在の設定コマンドを自動抽出

## 常駐監視機能 🆕

Homebrew でインストールすると、常駐監視機能が自動的に有効化されます。ディスプレイ設定の変更を自動検知し、適切なレイアウトを自動適用します。

### 基本的な使用方法

```bash
# 常駐機能の状態確認
display-layout-manager --status-daemon

# 常駐機能を無効化
display-layout-manager --disable-daemon

# 常駐機能を再有効化
display-layout-manager --enable-daemon
```

### 常駐機能管理コマンド

```bash
# プロセス制御
display-layout-manager --start-daemon      # 手動開始
display-layout-manager --stop-daemon       # 手動停止
display-layout-manager --status-daemon     # 状態確認

# ログ管理
display-layout-manager --show-daemon-logs  # ログ表示
display-layout-manager --clear-daemon-logs # ログクリア

# 設定管理
display-layout-manager --daemon-config     # 設定表示
display-layout-manager --reload-daemon     # 設定リロード
```

### 常駐設定のカスタマイズ

常駐機能の設定は `~/Library/Application Support/DisplayLayoutManager/daemon.json` で管理されます：

```json
{
  "version": "1.0",
  "daemon": {
    "enabled": true,
    "debounce_delay": 2.0,
    "log_level": "INFO",
    "auto_execute": true
  },
  "monitoring": {
    "display_changes": true,
    "configuration_changes": true
  },
  "execution": {
    "command_timeout": 30,
    "retry_count": 2,
    "dry_run": false
  }
}
```

### 常駐機能の特徴

- **自動検知**: ミラーリング/拡張モード切り替え、ディスプレイ追加/削除を検知
- **デバウンス処理**: 連続するイベントを統合（デフォルト2秒、設定可能）
- **自動起動**: ログイン時に自動開始、クラッシュ時は自動再起動
- **設定リロード**: daemon.json の変更を自動検知してリロード
- **包括的ログ**: daemon.log と execution_history.log で動作履歴を記録

## ログとデバッグ

### ログファイル

- **場所**: `~/Library/Logs/DisplayLayoutManager/`
- **形式**: JSON 構造化ログ
- **ファイル種類**:
  - `display_layout_manager_YYYYMMDD.log` - 通常実行ログ（日次ローテーション）
  - `daemon.log` - 常駐プロセスのメインログ
  - `daemon_error.log` - 常駐プロセスのエラーログ
  - `execution_history.log` - 自動実行履歴

### デバッグオプション

```bash
# 詳細ログ表示
display-layout-manager --verbose

# 統合テスト実行
display-layout-manager --run-tests --verbose

# 設定ファイル検証
display-layout-manager --validate-config --verbose
```

## トラブルシューティング

### 依存関係の問題

**Homebrew が見つからない**
```bash
# Homebrew をインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# シェルを再起動またはパスを設定
eval "$(/opt/homebrew/bin/brew shellenv)"  # Apple Silicon Mac
eval "$(/usr/local/bin/brew shellenv)"     # Intel Mac
```

**displayplacer が見つからない**
```bash
# displayplacer をインストール
brew install jakehilborn/jakehilborn/displayplacer

# または手動でダウンロード
# https://github.com/jakehilborn/displayplacer/releases
```

**GNU grep が見つからない**
```bash
# GNU grep をインストール
brew install grep

# PATH を設定（必要に応じて）
export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"  # Apple Silicon Mac
export PATH="/usr/local/opt/grep/libexec/gnubin:$PATH"     # Intel Mac
```

### 常駐機能の問題

**常駐機能が動作しない**
```bash
# 状態を確認
display-layout-manager --status-daemon

# ログを確認
display-layout-manager --show-daemon-logs

# 再起動
display-layout-manager --disable-daemon
display-layout-manager --enable-daemon
```

**ディスプレイ変更が検知されない**
```bash
# 設定を確認
display-layout-manager --daemon-config

# 監視機能が有効か確認
# daemon.json の monitoring.display_changes が true であることを確認

# デバウンス時間を調整
# daemon.json の daemon.debounce_delay を変更（デフォルト: 2.0秒）
```

**自動実行されない**
```bash
# 自動実行が有効か確認
display-layout-manager --daemon-config

# daemon.json の daemon.auto_execute が true であることを確認
# 設定パターンが正しく定義されているか確認
display-layout-manager --validate-config
```

### 設定ファイルの問題

**JSON 構文エラー**
- オンライン JSON バリデーターを使用
- コンマ、括弧、引用符の対応を確認
- `--validate-config` オプションで詳細確認

**パターンが一致しない**
```bash
# 現在の Screen ID を確認
display-layout-manager --show-displays

# 設定ファイルの screen_ids を更新
# 完全一致が必要（順序は問わない）
```

### コマンド実行の問題

**displayplacer コマンドが失敗する**
- Screen ID が正しいか確認
- 解像度やリフレッシュレートが対応しているか確認
- `--dry-run` オプションでコマンドを事前確認

## 開発・貢献

### 開発環境セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/eijikominami/display-layout-manager.git
cd display-layout-manager

# 開発モードでインストール
pip install -e .

# 統合テスト実行
python -m src.display_layout_manager.main --run-tests
```

### テスト

```bash
# 統合テスト
display-layout-manager --run-tests --verbose

# 手動テスト
display-layout-manager --dry-run --verbose
display-layout-manager --show-displays
display-layout-manager --validate-config
```

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 貢献・サポート

- **バグ報告**: [GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues)
- **機能要望**: [GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues)
- **ドキュメント**: [GitHub Wiki](https://github.com/eijikominami/display-layout-manager/wiki)
- **変更履歴**: [CHANGELOG.md](CHANGELOG.md)

## 関連プロジェクト

- [displayplacer](https://github.com/jakehilborn/displayplacer) - macOS ディスプレイ設定ツール
- [Homebrew](https://brew.sh/) - macOS パッケージマネージャー