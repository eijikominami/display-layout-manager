# 設計書

## 概要

Display Layout Manager は macOS 用のディスプレイレイアウト自動設定アプリケーションです。接続されたディスプレイの組み合わせを検出し、設定ファイルで定義されたパターンにマッチした場合に対応する displayplacer コマンドを自動実行します。

## プロジェクト構造

### ディレクトリ構成

```
display-layout-manager/
├── src/
│   ├── display_layout_manager/
│   │   ├── __init__.py
│   │   ├── main.py              # エントリーポイント
│   │   ├── dependency_manager.py
│   │   ├── config_manager.py
│   │   ├── display_manager.py
│   │   ├── pattern_matcher.py
│   │   ├── command_executor.py
│   │   └── logger.py
│   └── tests/
│       ├── test_dependency_manager.py
│       ├── test_config_manager.py
│       └── ...
├── setup.py                     # Python パッケージ設定
├── requirements.txt             # Python 依存関係
├── README.md
└── Makefile                     # ビルド・インストール用
```

### 実行ファイルの配置と形式

#### 開発・配布形式
1. **Python パッケージ**: `pip install` でインストール可能
2. **スタンドアロン実行ファイル**: PyInstaller でバイナリ化
3. **Homebrew Formula**: Homebrew でのインストール対応

#### インストール場所

**Homebrew インストール（推奨）:**
```bash
# インストール
brew install display-layout-manager

# 実行ファイル場所
/opt/homebrew/bin/display-layout-manager  # Apple Silicon Mac
/usr/local/bin/display-layout-manager     # Intel Mac
```

**pip インストール:**
```bash
# インストール
pip install display-layout-manager

# 実行ファイル場所
~/.local/bin/display-layout-manager       # ユーザーインストール
/usr/local/bin/display-layout-manager     # システムインストール
```

**手動インストール:**
```bash
# 推奨場所
/usr/local/bin/display-layout-manager

# または
~/bin/display-layout-manager              # ユーザー専用
```

#### 実行ファイル形式

**Python スクリプト版:**
- ファイル: `display-layout-manager` (拡張子なし)
- Shebang: `#!/usr/bin/env python3`
- 実行権限: `755`

**バイナリ版（PyInstaller）:**
- ファイル: `display-layout-manager` (単一実行ファイル)
- サイズ: 約 10-15MB
- 依存関係: なし（Python ランタイム内蔵）

#### PATH 設定
```bash
# ~/.zshrc または ~/.bash_profile に追加
export PATH="/opt/homebrew/bin:$PATH"     # Homebrew
export PATH="~/.local/bin:$PATH"          # pip --user
export PATH="~/bin:$PATH"                 # 手動インストール
```

## アーキテクチャ

### システム構成

```
┌─────────────────────────────────────────────────────────────┐
│                Display Layout Manager                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Dependency      │  │ Configuration   │  │ Display      │ │
│  │ Manager         │  │ Manager         │  │ Manager      │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Pattern         │  │ Command         │  │ Logger       │ │
│  │ Matcher         │  │ Executor        │  │              │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    External Dependencies                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Homebrew        │  │ displayplacer   │  │ GNU grep     │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### コンポーネント設計

#### 1. Dependency Manager
- **責務**: 必要な外部ツールの存在確認とインストール
- **機能**:
  - Homebrew の存在確認
  - displayplacer の存在確認とインストール
  - GNU grep の存在確認とインストール
  - インストール失敗時のエラーハンドリング

#### 2. Configuration Manager
- **責務**: 設定ファイルの読み込みと管理
- **機能**:
  - 設定ファイル（JSON/YAML）の読み込み
  - 設定ファイルが存在しない場合のデフォルト作成
  - 設定ファイルの構文検証
  - 設定パターンの管理

#### 3. Display Manager
- **責務**: ディスプレイ情報の取得と管理
- **機能**:
  - `displayplacer list` コマンドの実行
  - Persistent Screen ID の抽出
  - 現在のディスプレイ構成の管理

#### 4. Pattern Matcher
- **責務**: ディスプレイ組み合わせのパターンマッチング
- **機能**:
  - 現在のディスプレイ構成と設定パターンの照合
  - 完全一致による最適パターンの選択
  - マッチ結果の管理

#### 5. Command Executor
- **責務**: displayplacer コマンドの実行
- **機能**:
  - displayplacer コマンドの実行
  - 実行結果の取得と処理
  - エラーハンドリング

#### 6. Logger
- **責務**: ログ出力とユーザーフィードバック
- **機能**:
  - 各段階の進捗表示
  - エラーメッセージの出力
  - 詳細ログオプション
  - 構造化ログ出力（JSON形式）
  - セッションサマリー生成
  - macOS標準ディレクトリへのログファイル出力

#### 7. Error Handler
- **責務**: 包括的なエラー処理とユーザーガイダンス
- **機能**:
  - カテゴリ別エラーコード管理
  - ユーザーフレンドリーなエラーメッセージ
  - 具体的な解決策の提示
  - 適切な終了コードの返却

#### 8. Integration Tester
- **責務**: 統合テストの実行と結果管理
- **機能**:
  - 各コンポーネントの動作テスト
  - エンドツーエンドテストの実行
  - テスト結果のサマリー表示
  - 失敗時の詳細診断情報提供

#### 9. Layout Saver
- **責務**: 現在のディスプレイレイアウトの保存機能
- **機能**:
  - 現在のディスプレイ構成の自動検出
  - Screen IDsからの一意パターン名生成
  - displayplacer listからの現在設定コマンド抽出
  - 既存パターンの自動上書き機能
  - 設定ファイルへの保存処理

## データモデル

### 設定ファイル構造（JSON形式）

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
    },
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

### 内部データ構造

#### DisplayConfiguration クラス
```python
@dataclass
class DisplayConfiguration:
    screen_ids: List[str]
    timestamp: datetime
    raw_output: str
```

#### ConfigPattern クラス
```python
@dataclass
class ConfigPattern:
    name: str
    description: str
    screen_ids: List[str]
    command: str
```

#### MatchResult クラス
```python
@dataclass
class MatchResult:
    matched: bool
    pattern: Optional[ConfigPattern]
    confidence: float
    match_type: str  # "exact", "partial", "none"
    details: str
```

#### ExecutionResult クラス
```python
@dataclass
class ExecutionResult:
    success: bool
    command: str
    pattern_name: str
    stdout: str
    stderr: str
    return_code: int
    execution_time: datetime
    dry_run: bool = False
```

#### LogEntry クラス
```python
@dataclass
class LogEntry:
    timestamp: str
    level: str  # "INFO", "WARNING", "ERROR", "SUCCESS"
    component: str  # "dependency", "config", "display", "pattern", "command"
    message: str
    details: Optional[Dict[str, Any]] = None
```

#### ErrorInfo クラス
```python
@dataclass
class ErrorInfo:
    category: ErrorCategory
    code: str
    message: str
    details: Optional[str] = None
    suggestions: Optional[List[str]] = None
    technical_details: Optional[str] = None
```

#### SaveResult クラス
```python
@dataclass
class SaveResult:
    success: bool
    pattern_name: str
    action: str  # "created", "updated"
    screen_count: int
    screen_ids: List[str]
    message: str
    error_details: Optional[str] = None
```

## インターフェース設計

### コマンドラインインターフェース

```bash
# 基本実行
display-layout-manager

# 詳細ログ付き実行
display-layout-manager --verbose

# 設定ファイル指定
display-layout-manager --config /path/to/config.json

# ドライラン（実際にコマンドを実行しない）
display-layout-manager --dry-run

# 現在のディスプレイ構成を表示
display-layout-manager --show-displays

# 設定ファイルの検証
display-layout-manager --validate-config

# 統合テストの実行
display-layout-manager --run-tests

# 現在のディスプレイレイアウトを保存
display-layout-manager --save-current

# ヘルプ表示
display-layout-manager --help
```

### 設定ファイルAPI

#### 設定ファイルの場所

**優先順位（高い順）:**
1. **コマンドライン引数**: `--config /path/to/config.json`
2. **環境変数**: `DISPLAY_LAYOUT_CONFIG=/path/to/config.json`
3. **macOS デフォルト**: `~/Library/Application Support/DisplayLayoutManager/config.json`

**macOS 標準ディレクトリ構造:**
- **設定ファイル**: `~/Library/Application Support/DisplayLayoutManager/config.json`
- **ログファイル**: `~/Library/Logs/DisplayLayoutManager/`
- **キャッシュ**: `~/Library/Caches/DisplayLayoutManager/`

**ディレクトリ作成:**
- アプリ初回実行時に `~/Library/Application Support/DisplayLayoutManager/` ディレクトリを自動作成
- 設定ファイルが存在しない場合、サンプル設定を含むデフォルトファイルを作成

**ファイル権限:**
- 設定ファイル: `600` (所有者のみ読み書き可能)
- ディレクトリ: `700` (所有者のみアクセス可能)

**macOS 統合:**
- Finder での設定ファイルアクセス: `~/Library/Application Support/DisplayLayoutManager/`
- システム環境設定との連携を考慮した設計

#### 設定ファイルの検証ルール
1. **必須フィールド**: `version`, `patterns`
2. **パターン必須フィールド**: `name`, `screen_ids`, `command`
3. **screen_ids**: 空でない文字列の配列
4. **command**: 空でない文字列で "displayplacer" で開始

## エラーハンドリング

### エラー分類と対応

#### 1. 依存関係エラー (ErrorCategory.DEPENDENCY)
- **HOMEBREW_NOT_FOUND**: インストール手順を表示
- **DISPLAYPLACER_NOT_FOUND**: 自動インストール試行
- **GNU_GREP_NOT_FOUND**: 自動インストール試行

#### 2. 設定ファイルエラー (ErrorCategory.CONFIG)
- **CONFIG_FILE_NOT_FOUND**: デフォルト設定ファイル作成
- **CONFIG_SYNTAX_ERROR**: 詳細な構文エラー位置の表示
- **CONFIG_VALIDATION_ERROR**: 必須フィールド不足や無効な値の明示

#### 3. ディスプレイ検出エラー (ErrorCategory.DISPLAY)
- **DISPLAY_DETECTION_FAILED**: コマンド実行エラーの詳細表示
- **NO_DISPLAYS_FOUND**: Screen ID抽出失敗の詳細

#### 4. パターンマッチングエラー (ErrorCategory.PATTERN)
- **NO_PATTERN_MATCH**: マッチするパターンなしの詳細情報

#### 5. コマンド実行エラー (ErrorCategory.COMMAND)
- **COMMAND_EXECUTION_FAILED**: 終了コードとエラー出力の表示
- **COMMAND_TIMEOUT**: タイムアウト時の処理

#### 6. システムエラー (ErrorCategory.SYSTEM)
- **PERMISSION_DENIED**: 権限エラーの説明
- **UNEXPECTED_ERROR**: 予期しないエラーの処理

### エラーコード体系

各エラーには以下の情報が含まれます：
- **エラーコード**: 一意の識別子
- **カテゴリ**: エラーの分類
- **メッセージ**: ユーザー向けの説明
- **詳細**: 技術的な詳細情報
- **解決策**: 具体的な対処方法のリスト
- **終了コード**: プロセス終了時の適切なコード

### エラーハンドリング実装

```python
class ErrorHandler:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.error_catalog = self._build_error_catalog()
    
    def handle_error(self, error_code: str, context: Optional[Dict[str, Any]] = None, 
                    exception: Optional[Exception] = None) -> None:
        """エラーを処理して表示"""
        error_info = self.get_error_info(error_code)
        
        # エラーメッセージの表示
        print(f"\nエラー: {error_info.message}", file=sys.stderr)
        
        if error_info.details:
            print(f"詳細: {error_info.details}", file=sys.stderr)
        
        # 解決策の表示
        if error_info.suggestions:
            print("\n解決策:", file=sys.stderr)
            for i, suggestion in enumerate(error_info.suggestions, 1):
                print(f"  {i}. {suggestion}", file=sys.stderr)
    
    def get_exit_code(self, error_code: str) -> int:
        """エラーコードに対応する終了コードを取得"""
        exit_codes = {
            "HOMEBREW_NOT_FOUND": 2,
            "DISPLAYPLACER_NOT_FOUND": 2,
            "CONFIG_FILE_NOT_FOUND": 3,
            "DISPLAY_DETECTION_FAILED": 4,
            "NO_PATTERN_MATCH": 5,
            "COMMAND_EXECUTION_FAILED": 6,
            "PERMISSION_DENIED": 7,
            "UNEXPECTED_ERROR": 1
        }
        return exit_codes.get(error_code, 1)
```

## テスト戦略

### 単体テスト

#### 1. Dependency Manager テスト
- Homebrew 存在確認のモック
- displayplacer インストールのモック
- エラーケースのテスト

#### 2. Configuration Manager テスト
- 有効な設定ファイルの読み込み
- 無効な設定ファイルのエラーハンドリング
- デフォルト設定ファイル作成

#### 3. Display Manager テスト
- displayplacer コマンド出力の解析
- Screen ID 抽出の正確性
- エラー出力の処理

#### 4. Pattern Matcher テスト
- 完全一致パターンマッチング
- 部分一致の除外
- 複数パターンの優先順位

#### 5. Command Executor テスト
- 成功ケースの処理
- 失敗ケースのエラーハンドリング
- ドライランモードの動作

### 統合テスト

#### 1. 統合テストスイート（--run-tests）
- **依存関係管理テスト**: Homebrew、displayplacer、GNU grepの確認
- **設定ファイル管理テスト**: 有効・無効な設定ファイルの処理
- **ディスプレイ検出テスト**: displayplacerコマンドの実行と解析
- **パターンマッチングテスト**: 完全一致・部分一致・不一致のテスト
- **コマンド実行テスト**: ドライランモードでの実行テスト
- **ログシステムテスト**: 各レベルのログ出力テスト

#### 2. エンドツーエンドテスト
- 実際のディスプレイ環境でのテスト
- 設定ファイルから実行までの全フロー
- 異なるディスプレイ構成でのテスト

#### 3. エラーシナリオテスト
- 依存関係不足時の動作
- 無効な設定ファイルでの動作
- ネットワーク接続問題時の動作

#### 4. テスト結果管理
```python
@dataclass
class TestResult:
    test_name: str
    success: bool
    message: str
    details: Dict[str, Any]
    execution_time: float

class IntegrationTester:
    def run_all_tests(self) -> List[TestResult]:
        """全テストを実行"""
        # 各テストを実行してTestResultを収集
        
    def get_test_summary(self) -> Dict[str, Any]:
        """テストサマリーを取得"""
        # 成功率、実行時間等の統計情報を返却
```

### テストデータ

#### モックディスプレイ出力
```
Resolution: 1470x956
Framerate: 60
Color Depth: 8
Scaling:on
Origin: (0,0) - main display
Rotation: 0
Persistent screen id: 37D8832A-2D66-02CA-B9F7-8F30A301B230

Resolution: 1920x1080
Framerate: 120
Color Depth: 4
Scaling:off
Origin: (-1278,-1080)
Rotation: 0
Persistent screen id: 3F816611-C361-483F-8FB3-CE03208D949C
```

## パフォーマンス考慮事項

### 実行時間最適化
- **キャッシュ戦略**: ディスプレイ情報の短期キャッシュ
- **並列処理**: 依存関係チェックの並列実行
- **遅延読み込み**: 設定ファイルの必要時読み込み

### メモリ使用量
- **軽量データ構造**: 必要最小限のデータ保持
- **ストリーミング処理**: 大きなコマンド出力の逐次処理

### 起動時間
- **高速起動**: 不要な初期化処理の削減
- **依存関係の最適化**: 必要な場合のみ外部コマンド実行

## セキュリティ考慮事項

### コマンドインジェクション対策
- **入力検証**: 設定ファイルの displayplacer コマンドの検証
- **ホワイトリスト**: 許可されたコマンドパターンの制限
- **エスケープ処理**: シェルコマンド実行時の適切なエスケープ

### ファイルシステムアクセス
- **権限制限**: 必要最小限のファイルアクセス権限
- **パス検証**: 設定ファイルパスの検証
- **一時ファイル**: 安全な一時ファイル作成

### 外部コマンド実行
- **コマンド検証**: 実行前のコマンド妥当性チェック
- **タイムアウト**: 長時間実行の防止
- **出力制限**: 大量出力による DoS 攻撃の防止

## 運用・保守

### ログ管理
- **ログレベル**: INFO, SUCCESS, WARNING, ERROR
- **ログ形式**: JSON構造化ログ
- **ログローテーション**: 日次ローテーション（ファイル名に日付含む）
- **ログ場所**: `~/Library/Logs/DisplayLayoutManager/display_layout_manager_YYYYMMDD.log`
- **セッションサマリー**: 実行終了時の統計情報表示
- **コンポーネント別ログ**: dependency, config, display, pattern, command, system

### 設定管理
- **バージョン管理**: 設定ファイルのバージョン互換性
- **マイグレーション**: 古い設定形式からの自動変換
- **バックアップ**: 設定変更前の自動バックアップ

### 監視・診断
- **ヘルスチェック**: 依存関係の定期確認
- **診断モード**: 詳細な動作状況の出力
- **トラブルシューティング**: 一般的な問題の自動診断

## 現在レイアウト保存機能

### パターン名生成アルゴリズム

```python
def generate_pattern_name(self, screen_ids: List[str]) -> str:
    """Screen IDsからユニークなパターン名を生成"""
    # Screen IDsをソートして一貫性を保つ
    sorted_ids = sorted(screen_ids)
    
    # 各IDの最初の8文字を使用
    short_ids = [sid[:8] for sid in sorted_ids]
    
    # ディスプレイ数とIDの組み合わせでパターン名を作成
    display_count = len(screen_ids)
    if display_count == 1:
        return f"Single_Display_{short_ids[0]}"
    else:
        # 複数ディスプレイの場合
        id_hash = "_".join(short_ids)
        return f"{display_count}_Displays_{id_hash}"
```

### 現在設定コマンド抽出

```python
def extract_current_command(self, displayplacer_output: str) -> str:
    """displayplacer listの出力から現在の設定コマンドを抽出"""
    lines = displayplacer_output.split('\n')
    for i, line in enumerate(lines):
        if "Execute the command below" in line:
            # 次の行がコマンド
            if i + 1 < len(lines):
                return lines[i + 1].strip()
    return ""
```

### 保存処理フロー

1. **現在構成の検出**: `displayplacer list` 実行
2. **Screen IDs抽出**: 正規表現でPersistent Screen ID抽出
3. **パターン名生成**: Screen IDsから一意名を生成
4. **既存パターン確認**: 同じScreen IDsのパターンをチェック
5. **設定コマンド抽出**: displayplacer出力から現在コマンドを取得
6. **設定ファイル更新**: 新規追加または既存パターン上書き
7. **結果表示**: 保存結果をユーザーに通知

### 使用例

```bash
# 現在のレイアウトを保存
$ display-layout-manager --save-current

# 出力例（新規作成）:
# 現在のディスプレイ構成を保存中...
# 検出されたディスプレイ: 3個
#   - 37D8832A-2D66-02CA-B9F7-8F30A301B230
#   - 3F816611-C361-483F-8FB3-CE03208D949C  
#   - AE0F5F39-5D5C-4FF1-A7BA-8E5CBE679211
# ✓ パターン "3_Displays_37D8832A_3F816611_AE0F5F39" として保存しました

# 出力例（既存更新）:
# 現在のディスプレイ構成を保存中...
# 検出されたディスプレイ: 3個
# ✓ パターン "3_Displays_37D8832A_3F816611_AE0F5F39" を更新しました
```

## パッケージング・配布

### Python パッケージ構造
```
display-layout-manager/
├── src/
│   └── display_layout_manager/
│       ├── __init__.py              # バージョン情報
│       ├── main.py                  # エントリーポイント
│       ├── dependency_manager.py
│       ├── config_manager.py
│       ├── display_manager.py
│       ├── pattern_matcher.py
│       ├── command_executor.py
│       ├── logger.py
│       ├── error_handler.py
│       ├── integration_test.py
│       └── layout_saver.py
├── setup.py                         # setuptools設定
├── pyproject.toml                   # モダンなパッケージング設定
├── MANIFEST.in                      # パッケージ含有ファイル指定
├── LICENSE                          # MIT License
├── CHANGELOG.md                     # 変更履歴
├── README.md                        # ドキュメント
└── Formula/
    └── display-layout-manager.rb    # Homebrew Formula
```

### 配布方法
1. **Homebrew Tap**: `brew tap eijikominami/display-layout-manager && brew install display-layout-manager`
2. **PyPI パッケージ**: `pip install display-layout-manager` (将来対応)
3. **GitHub Releases**: ソースコード配布（自動生成）

### CI/CD パイプライン設計

#### GitHub Actions ワークフロー
```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  test:     # macOS環境でのテスト実行
  release:  # GitHub Release自動作成
  update-homebrew: # Homebrew Formula自動更新
```

#### リリースフロー
1. **開発者**: バージョンタグをプッシュ (`git tag v1.0.1 && git push origin v1.0.1`)
2. **自動テスト**: macOS環境での統合テスト実行
3. **自動リリース**: GitHub Release作成、SHA256計算
4. **自動更新**: Homebrew Formula更新、Tap更新
5. **通知**: 成功/失敗の通知

#### Homebrew Tap 構造
```
homebrew-display-layout-manager/
├── Formula/
│   └── display-layout-manager.rb
├── README.md
└── .github/
    └── workflows/
        └── tests.yml
```

### インストール後の設定
- 設定ディレクトリ自動作成: `~/Library/Application Support/DisplayLayoutManager/`
- ログディレクトリ自動作成: `~/Library/Logs/DisplayLayoutManager/`
- 適切なファイル権限設定（700/600）

### CI/CD での Homebrew テスト

#### プルリクエスト時の自動テスト

GitHub Actions でプルリクエスト時に Homebrew Formula のインストールテストを実行します。

```yaml
# .github/workflows/test.yml
jobs:
  homebrew-test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create temporary Homebrew tap
        run: |
          mkdir -p /tmp/homebrew-test/Formula
          
      - name: Create test Formula
        run: |
          # 現在のソースコードをアーカイブ
          tar czf /tmp/test-source.tar.gz --exclude='.git' .
          SHA256=$(shasum -a 256 /tmp/test-source.tar.gz | cut -d' ' -f1)
          
          # テスト用 Formula を作成
          cat > /tmp/homebrew-test/Formula/display-layout-manager.rb << EOF
          class DisplayLayoutManager < Formula
            # ... Formula の内容 ...
            url "file:///tmp/test-source.tar.gz"
            sha256 "$SHA256"
          end
          EOF
      
      - name: Install from local Formula
        run: |
          brew install --build-from-source /tmp/homebrew-test/Formula/display-layout-manager.rb
      
      - name: Verify CLI installation
        run: |
          which display-layout-manager
          display-layout-manager --version
      
      - name: Verify menubar app installation
        run: |
          which display-layout-menubar
          display-layout-menubar --help || true
      
      - name: Run integration tests
        run: |
          display-layout-manager --run-tests
```

#### テストの目的

1. **エントリーポイント検証**: すべてのコマンドが正しく作成されることを確認
2. **依存関係検証**: Python パッケージが正しくインストールされることを確認
3. **基本機能検証**: `--version`, `--help`, `--run-tests` が動作することを確認
4. **早期問題発見**: リリース前に Homebrew インストールの問題を検出

### テストカバレッジの測定と可視化

#### Codecov 統合

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: macos-latest
    steps:
      - name: Run tests with coverage
        run: |
          pip install coverage
          coverage run -m pytest
          coverage xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
```

#### README バッジ

```markdown
[![Build](https://github.com/eijikominami/display-layout-manager/actions/workflows/test.yml/badge.svg)](https://github.com/eijikominami/display-layout-manager/actions/workflows/test.yml)
[![Release](https://github.com/eijikominami/display-layout-manager/actions/workflows/release.yml/badge.svg)](https://github.com/eijikominami/display-layout-manager/actions/workflows/release.yml)
[![Release Version](https://img.shields.io/github/v/release/eijikominami/display-layout-manager)](https://github.com/eijikominami/display-layout-manager/releases)
[![codecov](https://codecov.io/gh/eijikominami/display-layout-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/eijikominami/display-layout-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
```

## ドキュメント構造

### ドキュメント階層

```
display-layout-manager/
├── README.md                    # プロジェクト概要、基本的な使用方法（英語）
├── README_JP.md                 # プロジェクト概要、基本的な使用方法（日本語）
├── ARCHITECTURE.md              # システムアーキテクチャ、設計原則（英語）
├── ARCHITECTURE_JP.md           # システムアーキテクチャ、設計原則（日本語）
├── CHANGELOG.md                 # 変更履歴
├── LICENSE                      # ライセンス情報
└── docs/
    ├── configuration.md         # 設定ファイル詳細仕様（英語）
    ├── configuration_jp.md      # 設定ファイル詳細仕様（日本語）
    ├── troubleshooting.md       # トラブルシューティングガイド（英語）
    └── troubleshooting_jp.md    # トラブルシューティングガイド（日本語）
```

### ドキュメントの役割

#### README.md / README_JP.md
- **対象**: すべてのユーザー
- **言語**: 英語（README.md）/ 日本語（README_JP.md）
- **内容**:
  - プロジェクト概要
  - 主な機能
  - インストール方法
  - 基本的な使用方法
  - 簡単なトラブルシューティング
  - バッジによる品質の可視化
- **言語切り替え**: 各ドキュメントの冒頭にリンクを配置

#### ARCHITECTURE.md / ARCHITECTURE_JP.md
- **対象**: 開発者、コントリビューター
- **言語**: 英語（ARCHITECTURE.md）/ 日本語（ARCHITECTURE_JP.md）
- **内容**:
  - システムアーキテクチャ図
  - コンポーネント詳細
  - データフロー
  - 設計原則
  - テスト戦略
  - パフォーマンス考慮事項
- **言語切り替え**: 各ドキュメントの冒頭にリンクを配置

#### docs/configuration.md / docs/configuration_jp.md
- **対象**: 高度な設定を行うユーザー
- **言語**: 英語（configuration.md）/ 日本語（configuration_jp.md）
- **内容**:
  - 設定ファイルの完全な仕様
  - すべてのフィールドの詳細説明
  - 高度な設定例
  - displayplacer コマンドの詳細
  - 複数ディスプレイの配置パターン
- **言語切り替え**: 各ドキュメントの冒頭にリンクを配置

#### docs/troubleshooting.md / docs/troubleshooting_jp.md
- **対象**: 問題に直面したユーザー
- **言語**: 英語（troubleshooting.md）/ 日本語（troubleshooting_jp.md）
- **内容**:
  - カテゴリ別の問題と解決策
  - 詳細なエラーメッセージの説明
  - ステップバイステップの解決手順
  - ログとデバッグ方法
  - よくある質問 (FAQ)
- **言語切り替え**: 各ドキュメントの冒頭にリンクを配置

### ドキュメント間の相互参照

各ドキュメントは相互にリンクし、ユーザーが必要な情報に簡単にアクセスできるようにします：

- README.md / README_JP.md → ARCHITECTURE.md / ARCHITECTURE_JP.md, docs/configuration.md / docs/configuration_jp.md, docs/troubleshooting.md / docs/troubleshooting_jp.md
- ARCHITECTURE.md / ARCHITECTURE_JP.md → README.md / README_JP.md, docs/configuration.md / docs/configuration_jp.md
- docs/configuration.md / docs/configuration_jp.md → README.md / README_JP.md, ARCHITECTURE.md / ARCHITECTURE_JP.md, docs/troubleshooting.md / docs/troubleshooting_jp.md
- docs/troubleshooting.md / docs/troubleshooting_jp.md → README.md / README_JP.md, ARCHITECTURE.md / ARCHITECTURE_JP.md, docs/configuration.md / docs/configuration_jp.md

### ドキュメント国際化戦略

#### 言語切り替えリンク形式

**英語版ドキュメント:**
```markdown
English / [**日本語**](filename_JP.md)
```

**日本語版ドキュメント:**
```markdown
[**English**](filename.md) / 日本語
```

#### 命名規則
- **英語版**: `filename.md`（拡張子なし）
- **日本語版**: `filename_JP.md`（`_JP` サフィックス）

#### 内容の同期
- 英語版を基本言語として管理
- 日本語版は英語版の翻訳として作成
- 機能追加・変更時は両言語を同時に更新
- 内部リンクは各言語版の対応するファイルを参照

## メニューバーアプリケーション

### 概要

macOS のメニューバー（Status Bar）に常駐し、クリック操作だけでディスプレイレイアウトの適用と保存ができる GUI アプリケーションです。CLI 機能と並行して動作し、ユーザーに直感的な操作方法を提供します。

### アーキテクチャ

#### 技術スタック
- **GUI フレームワーク**: `rumps` (Ridiculously Uncomplicated macOS Python Statusbar apps)
- **バックエンド**: 既存の CLI コンポーネントを再利用
- **通知**: macOS Notification Center (`pync` または `osascript`)
- **プロセス管理**: バックグラウンドプロセスとして動作

#### コンポーネント構成

```
┌─────────────────────────────────────────────────────────────┐
│                  Menu Bar Application                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Status Bar      │  │ Menu Manager    │  │ Notification │ │
│  │ Controller      │  │                 │  │ Manager      │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Action Handler  │  │ CLI Bridge      │  │ Auto Launch  │ │
│  │                 │  │                 │  │ Manager      │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│              Existing CLI Components (Reused)                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Display Manager │  │ Pattern Matcher │  │ Layout Saver │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### コンポーネント設計

#### 1. Status Bar Controller
- **責務**: メニューバーアイコンの管理
- **機能**:
  - アイコンの表示・更新
  - メニューの表示制御
  - アプリケーションライフサイクル管理

```python
import rumps

class DisplayLayoutMenuBar(rumps.App):
    def __init__(self):
        super(DisplayLayoutMenuBar, self).__init__(
            "Display Layout Manager",
            icon="icon.png",  # メニューバーアイコン
            quit_button=None  # カスタム終了ボタンを使用
        )
        self.menu = self._build_menu()
```

#### 2. Menu Manager
- **責務**: メニュー項目の構築と管理
- **機能**:
  - メニュー項目の動的生成
  - メニュー状態の更新
  - サブメニューの管理

```python
def _build_menu(self):
    """メニュー構造を構築"""
    # 自動起動メニュー項目（チェックマーク付き）
    auto_launch_item = rumps.MenuItem(
        "ログイン時に起動",
        callback=self.toggle_auto_launch
    )
    # 現在の状態を反映
    auto_launch_item.state = self.auto_launch_manager.is_enabled()
    
    return [
        rumps.MenuItem("レイアウトを適用", callback=self.apply_layout),
        rumps.MenuItem("現在の設定を保存", callback=self.save_current),
        rumps.separator,
        auto_launch_item,
        rumps.separator,
        rumps.MenuItem("終了", callback=self.quit_application)
    ]
```

#### 3. Action Handler
- **責務**: ユーザーアクションの処理
- **機能**:
  - メニュー項目クリック時の処理
  - バックグラウンドでの CLI 実行
  - 結果の通知表示

```python
@rumps.clicked("レイアウトを適用")
def apply_layout(self, _):
    """レイアウト適用アクション"""
    try:
        # バックグラウンドで CLI を実行
        result = self.cli_bridge.execute_apply_layout()
        
        # 通知は表示しない（サイレント実行）
        # ログファイルには記録される
    except Exception as e:
        # エラー時もサイレント（ログのみ）
        pass

@rumps.clicked("現在の設定を保存")
def save_current(self, _):
    """現在の設定保存アクション"""
    try:
        result = self.cli_bridge.execute_save_current()
        
        # 通知は表示しない（サイレント実行）
        # ログファイルには記録される
    except Exception as e:
        # エラー時もサイレント（ログのみ）
        pass

@rumps.clicked("ログイン時に起動")
def toggle_auto_launch(self, sender):
    """自動起動の切り替えアクション"""
    try:
        if self.auto_launch_manager.is_enabled():
            # 無効化
            self.auto_launch_manager.disable()
            sender.state = False
        else:
            # 有効化
            self.auto_launch_manager.enable()
            sender.state = True
        
        # 通知は表示しない（チェックマークで状態を表示）
    except Exception as e:
        # エラー時もサイレント（ログのみ）
        pass

@rumps.clicked("終了")
def quit_application(self, _):
    """アプリケーション終了アクション"""
    rumps.quit_application()
                result.error_message
            )
    except Exception as e:
        self.notification_manager.show_error(
            "エラーが発生しました",
            str(e)
        )
```

#### 4. CLI Bridge
- **責務**: CLI コンポーネントとの連携
- **機能**:
  - 既存 CLI 機能の呼び出し
  - 結果の変換と返却
  - エラーハンドリング

```python
class CLIBridge:
    def __init__(self):
        # 既存のCLIコンポーネントを初期化
        self.display_manager = DisplayManager()
        self.pattern_matcher = PatternMatcher()
        self.layout_saver = LayoutSaver()
        self.command_executor = CommandExecutor()
    
    def execute_apply_layout(self) -> ActionResult:
        """レイアウト適用を実行"""
        try:
            # 現在のディスプレイ構成を取得
            current_config = self.display_manager.get_current_configuration()
            
            # パターンマッチング
            match_result = self.pattern_matcher.find_match(current_config)
            
            if not match_result.matched:
                return ActionResult(
                    success=False,
                    error_message="一致するパターンが見つかりません"
                )
            
            # コマンド実行
            exec_result = self.command_executor.execute(match_result.pattern.command)
            
            return ActionResult(
                success=exec_result.success,
                pattern_name=match_result.pattern.name,
                error_message=exec_result.stderr if not exec_result.success else None
            )
        except Exception as e:
            return ActionResult(success=False, error_message=str(e))
    
    def execute_save_current(self) -> ActionResult:
        """現在の設定を保存"""
        try:
            save_result = self.layout_saver.save_current_layout()
            
            return ActionResult(
                success=save_result.success,
                pattern_name=save_result.pattern_name,
                error_message=save_result.error_details
            )
        except Exception as e:
            return ActionResult(success=False, error_message=str(e))
```

#### 5. Auto Launch Manager
- **責務**: ログイン時の自動起動管理
- **機能**:
  - LaunchAgent plist の作成・削除
  - 自動起動の有効化・無効化
  - 現在の状態確認

```python
import os
import plistlib
from pathlib import Path

class AutoLaunchManager:
    def __init__(self):
        self.launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
        self.plist_path = self.launch_agents_dir / "com.eijikominami.display-layout-manager.plist"
    
    def is_enabled(self) -> bool:
        """自動起動が有効かチェック"""
        return self.plist_path.exists()
    
    def enable(self):
        """自動起動を有効化"""
        # LaunchAgentsディレクトリを作成
        self.launch_agents_dir.mkdir(parents=True, exist_ok=True)
        
        # plistファイルを作成
        plist_data = {
            "Label": "com.eijikominami.display-layout-manager",
            "ProgramArguments": [
                "/opt/homebrew/bin/display-layout-manager-menubar"
            ],
            "RunAtLoad": True,
            "KeepAlive": False
        }
        
        with open(self.plist_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        
        # launchctl に登録
        subprocess.run(["launchctl", "load", str(self.plist_path)])
    
    def disable(self):
        """自動起動を無効化"""
        if self.plist_path.exists():
            # launchctl から削除
            subprocess.run(["launchctl", "unload", str(self.plist_path)])
            # plistファイルを削除
            self.plist_path.unlink()
```

### データモデル

#### ActionResult クラス
```python
@dataclass
class ActionResult:
    success: bool
    pattern_name: Optional[str] = None
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
```

### インターフェース設計

#### メニュー構造

```
┌─────────────────────────────────┐
│ 🖥️ Display Layout Manager      │
├─────────────────────────────────┤
│ レイアウトを適用                │
│ 現在の設定を保存                │
├─────────────────────────────────┤
│ 接続されたディスプレイ          │
├─────────────────────────────────┤
│ ✓ ログイン時に起動              │
├─────────────────────────────────┤
│ 終了                            │
└─────────────────────────────────┘
```

#### コマンドライン起動

```bash
# メニューバーアプリを起動
display-layout-manager-menubar

# バックグラウンドで起動
display-layout-manager-menubar &

# 自動起動を有効化
display-layout-manager-menubar --enable-auto-launch

# 自動起動を無効化
display-layout-manager-menubar --disable-auto-launch
```

### 依存関係

#### 新規追加パッケージ
```
rumps>=0.4.0          # メニューバーアプリフレームワーク
pyobjc-framework-Cocoa>=9.0  # macOS API アクセス
```

#### requirements.txt 更新
```txt
# 既存の依存関係
# (なし - 標準ライブラリのみ使用)

# メニューバーアプリ用
rumps>=0.4.0
pyobjc-framework-Cocoa>=9.0
```

### パッケージング

#### エントリーポイント追加

**setup.py 更新:**
```python
setup(
    name="display-layout-manager",
    # ... 既存の設定 ...
    entry_points={
        'console_scripts': [
            'display-layout-manager=display_layout_manager.main:main',
            'display-layout-manager-menubar=display_layout_manager.menubar:main',  # 追加
        ],
    },
)
```

#### ディレクトリ構造更新

```
display-layout-manager/
├── src/
│   └── display_layout_manager/
│       ├── __init__.py
│       ├── main.py                  # CLI エントリーポイント
│       ├── menubar.py               # メニューバーアプリ エントリーポイント (新規)
│       ├── menubar_app.py           # メニューバーアプリ実装 (新規)
│       ├── cli_bridge.py            # CLI連携 (新規)
│       ├── notification_manager.py  # 通知管理 (新規)
│       ├── auto_launch_manager.py   # 自動起動管理 (新規)
│       ├── dependency_manager.py
│       ├── config_manager.py
│       ├── display_manager.py
│       ├── pattern_matcher.py
│       ├── command_executor.py
│       ├── logger.py
│       ├── error_handler.py
│       ├── integration_test.py
│       └── layout_saver.py
```

### Homebrew Formula の詳細実装

#### エントリーポイントの手動作成

Homebrew の `virtualenv_install_with_resources` がメニューバーアプリのエントリーポイントを正しく処理しない問題に対応するため、手動でエントリーポイントスクリプトを作成します。

```ruby
class DisplayLayoutManager < Formula
  include Language::Python::Virtualenv

  desc "macOS用ディスプレイレイアウト自動設定ツール"
  homepage "https://github.com/eijikominami/display-layout-manager"
  url "https://github.com/eijikominami/display-layout-manager/archive/v1.3.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"
  license "MIT"

  depends_on "python@3.11"
  depends_on "jakehilborn/jakehilborn/displayplacer"
  depends_on "grep"

  # Python 依存関係のリソース定義
  resource "rumps" do
    url "https://files.pythonhosted.org/packages/source/r/rumps/rumps-0.4.0.tar.gz"
    sha256 "RUMPS_SHA256"
  end

  resource "pyobjc-core" do
    url "https://files.pythonhosted.org/packages/source/p/pyobjc-core/pyobjc-core-10.1.tar.gz"
    sha256 "PYOBJC_CORE_SHA256"
  end

  resource "pyobjc-framework-Cocoa" do
    url "https://files.pythonhosted.org/packages/source/p/pyobjc-framework-Cocoa/pyobjc_framework_Cocoa-10.1.tar.gz"
    sha256 "PYOBJC_COCOA_SHA256"
  end

  def install
    # 依存関係を含めてインストール
    virtualenv_install_with_resources
    
    # メニューバーアプリのエントリーポイントを手動作成
    # virtualenv_install_with_resources が正しく処理しないため
    (bin/"display-layout-menubar").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" -m display_layout_manager.menubar "$@"
    EOS
    
    # 実行権限を付与
    chmod 0755, bin/"display-layout-menubar"
  end

  def post_install
    config_dir = "#{Dir.home}/Library/Application Support/DisplayLayoutManager"
    system "mkdir", "-p", config_dir
    system "chmod", "700", config_dir

    log_dir = "#{Dir.home}/Library/Logs/DisplayLayoutManager"
    system "mkdir", "-p", log_dir
    system "chmod", "700", log_dir
    
    puts <<~EOS
      Display Layout Manager がインストールされました。
      
      CLI使用方法:
        display-layout-manager --save-current     # 現在のレイアウトを保存
        display-layout-manager                    # 保存されたレイアウトを適用
        display-layout-manager --show-displays   # 接続されたディスプレイを表示
      
      メニューバーアプリ:
        display-layout-menubar                    # メニューバーアプリを起動
        display-layout-menubar --enable-auto-launch  # 自動起動を有効化
      
      設定ファイル:
        ~/Library/Application Support/DisplayLayoutManager/config.json
      
      ログファイル:
        ~/Library/Logs/DisplayLayoutManager/
    EOS
  end

  test do
    assert_match "Display Layout Manager", shell_output("#{bin}/display-layout-manager --version")
    system "#{bin}/display-layout-manager", "--run-tests"
  end
end
```

#### リソース管理の重要性

**必須リソース:**
1. **rumps**: メニューバーアプリフレームワーク
2. **pyobjc-core**: PyObjC の基盤パッケージ（重要！）
3. **pyobjc-framework-Cocoa**: macOS Cocoa フレームワークへのアクセス

**注意事項:**
- `pyobjc-core` は `pyobjc-framework-Cocoa` の依存関係だが、明示的に記載する必要がある
- 各リソースの正確な PyPI URL と SHA256 ハッシュが必要
- バージョンの整合性を保つ（pyobjc-core と pyobjc-framework-Cocoa は同じバージョン）

### エラーハンドリング

#### メニューバーアプリ固有のエラー

1. **GUI初期化エラー**: rumps の初期化失敗
2. **通知エラー**: macOS 通知センターへのアクセス失敗
3. **自動起動エラー**: LaunchAgent の作成・削除失敗
4. **CLI連携エラー**: バックグラウンド実行の失敗

### テスト戦略

#### 単体テスト
- CLI Bridge のモックテスト
- Notification Manager のテスト
- Auto Launch Manager のテスト

#### 統合テスト
- メニュー項目クリックのシミュレーション
- 通知表示の確認
- 自動起動の有効化・無効化テスト

#### 手動テスト
- 実際のメニューバーでの動作確認
- 通知の表示確認
- ログイン時の自動起動確認

### セキュリティ考慮事項

- **LaunchAgent plist**: 適切な権限設定（644）
- **プロセス分離**: メニューバーアプリと CLI の独立動作
- **通知内容**: 機密情報を含まない

### パフォーマンス考慮事項

- **軽量起動**: メニューバーアプリの高速起動
- **バックグラウンド実行**: UI をブロックしない非同期処理
- **メモリ使用量**: 常駐アプリとしての最小メモリ使用

## 将来拡張

### 機能拡張候補
1. **自動検出**: ディスプレイ接続/切断の自動検出とレイアウト適用
2. **プロファイル管理**: 時間帯や場所に応じた自動プロファイル切り替え
3. **クラウド同期**: 設定ファイルのクラウド同期機能
4. **プラグインシステム**: カスタム処理の追加機能
5. **保存済みパターン一覧**: メニューから直接パターンを選択して適用

### アーキテクチャ拡張
1. **イベント駆動**: ディスプレイ変更イベントの非同期処理
2. **API 化**: REST API による外部連携機能
3. **データベース**: 履歴管理用のローカルデータベース


## 国際化（i18n）対応

### 概要

CLI とメニューバーアプリのメッセージを、システムロケールに応じて日本語または英語で表示します。ログファイルは技術的な記録として常に英語で記録します。

### アーキテクチャ

#### コンポーネント構成

```
┌─────────────────────────────────────────────────────────────┐
│                  Internationalization Layer                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Message Manager │  │ Locale Detector │  │ Message      │ │
│  │                 │  │                 │  │ Catalog      │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│              Existing Components (Modified)                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ CLI             │  │ Menu Bar App    │  │ Logger       │ │
│  │ (i18n enabled)  │  │ (i18n enabled)  │  │ (English)    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### コンポーネント設計

#### 1. Locale Detector
- **責務**: システムロケールの検出
- **機能**:
  - 環境変数（LANG、LC_ALL、LC_MESSAGES）の確認
  - Python の locale モジュールによるロケール検出
  - 環境変数 DISPLAY_LAYOUT_LANG によるオーバーライド
  - 日本語ロケール（ja、ja_JP 等）の判定

```python
import locale
import os

class LocaleDetector:
    def __init__(self):
        self._detected_locale = None
    
    def detect_locale(self) -> str:
        """
        システムロケールを検出
        
        Returns:
            str: 'ja' または 'en'
        """
        # 環境変数によるオーバーライド
        override = os.environ.get('DISPLAY_LAYOUT_LANG')
        if override:
            return 'ja' if override.startswith('ja') else 'en'
        
        # システムロケールの検出
        try:
            # LANG 環境変数を確認
            lang = os.environ.get('LANG', '')
            if lang.startswith('ja'):
                return 'ja'
            
            # locale モジュールで検出
            current_locale, _ = locale.getdefaultlocale()
            if current_locale and current_locale.startswith('ja'):
                return 'ja'
        except Exception:
            pass
        
        # デフォルトは英語
        return 'en'
    
    def get_locale(self) -> str:
        """キャッシュされたロケールを取得"""
        if self._detected_locale is None:
            self._detected_locale = self.detect_locale()
        return self._detected_locale
```

#### 2. Message Catalog
- **責務**: メッセージの辞書管理
- **機能**:
  - 日本語・英語のメッセージマッピング
  - メッセージキーによる取得
  - フォーマット文字列のサポート

```python
# メッセージカタログの構造
MESSAGES = {
    'en': {
        # CLI messages
        'checking_dependencies': 'Checking dependencies...',
        'tool_found': '{tool} found: {version}',
        'tool_not_found': '{tool} not found',
        'detecting_displays': 'Detecting displays...',
        'displays_detected': 'Detected {count} display(s)',
        'applying_layout': 'Applying layout: {pattern}',
        'layout_applied': 'Layout applied successfully',
        'saving_current': 'Saving current layout...',
        'layout_saved': 'Layout saved as: {pattern}',
        'no_pattern_match': 'No matching pattern found',
        
        # Menu bar messages
        'menu_apply_layout': 'Apply Layout',
        'menu_save_current': 'Save Current Layout',
        'menu_auto_launch': 'Launch at Login',
        'menu_quit': 'Quit',
        
        # Error messages
        'error_occurred': 'Error occurred: {error}',
        'config_not_found': 'Configuration file not found',
        'command_failed': 'Command execution failed',
        
        # Auto launch messages
        'auto_launch_enabled': 'Auto-launch enabled',
        'auto_launch_disabled': 'Auto-launch disabled',
    },
    'ja': {
        # CLI メッセージ
        'checking_dependencies': '依存関係を確認中...',
        'tool_found': '{tool} が見つかりました: {version}',
        'tool_not_found': '{tool} が見つかりません',
        'detecting_displays': 'ディスプレイを検出中...',
        'displays_detected': '{count}個のディスプレイを検出しました',
        'applying_layout': 'レイアウトを適用中: {pattern}',
        'layout_applied': 'レイアウトを適用しました',
        'saving_current': '現在のレイアウトを保存中...',
        'layout_saved': 'レイアウトを保存しました: {pattern}',
        'no_pattern_match': '一致するパターンが見つかりません',
        
        # メニューバーメッセージ
        'menu_apply_layout': 'レイアウトを適用',
        'menu_save_current': '現在の設定を保存',
        'menu_auto_launch': 'ログイン時に起動',
        'menu_quit': '終了',
        
        # エラーメッセージ
        'error_occurred': 'エラーが発生しました: {error}',
        'config_not_found': '設定ファイルが見つかりません',
        'command_failed': 'コマンドの実行に失敗しました',
        
        # 自動起動メッセージ
        'auto_launch_enabled': '自動起動を有効化しました',
        'auto_launch_disabled': '自動起動を無効化しました',
    }
}
```

#### 3. Message Manager
- **責務**: メッセージの取得とフォーマット
- **機能**:
  - ロケールに応じたメッセージ取得
  - フォーマット文字列の処理
  - フォールバック処理（キーが見つからない場合は英語）

```python
class MessageManager:
    def __init__(self, locale_detector: LocaleDetector):
        self.locale_detector = locale_detector
        self.messages = MESSAGES
    
    def get(self, key: str, **kwargs) -> str:
        """
        メッセージを取得
        
        Args:
            key: メッセージキー
            **kwargs: フォーマット用のパラメータ
        
        Returns:
            str: ロケールに応じたメッセージ
        """
        locale = self.locale_detector.get_locale()
        
        # ロケールのメッセージを取得
        message = self.messages.get(locale, {}).get(key)
        
        # フォールバック: 英語
        if message is None:
            message = self.messages.get('en', {}).get(key, key)
        
        # フォーマット
        if kwargs:
            try:
                return message.format(**kwargs)
            except KeyError:
                return message
        
        return message
```

### 既存コンポーネントの修正

#### CLI（main.py）

```python
# 修正前
print("依存関係を確認中...")

# 修正後
msg = MessageManager(LocaleDetector())
print(msg.get('checking_dependencies'))
```

#### メニューバーアプリ（menubar_app.py）

```python
# 修正前
rumps.MenuItem("レイアウトを適用", callback=self.apply_layout)

# 修正後
msg = MessageManager(LocaleDetector())
rumps.MenuItem(msg.get('menu_apply_layout'), callback=self.apply_layout)
```

#### Logger（logger.py）

ログファイルは常に英語で記録するため、MessageManager を使用せず、直接英語メッセージを使用します。

```python
# ログファイルへの出力は常に英語
log_entry = {
    "timestamp": timestamp,
    "level": level,
    "component": component,
    "message": "Checking dependencies",  # 常に英語
    "details": details
}
```

ただし、CLI への出力（print文）は国際化対応します。

```python
# CLI出力は国際化
if self.verbose or level in ["ERROR", "WARNING"]:
    print(msg.get('checking_dependencies'))

# ログファイルは英語
self._write_to_file(log_entry)
```

### 実装ファイル構成

```
src/display_layout_manager/
├── i18n/
│   ├── __init__.py
│   ├── locale_detector.py    # ロケール検出
│   ├── message_catalog.py    # メッセージカタログ
│   └── message_manager.py    # メッセージ管理
├── main.py                    # CLI（i18n対応）
├── menubar_app.py             # メニューバーアプリ（i18n対応）
├── logger.py                  # Logger（ログは英語、CLI出力は i18n）
└── ...
```

### テスト戦略

#### 単体テスト
- LocaleDetector のロケール検出テスト
- MessageManager のメッセージ取得テスト
- 環境変数オーバーライドのテスト
- フォーマット文字列のテスト

#### 統合テスト
- 日本語環境でのCLI実行テスト
- 英語環境でのCLI実行テスト
- メニューバーアプリの言語切り替えテスト
- ログファイルが常に英語であることの確認

#### テストケース例

```python
def test_locale_detection_japanese():
    """日本語ロケールの検出"""
    os.environ['LANG'] = 'ja_JP.UTF-8'
    detector = LocaleDetector()
    assert detector.get_locale() == 'ja'

def test_locale_detection_english():
    """英語ロケールの検出"""
    os.environ['LANG'] = 'en_US.UTF-8'
    detector = LocaleDetector()
    assert detector.get_locale() == 'en'

def test_message_manager_japanese():
    """日本語メッセージの取得"""
    os.environ['LANG'] = 'ja_JP.UTF-8'
    msg = MessageManager(LocaleDetector())
    assert msg.get('checking_dependencies') == '依存関係を確認中...'

def test_message_manager_english():
    """英語メッセージの取得"""
    os.environ['LANG'] = 'en_US.UTF-8'
    msg = MessageManager(LocaleDetector())
    assert msg.get('checking_dependencies') == 'Checking dependencies...'

def test_environment_variable_override():
    """環境変数によるオーバーライド"""
    os.environ['DISPLAY_LAYOUT_LANG'] = 'ja'
    os.environ['LANG'] = 'en_US.UTF-8'
    detector = LocaleDetector()
    assert detector.get_locale() == 'ja'
```

### パフォーマンス考慮事項

- **ロケール検出のキャッシュ**: 初回検出後はキャッシュを使用
- **メッセージカタログの事前ロード**: 起動時に全メッセージをメモリにロード
- **軽量な実装**: 外部ライブラリ（gettext等）を使用せず、シンプルな辞書ベース

### セキュリティ考慮事項

- **環境変数の検証**: DISPLAY_LAYOUT_LANG の値を検証
- **インジェクション対策**: メッセージフォーマット時のパラメータ検証

### 将来拡張

- **追加言語のサポート**: 中国語、韓国語等の追加
- **動的言語切り替え**: 実行時の言語切り替え機能
- **外部メッセージファイル**: JSON/YAML形式の外部メッセージファイル対応

## メニューバーアプリの拡張機能

### 全ディスプレイへのアイコン表示

#### 概要

現在の実装では、メニューバーアイコンは1つのディスプレイ（通常はプライマリディスプレイ）にのみ表示されます。この機能により、接続されているすべてのディスプレイのメニューバーにアイコンを表示します。

#### 技術的アプローチ

##### 方法1: NSWindow.Level 設定（推奨）

rumps は内部的に NSStatusBar を使用していますが、デフォルトでは1つのディスプレイにのみ表示されます。NSWindow の level 設定を変更することで、すべてのディスプレイに表示できる可能性があります。

```python
from AppKit import NSApp, NSWindow

class DisplayLayoutMenuBar(rumps.App):
    def __init__(self):
        super(DisplayLayoutMenuBar, self).__init__(...)
        
        # すべてのディスプレイに表示されるように設定を試みる
        self._configure_multi_display()
    
    def _configure_multi_display(self):
        """すべてのディスプレイにアイコンを表示する設定"""
        try:
            # NSApp のウィンドウを取得
            for window in NSApp.windows():
                # ステータスバーウィンドウの level を設定
                window.setLevel_(NSWindow.NSStatusWindowLevel)
                window.setCollectionBehavior_(
                    NSWindow.NSWindowCollectionBehaviorCanJoinAllSpaces
                )
        except Exception as e:
            # エラーは無視（デフォルト動作を維持）
            pass
```

##### 方法2: 複数の NSStatusItem 作成（代替案）

各ディスプレイに対して個別の NSStatusItem を作成する方法です。ただし、rumps の制約により実装が複雑になる可能性があります。

```python
from AppKit import NSStatusBar

class MultiDisplayMenuBar:
    def __init__(self):
        self.status_items = []
        self._create_status_items_for_all_displays()
    
    def _create_status_items_for_all_displays(self):
        """各ディスプレイに対してステータスアイテムを作成"""
        # ディスプレイ数を取得
        display_count = self._get_display_count()
        
        # 各ディスプレイにステータスアイテムを作成
        for i in range(display_count):
            status_bar = NSStatusBar.systemStatusBar()
            status_item = status_bar.statusItemWithLength_(-1)
            status_item.setTitle_("⧈")
            self.status_items.append(status_item)
```

##### 実装の制約と注意事項

1. **macOS の制限**: macOS のステータスバーは、デフォルトでプライマリディスプレイにのみ表示される設計です
2. **rumps の制約**: rumps は単一のステータスアイテムを前提としているため、複数ディスプレイ対応には PyObjC の直接使用が必要になる可能性があります
3. **ユーザー体験**: すべてのディスプレイにアイコンが表示されることが、必ずしも良いUXとは限りません

##### 推奨実装アプローチ

1. **Phase 1**: NSWindow.Level 設定を試みる（方法1）
2. **Phase 2**: 動作しない場合は、PyObjC を直接使用して複数 NSStatusItem を作成（方法2）
3. **Phase 3**: 技術的に困難な場合は、要件を再検討（プライマリディスプレイのみでも十分な可能性）

#### データモデル

```python
@dataclass
class DisplayInfo:
    """ディスプレイ情報"""
    display_id: int
    is_primary: bool
    bounds: Dict[str, int]  # x, y, width, height
```

#### テスト戦略

- **単体テスト**: ディスプレイ数の取得テスト
- **統合テスト**: 複数ディスプレイ環境でのアイコン表示確認
- **手動テスト**: 実際の複数ディスプレイ環境での動作確認（必須）

### 重複起動の防止

#### 概要

メニューバーアプリが既に起動している場合、新しいインスタンスの起動を防止し、既存のインスタンスを前面に表示します。

#### 技術的アプローチ

##### 方法1: PID ファイルによる排他制御（推奨）

プロセスIDをファイルに記録し、起動時にチェックすることで重複起動を防止します。

```python
import os
import sys
from pathlib import Path

class SingleInstanceManager:
    """単一インスタンス管理"""
    
    def __init__(self):
        self.pid_file = Path.home() / "Library" / "Application Support" / \
                       "DisplayLayoutManager" / "menubar.pid"
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
    
    def is_already_running(self) -> bool:
        """既に起動しているかチェック"""
        if not self.pid_file.exists():
            return False
        
        try:
            # PIDファイルからプロセスIDを読み込む
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # プロセスが実際に動作しているかチェック
            os.kill(pid, 0)  # シグナル0は存在確認のみ
            return True
        except (ValueError, ProcessLookupError, PermissionError):
            # PIDファイルが無効、またはプロセスが存在しない
            return False
    
    def acquire_lock(self) -> bool:
        """ロックを取得（PIDファイルを作成）"""
        if self.is_already_running():
            return False
        
        try:
            # 現在のプロセスIDを書き込む
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
            return True
        except Exception:
            return False
    
    def release_lock(self):
        """ロックを解放（PIDファイルを削除）"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
        except Exception:
            pass
    
    def bring_existing_to_front(self):
        """既存のインスタンスを前面に表示"""
        try:
            # NSRunningApplication を使用して既存インスタンスをアクティブ化
            from AppKit import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
            
            # 現在実行中のアプリケーションを取得
            running_apps = NSRunningApplication.runningApplicationsWithBundleIdentifier_(
                "com.eijikominami.display-layout-manager"
            )
            
            if running_apps:
                app = running_apps[0]
                app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
        except Exception:
            # エラーは無視（既存インスタンスが見つからない場合等）
            pass
```

##### 方法2: NSRunningApplication による検出（代替案）

macOS の NSRunningApplication API を使用して、同じバンドル識別子のアプリケーションが既に実行中かチェックします。

```python
from AppKit import NSRunningApplication

class SingleInstanceManager:
    def is_already_running(self) -> bool:
        """既に起動しているかチェック"""
        bundle_id = "com.eijikominami.display-layout-manager"
        running_apps = NSRunningApplication.runningApplicationsWithBundleIdentifier_(bundle_id)
        
        # 自分自身以外のインスタンスが存在するかチェック
        current_pid = os.getpid()
        for app in running_apps:
            if app.processIdentifier() != current_pid:
                return True
        return False
```

##### エントリーポイントでの実装

```python
# menubar.py
def main():
    """メニューバーアプリのエントリーポイント"""
    # 単一インスタンス管理
    instance_manager = SingleInstanceManager()
    
    # 既に起動しているかチェック
    if instance_manager.is_already_running():
        print("Display Layout Manager is already running.")
        # 既存のインスタンスを前面に表示
        instance_manager.bring_existing_to_front()
        sys.exit(0)
    
    # ロックを取得
    if not instance_manager.acquire_lock():
        print("Failed to acquire lock.")
        sys.exit(1)
    
    try:
        # メニューバーアプリを起動
        app = DisplayLayoutMenuBar()
        app.run()
    finally:
        # 終了時にロックを解放
        instance_manager.release_lock()

if __name__ == '__main__':
    main()
```

#### データモデル

```python
@dataclass
class InstanceInfo:
    """インスタンス情報"""
    pid: int
    start_time: datetime
    is_running: bool
```

#### エラーハンドリング

1. **PIDファイル破損**: 無効なPIDファイルは無視して新規作成
2. **権限エラー**: PIDファイルの作成・削除に失敗した場合はログに記録
3. **プロセス検出失敗**: NSRunningApplication が使用できない場合はPIDファイルにフォールバック

#### テスト戦略

- **単体テスト**: 
  - PIDファイルの作成・削除テスト
  - 既存プロセスの検出テスト
  - ロック取得・解放テスト
- **統合テスト**:
  - 2つのインスタンスを同時起動して重複防止を確認
  - 既存インスタンスが前面に表示されることを確認
- **手動テスト**:
  - 実際にメニューバーアプリを2回起動して動作確認（必須）
  - Finder から複数回起動して動作確認

#### セキュリティ考慮事項

- **PIDファイルの権限**: 600（所有者のみ読み書き可能）
- **PIDファイルの場所**: ユーザーディレクトリ内（他ユーザーからアクセス不可）
- **プロセス検証**: PIDファイルのPIDが実際に動作しているか確認

#### パフォーマンス考慮事項

- **高速チェック**: 起動時のチェックは数ミリ秒以内に完了
- **軽量実装**: 外部ライブラリを使用せず、標準ライブラリとPyObjCのみ使用

### 実装ファイル構成

```
src/display_layout_manager/
├── menubar.py                      # エントリーポイント（重複起動チェック追加）
├── menubar_app.py                  # メニューバーアプリ（全ディスプレイ表示対応）
├── single_instance_manager.py      # 単一インスタンス管理（新規）
├── multi_display_manager.py        # 複数ディスプレイ対応（新規）
└── ...
```
