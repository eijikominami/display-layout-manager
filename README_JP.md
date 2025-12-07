[**English**](README.md) / 日本語

# Display Layout Manager

[![Build](https://github.com/eijikominami/display-layout-manager/actions/workflows/test.yml/badge.svg)](https://github.com/eijikominami/display-layout-manager/actions/workflows/test.yml)
[![Release](https://github.com/eijikominami/display-layout-manager/actions/workflows/release.yml/badge.svg)](https://github.com/eijikominami/display-layout-manager/actions/workflows/release.yml)
[![Release Version](https://img.shields.io/github/v/release/eijikominami/display-layout-manager)](https://github.com/eijikominami/display-layout-manager/releases)
[![codecov](https://codecov.io/gh/eijikominami/display-layout-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/eijikominami/display-layout-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

macOS用のディスプレイレイアウト自動設定ツール

## 概要

Display Layout Manager は、macOS で複数のディスプレイ構成を自動的に管理するためのコマンドラインツールです。異なるディスプレイの組み合わせに応じて、事前に定義されたレイアウト設定を自動的に適用します。

## 主な機能

- **自動ディスプレイ検出**: 現在接続されているディスプレイの Persistent Screen ID を自動検出
- **パターンマッチング**: ディスプレイ構成に基づいて最適なレイアウトパターンを自動選択
- **設定ファイル管理**: JSON 形式の設定ファイルで複数のレイアウトパターンを管理
- **現在レイアウト保存**: `--save-current` で現在のディスプレイ構成を簡単保存
- **依存関係管理**: 必要なツールの自動インストールと確認
- **包括的なログ**: 構造化ログ出力とセッションサマリー
- **メニューバーアプリ**: macOS メニューバーから簡単に操作できる GUI
- **エラーハンドリング**: ユーザーフレンドリーなエラーメッセージとトラブルシューティングガイド
- **統合テスト**: 包括的なテストスイートによる品質保証

## システム要件

- **OS**: macOS 10.14 (Mojave) 以降
- **Python**: 3.8 以降
- **依存ツール**: Homebrew、displayplacer、GNU grep（自動インストール対応）

## 言語サポート

Display Layout Manager は **英語** と **日本語** のインターフェースをサポートしています。

### 自動言語検出

アプリケーションはシステムのロケール設定を自動的に検出し、適切な言語でメッセージを表示します：
- **日本語ロケール**（ja、ja_JP 等）: CLI とメニューバーアプリの全メッセージが日本語で表示
- **その他のロケール**: CLI とメニューバーアプリの全メッセージが英語で表示

### 手動言語切り替え

環境変数 `DISPLAY_LAYOUT_LANG` を使用して、自動言語検出を上書きできます：

```bash
# 英語インターフェースを強制
export DISPLAY_LAYOUT_LANG=en
display-layout-manager

# 日本語インターフェースを強制
export DISPLAY_LAYOUT_LANG=ja
display-layout-manager

# 一時的な上書き
DISPLAY_LAYOUT_LANG=en display-layout-manager --show-displays
```

### ログファイル

**注意**: ログファイルは、インターフェース言語に関係なく、常に英語で記録されます（技術的な記録のため）。これにより、デバッグやトラブルシューティングの一貫性が確保されます。

- **CLI/メニューバー出力**: 国際化対応（英語/日本語）
- **ログファイル**: 常に英語（`~/Library/Logs/DisplayLayoutManager/`）

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

### メニューバーアプリケーション（推奨）

macOS のメニューバーから簡単に操作できる GUI アプリケーションです。

```bash
# メニューバーアプリを起動
display-layout-menubar

# バックグラウンドで起動
display-layout-menubar &

# ログイン時の自動起動を有効化
display-layout-menubar --enable-auto-launch

# ログイン時の自動起動を無効化
display-layout-menubar --disable-auto-launch
```

#### メニューバーアプリの機能

メニューバーに ⧈ アイコンが表示され、以下の機能を提供します：

- **レイアウトを適用**: クリック一つで現在のディスプレイ構成に合ったレイアウトを適用
- **現在の設定を保存**: 現在のディスプレイ構成を設定ファイルに保存
- **✓ ログイン時に起動**: 自動起動の有効化・無効化を切り替え（チェックマークで状態表示）
- **終了**: メニューバーアプリを終了

操作結果はログファイル（`~/Library/Logs/DisplayLayoutManager/`）に記録されます。

### CLI コマンド

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

# ヘルプ表示
display-layout-manager --help
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

## ログとデバッグ

### ログファイル

- **場所**: `~/Library/Logs/DisplayLayoutManager/`
- **形式**: JSON 構造化ログ
- **ファイル種類**:
  - `display_layout_manager_YYYYMMDD.log` - 通常実行ログ（日次ローテーション）

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

### 開発環境のセットアップ

1. **開発依存関係のインストール**
   ```bash
   pip install -e ".[dev]"
   ```

2. **pre-commit フックのセットアップ**
   ```bash
   pre-commit install
   ```

   これにより、コミット前に以下のチェックが自動実行されます：
   - **Black**: コードフォーマット
   - **isort**: import 文の整理
   - **flake8**: Lint チェック
   - **末尾の空白削除**
   - **ファイル末尾の改行修正**
   - **YAML 検証**

3. **手動での pre-commit 実行**（オプション）
   ```bash
   # 全ファイルに対して実行
   pre-commit run --all-files

   # 特定のフックのみ実行
   pre-commit run black --all-files
   ```

### テスト

```bash
# 全テストスイートを実行（推奨）
python3 tests/run_all_tests.py

# テストカバレッジを測定
python3 tests/run_coverage.py
# HTML レポート: htmlcov/index.html

# CLI コンポーネント単体テスト
python3 tests/test_cli_components.py      # ConfigManager, PatternMatcher, CLIBridge
python3 tests/test_dependency_manager.py  # DependencyManager
python3 tests/test_display_manager.py     # DisplayManager
python3 tests/test_command_executor.py    # CommandExecutor
python3 tests/test_layout_saver.py        # LayoutSaver

# メニューバーアプリテスト
python3 tests/test_menubar_checkbox.py    # AutoLaunchManager
python3 tests/test_menubar_logic.py       # メニューバーロジック
python3 tests/test_menubar_integration.py # メニューバー統合テスト

# CLI 統合テスト
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
