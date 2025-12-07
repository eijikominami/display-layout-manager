[**English**](configuration.md) / 日本語

# 設定ファイル詳細仕様

## 概要

Display Layout Manager は JSON 形式の設定ファイルを使用して、ディスプレイレイアウトパターンを管理します。このドキュメントでは、設定ファイルの詳細な仕様と高度な設定例を説明します。

## 設定ファイルの場所

### デフォルトの場所

```
~/Library/Application Support/DisplayLayoutManager/config.json
```

### 優先順位

設定ファイルは以下の優先順位で検索されます（高い順）：

1. **コマンドライン引数**: `--config /path/to/config.json`
2. **環境変数**: `DISPLAY_LAYOUT_CONFIG=/path/to/config.json`
3. **macOS デフォルト**: `~/Library/Application Support/DisplayLayoutManager/config.json`

### 設定例

```bash
# コマンドライン引数で指定
display-layout-manager --config ~/my-custom-config.json

# 環境変数で指定
export DISPLAY_LAYOUT_CONFIG=~/my-custom-config.json
display-layout-manager
```

## 設定ファイル構造

### 基本構造

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "パターン名",
      "description": "パターンの説明",
      "screen_ids": ["Screen ID 1", "Screen ID 2"],
      "command": "displayplacer コマンド"
    }
  ]
}
```

### フィールド詳細

#### version (必須)

- **型**: 文字列
- **説明**: 設定ファイルのバージョン
- **現在のバージョン**: `"1.0"`
- **用途**: 将来の互換性管理

```json
{
  "version": "1.0"
}
```

#### patterns (必須)

- **型**: 配列
- **説明**: ディスプレイレイアウトパターンのリスト
- **最小要素数**: 0（空配列も有効）
- **最大要素数**: 制限なし

```json
{
  "patterns": []
}
```

### パターンオブジェクト

#### name (必須)

- **型**: 文字列
- **説明**: パターンの一意な名前
- **制約**: 
  - 空文字列不可
  - 同じ名前のパターンは推奨されない（最後のものが優先）
- **推奨**: 分かりやすい名前を使用

```json
{
  "name": "Home Office Setup"
}
```

#### description (オプション)

- **型**: 文字列
- **説明**: パターンの詳細説明
- **用途**: ログ出力、ユーザーへの情報提供
- **推奨**: パターンの用途を明確に記載

```json
{
  "description": "メインディスプレイ + 外部モニター2台"
}
```

#### screen_ids (必須)

- **型**: 文字列の配列
- **説明**: Persistent Screen ID のリスト
- **制約**:
  - 空配列不可
  - 各要素は空文字列不可
  - 順序は問わない（セットとして比較）
- **取得方法**: `displayplacer list` または `display-layout-manager --show-displays`

```json
{
  "screen_ids": [
    "37D8832A-2D66-02CA-B9F7-8F30A301B230",
    "3F816611-C361-483F-8FB3-CE03208D949C"
  ]
}
```

#### command (必須)

- **型**: 文字列
- **説明**: 適用する displayplacer コマンド
- **制約**:
  - 空文字列不可
  - "displayplacer" で開始する必要がある
- **取得方法**: `displayplacer list` の出力から "Execute the command below" の次の行

```json
{
  "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\""
}
```

## 完全な設定例

### シングルディスプレイ

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
    }
  ]
}
```

### デュアルディスプレイ

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Dual Monitor Setup",
      "description": "ラップトップ + 外部モニター1台",
      "screen_ids": [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230",
        "3F816611-C361-483F-8FB3-CE03208D949C"
      ],
      "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\" \"id:3F816611-C361-483F-8FB3-CE03208D949C res:1920x1080 hz:120 color_depth:4 enabled:true scaling:off origin:(1470,0) degree:0\""
    }
  ]
}
```

### トリプルディスプレイ

```json
{
  "version": "1.0",
  "patterns": [
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

### 複数パターン

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
      "name": "Office Dual Monitor",
      "description": "オフィスのデュアルモニター",
      "screen_ids": [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230",
        "3F816611-C361-483F-8FB3-CE03208D949C"
      ],
      "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\" \"id:3F816611-C361-483F-8FB3-CE03208D949C res:1920x1080 hz:60 color_depth:4 enabled:true scaling:off origin:(1470,0) degree:0\""
    },
    {
      "name": "Home Triple Monitor",
      "description": "自宅のトリプルモニター",
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

## 設定ファイルの作成方法

### 方法1: 自動保存（推奨）

現在のディスプレイ構成を自動的に保存します：

```bash
# 現在のレイアウトを保存
display-layout-manager --save-current
```

この方法の利点：
- Screen ID の手動入力不要
- displayplacer コマンドの自動抽出
- パターン名の自動生成
- 既存パターンの自動上書き

### 方法2: 手動作成

1. **Screen ID を確認**
   ```bash
   display-layout-manager --show-displays
   ```

2. **displayplacer コマンドを取得**
   ```bash
   displayplacer list
   ```
   
   出力の "Execute the command below" の次の行をコピー

3. **設定ファイルを編集**
   ```bash
   open ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```

4. **パターンを追加**
   - `name`: 分かりやすい名前
   - `description`: パターンの説明
   - `screen_ids`: 手順1で確認した Screen ID
   - `command`: 手順2で取得したコマンド

5. **設定ファイルを検証**
   ```bash
   display-layout-manager --validate-config
   ```

## 設定ファイルの検証

### 検証コマンド

```bash
# 設定ファイルを検証
display-layout-manager --validate-config

# 詳細な検証結果を表示
display-layout-manager --validate-config --verbose
```

### 検証項目

1. **JSON 構文**: 有効な JSON 形式か
2. **必須フィールド**: `version`, `patterns` が存在するか
3. **パターン構造**: 各パターンに必須フィールドが存在するか
4. **screen_ids**: 空でない文字列の配列か
5. **command**: "displayplacer" で開始するか

### 検証エラー例

#### JSON 構文エラー

```
エラー: 設定ファイルの構文エラー
詳細: Expecting ',' delimiter: line 5 column 3 (char 123)

解決策:
  1. JSON バリデーターで構文を確認
  2. コンマ、括弧、引用符の対応を確認
```

#### 必須フィールド不足

```
エラー: 設定ファイルの検証エラー
詳細: パターン 'Home Office Setup' に必須フィールド 'command' がありません

解決策:
  1. パターンに 'command' フィールドを追加
  2. displayplacer list コマンドでコマンドを取得
```

## 高度な設定

### 環境変数の使用

```bash
# 開発環境用の設定
export DISPLAY_LAYOUT_CONFIG=~/dev-config.json

# 本番環境用の設定
export DISPLAY_LAYOUT_CONFIG=~/prod-config.json
```

### 複数の設定ファイル管理

```bash
# 設定ファイルのディレクトリ構造
~/display-configs/
├── home.json          # 自宅用
├── office.json        # オフィス用
└── presentation.json  # プレゼンテーション用

# 使用例
display-layout-manager --config ~/display-configs/home.json
display-layout-manager --config ~/display-configs/office.json
```

### バックアップと復元

```bash
# 設定ファイルをバックアップ
cp ~/Library/Application\ Support/DisplayLayoutManager/config.json \
   ~/Library/Application\ Support/DisplayLayoutManager/config.json.backup

# バックアップから復元
cp ~/Library/Application\ Support/DisplayLayoutManager/config.json.backup \
   ~/Library/Application\ Support/DisplayLayoutManager/config.json
```

## displayplacer コマンドの詳細

### コマンド構造

```
displayplacer "id:<Screen ID> res:<解像度> hz:<リフレッシュレート> color_depth:<色深度> enabled:<有効/無効> scaling:<スケーリング> origin:(<X座標>,<Y座標>) degree:<回転角度>"
```

### パラメータ詳細

#### id (必須)

- **説明**: Persistent Screen ID
- **形式**: UUID 形式の文字列
- **例**: `id:37D8832A-2D66-02CA-B9F7-8F30A301B230`

#### res (必須)

- **説明**: 解像度
- **形式**: `幅x高さ`
- **例**: `res:1920x1080`, `res:2560x1440`

#### hz (必須)

- **説明**: リフレッシュレート
- **形式**: 整数（Hz）
- **例**: `hz:60`, `hz:120`, `hz:144`

#### color_depth (必須)

- **説明**: 色深度
- **形式**: 整数（ビット）
- **例**: `color_depth:4`, `color_depth:8`

#### enabled (必須)

- **説明**: ディスプレイの有効/無効
- **値**: `true` または `false`
- **例**: `enabled:true`

#### scaling (必須)

- **説明**: スケーリングの有効/無効
- **値**: `on` または `off`
- **例**: `scaling:on`, `scaling:off`

#### origin (必須)

- **説明**: ディスプレイの位置座標
- **形式**: `(X座標,Y座標)`
- **例**: `origin:(0,0)`, `origin:(1920,0)`, `origin:(-1920,0)`

#### degree (必須)

- **説明**: ディスプレイの回転角度
- **値**: `0`, `90`, `180`, `270`
- **例**: `degree:0`, `degree:90`

### 複数ディスプレイの配置

#### 横並び配置

```json
{
  "command": "displayplacer \"id:SCREEN1 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(0,0) degree:0\" \"id:SCREEN2 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(1920,0) degree:0\""
}
```

#### 縦並び配置

```json
{
  "command": "displayplacer \"id:SCREEN1 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(0,0) degree:0\" \"id:SCREEN2 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(0,1080) degree:0\""
}
```

#### L字配置

```json
{
  "command": "displayplacer \"id:SCREEN1 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(0,0) degree:0\" \"id:SCREEN2 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(1920,0) degree:0\" \"id:SCREEN3 res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(0,1080) degree:0\""
}
```

## ファイル権限とセキュリティ

### 推奨権限

```bash
# 設定ディレクトリ
chmod 700 ~/Library/Application\ Support/DisplayLayoutManager/

# 設定ファイル
chmod 600 ~/Library/Application\ Support/DisplayLayoutManager/config.json
```

### セキュリティ考慮事項

- 設定ファイルには機密情報を含めない
- 他のユーザーからアクセスできないようにする
- バックアップファイルも同様の権限で保護する

## トラブルシューティング

設定ファイルに関する問題は、[トラブルシューティングガイド](troubleshooting.md) を参照してください。

## 関連ドキュメント

- [README_JP.md](../README_JP.md) - 基本的な使用方法
- [ARCHITECTURE_JP.md](../ARCHITECTURE_JP.md) - システムアーキテクチャ
- [トラブルシューティングガイド](troubleshooting_jp.md) - 問題解決方法
