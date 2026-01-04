[**English**](api-specification.md) / 日本語

# API 仕様書

## CLI コマンド

### display-layout-manager

ディスプレイレイアウト自動設定のメインコマンド。

#### 構文

```bash
display-layout-manager [OPTIONS]
```

#### オプション

| オプション | 型 | 説明 |
|-----------|-----|------|
| `--version` | フラグ | バージョンを表示して終了 |
| `--config PATH` | パス | 設定ファイルパス（デフォルト: `~/Library/Application Support/DisplayLayoutManager/config.json`） |
| `--verbose`, `-v` | フラグ | 詳細ログを有効化 |
| `--dry-run` | フラグ | ドライランモード（コマンドを実行しない） |
| `--show-displays` | フラグ | 現在のディスプレイ構成を表示して終了 |
| `--validate-config` | フラグ | 設定ファイルの検証のみ実行 |
| `--run-tests` | フラグ | 統合テストを実行 |
| `--save-current` | フラグ | 現在のディスプレイレイアウトをパターンとして保存 |

#### 終了コード

| コード | 意味 |
|--------|------|
| 0 | 成功 |
| 1 | 一般的なエラーまたはユーザー中断 |
| 2 | 設定ファイルエラー |
| 3 | ディスプレイ検出エラー |
| 4 | パターンマッチングエラー |
| 5 | コマンド実行エラー |
| 6 | 依存関係エラー |

#### 使用例

```bash
# 基本実行
display-layout-manager

# 現在のディスプレイを表示
display-layout-manager --show-displays

# 設定ファイルを検証
display-layout-manager --validate-config

# 詳細出力付きドライラン
display-layout-manager --dry-run --verbose

# 現在のレイアウトを保存
display-layout-manager --save-current

# 統合テストを実行
display-layout-manager --run-tests --verbose
```

### display-layout-menubar

GUI ベースのディスプレイレイアウト管理用メニューバーアプリケーション。

#### 構文

```bash
display-layout-menubar [OPTIONS]
```

#### オプション

| オプション | 型 | 説明 |
|-----------|-----|------|
| `--enable-auto-launch` | フラグ | ログイン時の自動起動を有効化 |
| `--disable-auto-launch` | フラグ | ログイン時の自動起動を無効化 |

#### メニュー項目

| 項目 | アクション |
|------|-----------|
| レイアウトを適用 | 現在のディスプレイ構成に一致するレイアウトを適用 |
| 現在の設定を保存 | 現在のディスプレイ構成を設定ファイルに保存 |
| ✓ ログイン時に起動 | 自動起動のオン/オフを切り替え（チェックマークは現在の状態を示す） |
| 終了 | メニューバーアプリを終了 |

#### 使用例

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

## 設定ファイル形式

### ファイル配置

設定ファイルは以下の優先順位で読み込まれます：

1. コマンドライン引数（`--config`）
2. 環境変数（`DISPLAY_LAYOUT_CONFIG`）
3. デフォルト位置（`~/Library/Application Support/DisplayLayoutManager/config.json`）

### JSON スキーマ

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "string (必須)",
      "description": "string (任意)",
      "screen_ids": ["string (必須、最低1つ)"],
      "command": "string (必須、'displayplacer' で開始)"
    }
  ]
}
```

### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `version` | string | はい | 設定ファイル形式のバージョン |
| `patterns` | array | はい | レイアウトパターンの配列（最低1つ必要） |
| `patterns[].name` | string | はい | パターン名（一意の識別子） |
| `patterns[].description` | string | いいえ | パターンの説明 |
| `patterns[].screen_ids` | array | はい | Persistent Screen ID の配列（最低1つ必要） |
| `patterns[].command` | string | はい | 実行する displayplacer コマンド |

### 検証ルール

1. **version**: 空でない文字列
2. **patterns**: 空でない配列
3. **patterns[].name**: 空でない文字列
4. **patterns[].screen_ids**: 空でない文字列の配列
5. **patterns[].command**: "displayplacer" で開始する文字列

### 設定例

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Laptop Only",
      "description": "ノートパソコンのみ使用",
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

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `DISPLAY_LAYOUT_CONFIG` | 設定ファイルパス | `~/Library/Application Support/DisplayLayoutManager/config.json` |
| `DISPLAY_LAYOUT_LANG` | インターフェース言語（`en` または `ja`） | システムロケールから自動検出 |

## 出力形式

### 標準出力

#### 成功時

```
Display Layout Manager v1.5.0 started
==================================================
Configuration file: /Users/username/Library/Application Support/DisplayLayoutManager/config.json
✓ Configuration loaded: 2 patterns

==================================================
Checking current display configuration...
✓ Displays detected: 3

==================================================
Pattern matching...
Pattern match result:
✓ Pattern matched: Home Office Setup
Match type: exact
Confidence: 100%

==================================================
Executing command...
✓ Command executed successfully

==================================================
Display Layout Manager completed successfully
```

#### エラー時

```
Display Layout Manager v1.5.0 started
==================================================
Configuration file: /Users/username/Library/Application Support/DisplayLayoutManager/config.json
✗ Configuration invalid
  - JSON構文エラー: Expecting ',' delimiter (行 5, 列 3)

エラー: CONFIG_SYNTAX_ERROR
設定ファイルにJSON構文エラーがあります

トラブルシューティング:
1. オンラインJSONバリデータで構文を確認してください
2. カンマ、括弧、引用符の不足を確認してください
3. --validate-config オプションで詳細な検証を実行してください
```

### ログファイル

ログファイルは `~/Library/Logs/DisplayLayoutManager/` に JSON 形式で出力されます。

#### ログエントリ形式

```json
{
  "timestamp": "2025-12-07T10:30:45.123456",
  "level": "INFO",
  "component": "display",
  "message": "Display detection started",
  "data": {}
}
```

#### ログレベル

| レベル | 説明 |
|--------|------|
| `DEBUG` | 詳細なデバッグ情報 |
| `INFO` | 一般的な情報メッセージ |
| `WARNING` | 警告メッセージ |
| `ERROR` | エラーメッセージ |
| `SUCCESS` | 成功メッセージ |

## 国際化

### 言語検出

アプリケーションはシステムロケールを自動検出し、適切な言語でメッセージを表示します：

- **日本語ロケール**（`ja`、`ja_JP` 等）: CLI とメニューバーのメッセージを日本語で表示
- **その他のロケール**: CLI とメニューバーのメッセージを英語で表示

### 言語オーバーライド

`DISPLAY_LAYOUT_LANG` 環境変数を使用して自動検出をオーバーライドできます：

```bash
# 英語を強制
export DISPLAY_LAYOUT_LANG=en
display-layout-manager

# 日本語を強制
export DISPLAY_LAYOUT_LANG=ja
display-layout-manager
```

### ログファイルの言語

ログファイルはインターフェース言語に関わらず、常に英語（技術的記録）で記録されます。

## エラーハンドリング

### エラーカテゴリ

| カテゴリ | 終了コード | 説明 |
|---------|-----------|------|
| 設定エラー | 2 | 設定ファイルの問題 |
| ディスプレイ検出エラー | 3 | ディスプレイ検出の失敗 |
| パターンマッチエラー | 4 | パターンマッチングの失敗 |
| コマンド実行エラー | 5 | displayplacer コマンドの失敗 |
| 依存関係エラー | 6 | 依存関係の不足 |

### エラーレスポンス形式

全てのエラーには以下が含まれます：
- エラーコード
- ユーザーフレンドリーなエラーメッセージ
- トラブルシューティング手順
- 関連するログファイルの場所

## 外部ツールとの連携

### displayplacer

Display Layout Manager は [displayplacer](https://github.com/jakehilborn/displayplacer) を使用してディスプレイ設定を行います。

#### 必要なコマンド

- `displayplacer list`: 現在のディスプレイ構成を取得
- `displayplacer <config>`: ディスプレイ構成を適用

### Homebrew

依存関係のインストールに使用：
- `brew --version`: Homebrew の利用可能性を確認
- `brew install <package>`: 依存関係をインストール

### GNU grep

テキスト処理に使用：
- `grep --version`: GNU grep の利用可能性を確認
