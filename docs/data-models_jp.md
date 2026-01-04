[**English**](data-models.md) / 日本語

# データモデル

## 概要

Display Layout Manager は dataclass を使用して設定データとディスプレイ情報を表現します。このドキュメントでは、データ構造、変換ロジック、検証ルールについて説明します。

## コアデータモデル

### ConfigPattern

単一のディスプレイレイアウトパターンを表現します。

#### フィールド

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `name` | str | はい | パターン名（一意の識別子） |
| `description` | str | いいえ | パターンの説明（デフォルト: 空文字列） |
| `screen_ids` | List[str] | はい | Persistent Screen ID のリスト |
| `command` | str | はい | 実行する displayplacer コマンド |

#### 検証ルール

- `name`: 空でない文字列
- `screen_ids`: 空でない文字列のリスト
- `command`: "displayplacer" で開始する空でない文字列

#### Python 定義

```python
@dataclass
class ConfigPattern:
    """設定パターンクラス"""
    name: str
    description: str
    screen_ids: List[str]
    command: str

    def __post_init__(self):
        """初期化後の検証"""
        if not self.name:
            raise ValueError("パターン名は必須です")
        if not self.screen_ids:
            raise ValueError("screen_ids は必須です")
        if not self.command:
            raise ValueError("command は必須です")
        if not self.command.strip().startswith("displayplacer"):
            raise ValueError("command は 'displayplacer' で開始する必要があります")
```

#### JSON 表現

```json
{
  "name": "Home Office Setup",
  "description": "メインディスプレイ + 外部モニター2台",
  "screen_ids": [
    "37D8832A-2D66-02CA-B9F7-8F30A301B230",
    "3F816611-C361-483F-8FB3-CE03208D949C"
  ],
  "command": "displayplacer \"id:37D8832A...\""
}
```

### Configuration

設定ファイル全体の構造を表現します。

#### フィールド

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `version` | str | はい | 設定ファイル形式のバージョン |
| `patterns` | List[ConfigPattern] | はい | レイアウトパターンのリスト（最低1つ必要） |

#### 検証ルール

- `version`: 空でない文字列
- `patterns`: 空でない ConfigPattern オブジェクトのリスト

#### Python 定義

```python
@dataclass
class Configuration:
    """設定ファイル全体の構造"""
    version: str
    patterns: List[ConfigPattern]

    def __post_init__(self):
        """初期化後の検証"""
        if not self.version:
            raise ValueError("version は必須です")
        if not self.patterns:
            raise ValueError("patterns は必須です")
```

#### JSON 表現

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Pattern 1",
      "description": "説明",
      "screen_ids": ["ID1", "ID2"],
      "command": "displayplacer ..."
    }
  ]
}
```

### DisplayConfiguration

システムから検出された現在のディスプレイ構成を表現します。

#### フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `screen_ids` | List[str] | 検出された Persistent Screen ID のリスト |
| `raw_output` | str | displayplacer コマンドの生出力 |

#### Python 定義

```python
@dataclass
class DisplayConfiguration:
    """現在のディスプレイ構成"""
    screen_ids: List[str]
    raw_output: str
```

### MatchResult

パターンマッチング操作の結果を表現します。

#### フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `matched` | bool | パターンがマッチしたかどうか |
| `pattern` | Optional[ConfigPattern] | マッチしたパターン（マッチしない場合は None） |
| `match_type` | str | マッチのタイプ（"exact"、"partial"、または "none"） |
| `confidence` | int | 信頼度スコア（0-100） |
| `details` | str | 詳細なマッチング情報 |

#### Python 定義

```python
@dataclass
class MatchResult:
    """パターンマッチング結果"""
    matched: bool
    pattern: Optional[ConfigPattern]
    match_type: str
    confidence: int
    details: str
```

### ExecutionResult

コマンド実行の結果を表現します。

#### フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `success` | bool | コマンドが正常に実行されたかどうか |
| `pattern_name` | str | 実行されたパターンの名前 |
| `command` | str | 実行されたコマンド |
| `return_code` | int | コマンドの戻り値 |
| `stdout` | str | 標準出力 |
| `stderr` | str | 標準エラー出力 |
| `dry_run` | bool | ドライランだったかどうか |

#### Python 定義

```python
@dataclass
class ExecutionResult:
    """コマンド実行結果"""
    success: bool
    pattern_name: str
    command: str
    return_code: int
    stdout: str
    stderr: str
    dry_run: bool

    def get_summary(self) -> str:
        """実行結果のサマリーを取得"""
        # 実装の詳細...
```

## データ変換

### JSON から Python オブジェクトへ

設定ファイルは以下のプロセスで JSON から Python dataclass に変換されます：

1. **JSON パース**: `json.load()` を使用して JSON ファイルを読み込み
2. **構造検証**: 必須フィールドと型を検証
3. **オブジェクト作成**: JSON データから ConfigPattern オブジェクトを作成
4. **設定の組み立て**: パターンを含む Configuration オブジェクトを作成

#### 変換フロー

```
JSON ファイル
  ↓ json.load()
Dict[str, Any]
  ↓ validate_config_structure()
検証済み Dict
  ↓ 各パターンに対して ConfigPattern()
List[ConfigPattern]
  ↓ Configuration()
Configuration オブジェクト
```

#### 実装

```python
def load_config(self, config_path: Path) -> Tuple[bool, Optional[Configuration], List[str]]:
    """設定ファイルを読み込み"""
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    
    # 構造検証
    validation_errors = self.validate_config_structure(config_data)
    if validation_errors:
        return False, None, validation_errors
    
    # Configurationオブジェクトの作成
    patterns = []
    for pattern_data in config_data["patterns"]:
        pattern = ConfigPattern(
            name=pattern_data["name"],
            description=pattern_data.get("description", ""),
            screen_ids=pattern_data["screen_ids"],
            command=pattern_data["command"],
        )
        patterns.append(pattern)
    
    config = Configuration(version=config_data["version"], patterns=patterns)
    return True, config, []
```

### Python オブジェクトから JSON へ

設定を保存する際（例: `--save-current`）、Python オブジェクトは JSON に変換されます：

```python
def save_config(self, config_path: Path, config: Configuration) -> bool:
    """設定ファイルを保存"""
    config_data = {
        "version": config.version,
        "patterns": [
            {
                "name": p.name,
                "description": p.description,
                "screen_ids": p.screen_ids,
                "command": p.command,
            }
            for p in config.patterns
        ],
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    return True
```

## 検証ロジック

### 設定の検証

`ConfigManager.validate_config_structure()` メソッドは包括的な検証を実行します：

1. **トップレベルフィールド**: 必須の `version` と `patterns` フィールドを確認
2. **型チェック**: フィールドが正しい型であることを確認
3. **パターン検証**: 配列内の各パターンを検証
4. **フィールド要件**: 各パターンの必須フィールドを確認
5. **コマンド検証**: コマンドが "displayplacer" で開始することを確認

### パターンの検証

`PatternMatcher.validate_patterns()` メソッドは以下を確認します：

1. **重複名**: パターン名が一意であることを確認
2. **Screen ID 形式**: Screen ID の形式（UUID 形式）を検証
3. **コマンド構文**: displayplacer コマンドの基本構文を確認

## データフロー

### 設定読み込みフロー

```
1. 設定ファイルパスを決定（CLI 引数 > 環境変数 > デフォルト）
   ↓
2. ファイルの存在を確認
   ↓
3. JSON ファイルを読み込み
   ↓
4. JSON 構造を検証
   ↓
5. ConfigPattern オブジェクトを作成
   ↓
6. Configuration オブジェクトを作成
   ↓
7. ConfigManager に保存
```

### レイアウト保存フロー

```
1. 現在のディスプレイ構成を取得（DisplayManager）
   ↓
2. Screen ID とコマンドを抽出
   ↓
3. パターン名を生成
   ↓
4. 既存の設定を読み込み
   ↓
5. 重複する Screen ID セットを確認
   ↓
6. パターンを追加または更新
   ↓
7. JSON に変換
   ↓
8. ファイルに保存
```

## エラーハンドリング

### 検証エラー

全ての検証エラーはエラーメッセージのリストとして収集され、返されます：

```python
errors = [
    "必須フィールド 'version' が見つかりません",
    "パターン 1: 必須フィールド 'name' が見つかりません",
    "パターン 2: 'command' は 'displayplacer' で開始する必要があります"
]
```

### 例外処理

Dataclass の `__post_init__` メソッドは無効なデータに対して `ValueError` を発生させます：

```python
try:
    pattern = ConfigPattern(
        name="",  # 無効: 空の名前
        description="テスト",
        screen_ids=["ID1"],
        command="displayplacer ..."
    )
except ValueError as e:
    print(f"検証エラー: {e}")
```

## ベストプラクティス

### パターンの作成

1. **説明的な名前を使用**: "Pattern1" ではなく "Home Office Setup"
2. **説明を追加**: ユーザーが各パターンをいつ使用するかを理解できるようにする
3. **コマンドをテスト**: 保存前に displayplacer コマンドが動作することを確認
4. **--save-current を使用**: 現在のレイアウトから自動的にパターンを生成

### 設定管理

1. **使用前に検証**: `--validate-config` を使用して設定を確認
2. **設定のバックアップ**: 動作する設定のバックアップコピーを保持
3. **バージョン管理**: 設定の変更をバージョン管理で追跡
4. **パターンを文書化**: 各パターンに明確な説明を追加

### データ整合性

1. **不変パターン**: 作成後に ConfigPattern オブジェクトを変更しない
2. **読み込み時の検証**: 常に読み込み時に設定を検証
3. **エラーハンドリング**: 全ての検証エラーを適切に処理
4. **アトミック更新**: 破損を防ぐために設定をアトミックに保存
