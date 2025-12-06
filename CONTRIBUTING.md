# コントリビューションガイド

Display Layout Manager へのコントリビューションをご検討いただき、ありがとうございます！このガイドでは、プロジェクトへの貢献方法について説明します。

## 目次

- [行動規範](#行動規範)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [開発ワークフロー](#開発ワークフロー)
- [コーディング規約](#コーディング規約)
- [テスト](#テスト)
- [プルリクエスト](#プルリクエスト)
- [バグ報告](#バグ報告)
- [機能要望](#機能要望)

## 行動規範

このプロジェクトは、すべての参加者に対して友好的で包括的な環境を提供することを目指しています。以下の行動規範を遵守してください：

- 他の参加者を尊重する
- 建設的なフィードバックを提供する
- 異なる意見や経験を受け入れる
- プロジェクトの目標に焦点を当てる

## 開発環境のセットアップ

### 必要な環境

- **OS**: macOS 10.14 (Mojave) 以降
- **Python**: 3.8 以降
- **Git**: 最新版
- **Homebrew**: 最新版

### セットアップ手順

1. **リポジトリをフォーク**
   - GitHub でリポジトリをフォーク
   - フォークしたリポジトリをローカルにクローン

   ```bash
   git clone https://github.com/YOUR_USERNAME/display-layout-manager.git
   cd display-layout-manager
   ```

2. **上流リポジトリを追加**
   ```bash
   git remote add upstream https://github.com/eijikominami/display-layout-manager.git
   ```

3. **開発モードでインストール**
   ```bash
   pip install -e .
   ```

4. **依存関係をインストール**
   ```bash
   brew install jakehilborn/jakehilborn/displayplacer
   brew install grep
   ```

5. **開発ツールをインストール**
   ```bash
   pip install black isort flake8 pytest coverage
   ```

## 開発ワークフロー

### ブランチ戦略

- **main**: 本番環境にデプロイ可能な安定版
- **feature/\***: 新機能開発用ブランチ
- **fix/\***: バグ修正用ブランチ
- **docs/\***: ドキュメント更新用ブランチ

### 開発フロー

1. **最新の main ブランチを取得**
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **feature ブランチを作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **コードを変更**
   - 機能を実装
   - テストを追加
   - ドキュメントを更新

4. **コードフォーマット**
   ```bash
   # import 文を整理
   isort --profile black src/ tests/
   
   # コードをフォーマット
   black src/ tests/
   ```

5. **コードチェック**
   ```bash
   # フォーマットチェック
   black --check src/ tests/
   isort --check-only --profile black src/ tests/
   
   # Lint チェック
   flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203
   ```

6. **テストを実行**
   ```bash
   # 全テストを実行
   python tests/run_all_tests.py
   
   # カバレッジを測定
   python tests/run_coverage.py
   ```

7. **変更をコミット**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

8. **プッシュ**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **プルリクエストを作成**
   - GitHub でプルリクエストを作成
   - テンプレートに従って説明を記入

## コーディング規約

### Python スタイルガイド

- **PEP 8** に準拠
- **Black** でフォーマット（行長: 88文字）
- **isort** で import 文を整理

### 命名規則

- **クラス**: `PascalCase` (例: `ConfigManager`)
- **関数・メソッド**: `snake_case` (例: `load_config`)
- **定数**: `UPPER_SNAKE_CASE` (例: `DEFAULT_CONFIG_PATH`)
- **プライベート**: `_leading_underscore` (例: `_internal_method`)

### ドキュメント

- すべての public クラス・メソッドに docstring を記述
- Google スタイルの docstring を使用

```python
def example_function(param1: str, param2: int) -> bool:
    """関数の簡潔な説明。

    Args:
        param1: 第1引数の説明
        param2: 第2引数の説明

    Returns:
        戻り値の説明

    Raises:
        ValueError: エラーが発生する条件
    """
    pass
```

### 型ヒント

- すべての関数・メソッドに型ヒントを追加
- `typing` モジュールを活用

```python
from typing import List, Dict, Optional

def process_data(items: List[str]) -> Dict[str, int]:
    pass
```

## テスト

### テストの種類

1. **単体テスト**: 個別のコンポーネントをテスト
2. **統合テスト**: 複数のコンポーネントの連携をテスト
3. **エンドツーエンドテスト**: 全体のフローをテスト

### テストの書き方

```python
import unittest
from src.display_layout_manager.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        """各テストの前に実行"""
        self.config_manager = ConfigManager()
    
    def test_load_config_success(self):
        """設定ファイルの読み込みが成功する"""
        config = self.config_manager.load_config("test_config.json")
        self.assertIsNotNone(config)
        self.assertIn("patterns", config)
    
    def test_load_config_invalid_json(self):
        """不正な JSON でエラーが発生する"""
        with self.assertRaises(ConfigError):
            self.config_manager.load_config("invalid.json")
```

### テストカバレッジ

- 新機能には必ずテストを追加
- カバレッジ 70% 以上を維持
- 重要なロジックは 100% カバレッジを目指す

### テスト実行

```bash
# 全テストを実行
python tests/run_all_tests.py

# 特定のテストを実行
python tests/test_config_manager.py

# カバレッジレポートを生成
python tests/run_coverage.py
open htmlcov/index.html
```

## プルリクエスト

### プルリクエストの作成

1. **明確なタイトル**
   - `feat: 新機能の追加`
   - `fix: バグの修正`
   - `docs: ドキュメントの更新`
   - `refactor: リファクタリング`
   - `test: テストの追加・修正`

2. **詳細な説明**
   - 変更の目的
   - 変更内容の概要
   - テスト方法
   - 関連 Issue

3. **チェックリスト**
   - [ ] コードフォーマット済み（black, isort）
   - [ ] Lint チェック通過（flake8）
   - [ ] テスト追加済み
   - [ ] テスト全て通過
   - [ ] ドキュメント更新済み
   - [ ] CHANGELOG.md 更新済み

### レビュープロセス

1. **自動チェック**
   - GitHub Actions で自動テスト実行
   - コードフォーマットチェック
   - Lint チェック
   - テストカバレッジ測定

2. **コードレビュー**
   - メンテナーがコードをレビュー
   - フィードバックに対応
   - 承認後にマージ

3. **マージ**
   - Squash and merge を使用
   - コミットメッセージを整理

## バグ報告

バグを発見した場合は、[GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues) で報告してください。

### バグ報告テンプレート

```markdown
## バグの説明
バグの簡潔な説明

## 再現手順
1. '...' を実行
2. '...' をクリック
3. エラーが発生

## 期待される動作
本来どのように動作すべきか

## 実際の動作
実際にどのように動作したか

## 環境
- OS: macOS 14.0
- Python: 3.11
- Display Layout Manager: 1.3.3

## ログ
関連するログやエラーメッセージ

## スクリーンショット
該当する場合、スクリーンショットを添付
```

## 機能要望

新機能の提案は、[GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues) で行ってください。

### 機能要望テンプレート

```markdown
## 機能の説明
提案する機能の簡潔な説明

## 動機
なぜこの機能が必要か

## 提案する解決策
どのように実装すべきか

## 代替案
他に考えられる実装方法

## 追加情報
その他の関連情報
```

## コミットメッセージ規約

### フォーマット

```
<type>: <subject>

<body>

<footer>
```

### Type

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
- `refactor`: バグ修正や機能追加ではないコード変更
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

### 例

```
feat: add support for multiple configuration profiles

- Add profile selection in menu bar app
- Update config file format to support profiles
- Add migration script for existing configs

Closes #123
```

## リリースプロセス

1. **バージョン番号の更新**
   - `src/display_layout_manager/__init__.py` の `__version__`
   - セマンティックバージョニングに従う（MAJOR.MINOR.PATCH）

2. **CHANGELOG.md の更新**
   - 変更内容を記載
   - リリース日を記載

3. **タグの作成**
   ```bash
   git tag v1.3.4
   git push origin v1.3.4
   ```

4. **GitHub Actions**
   - 自動的にリリースを作成
   - Homebrew Formula を更新

## 質問・サポート

- **質問**: [GitHub Discussions](https://github.com/eijikominami/display-layout-manager/discussions)
- **バグ報告**: [GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues)
- **機能要望**: [GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues)

## ライセンス

このプロジェクトに貢献することで、あなたの貢献が MIT ライセンスの下でライセンスされることに同意したものとみなされます。

---

ご協力ありがとうございます！🎉
