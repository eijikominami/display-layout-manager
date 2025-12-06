[**English**](troubleshooting.md) / 日本語

# トラブルシューティングガイド

## 概要

このガイドでは、Display Layout Manager の使用中に発生する可能性のある問題と、その解決方法を説明します。

## 目次

- [依存関係の問題](#依存関係の問題)
- [設定ファイルの問題](#設定ファイルの問題)
- [ディスプレイ検出の問題](#ディスプレイ検出の問題)
- [パターンマッチングの問題](#パターンマッチングの問題)
- [コマンド実行の問題](#コマンド実行の問題)
- [メニューバーアプリの問題](#メニューバーアプリの問題)
- [Homebrew インストールの問題](#homebrew-インストールの問題)
- [ログとデバッグ](#ログとデバッグ)

## 依存関係の問題

### Homebrew が見つからない

**症状:**
```
エラー: Homebrew が見つかりません
```

**原因:**
- Homebrew がインストールされていない
- PATH が正しく設定されていない

**解決策:**

1. **Homebrew をインストール**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **PATH を設定**
   
   Apple Silicon Mac の場合:
   ```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
   source ~/.zshrc
   ```
   
   Intel Mac の場合:
   ```bash
   echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **確認**
   ```bash
   brew --version
   ```

### displayplacer が見つからない

**症状:**
```
エラー: displayplacer が見つかりません
```

**原因:**
- displayplacer がインストールされていない
- 自動インストールが失敗した

**解決策:**

1. **手動でインストール**
   ```bash
   brew install jakehilborn/jakehilborn/displayplacer
   ```

2. **確認**
   ```bash
   displayplacer --version
   ```

3. **それでも解決しない場合**
   - GitHub から直接ダウンロード: https://github.com/jakehilborn/displayplacer/releases
   - バイナリを `/usr/local/bin/` に配置
   - 実行権限を付与: `chmod +x /usr/local/bin/displayplacer`

### GNU grep が見つからない

**症状:**
```
エラー: GNU grep が見つかりません
```

**原因:**
- GNU grep がインストールされていない
- macOS 標準の grep が使用されている

**解決策:**

1. **GNU grep をインストール**
   ```bash
   brew install grep
   ```

2. **PATH を設定（オプション）**
   
   Apple Silicon Mac の場合:
   ```bash
   echo 'export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
   
   Intel Mac の場合:
   ```bash
   echo 'export PATH="/usr/local/opt/grep/libexec/gnubin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **確認**
   ```bash
   grep --version | head -1
   # GNU grep が表示されることを確認
   ```

## 設定ファイルの問題

### JSON 構文エラー

**症状:**
```
エラー: 設定ファイルの構文エラー
詳細: Expecting ',' delimiter: line 5 column 3 (char 123)
```

**原因:**
- JSON の構文が不正
- コンマ、括弧、引用符の対応が不正

**解決策:**

1. **オンライン JSON バリデーターを使用**
   - https://jsonlint.com/
   - 設定ファイルの内容を貼り付けて検証

2. **一般的な構文エラー**
   
   **末尾のコンマ**
   ```json
   // ❌ 悪い例
   {
     "patterns": [
       {
         "name": "Pattern 1",
       }
     ]
   }
   
   // ✅ 良い例
   {
     "patterns": [
       {
         "name": "Pattern 1"
       }
     ]
   }
   ```
   
   **引用符の不一致**
   ```json
   // ❌ 悪い例
   {
     "name": "Pattern 1'
   }
   
   // ✅ 良い例
   {
     "name": "Pattern 1"
   }
   ```

3. **設定ファイルを検証**
   ```bash
   display-layout-manager --validate-config --verbose
   ```

### 必須フィールド不足

**症状:**
```
エラー: 設定ファイルの検証エラー
詳細: パターン 'Home Office Setup' に必須フィールド 'command' がありません
```

**原因:**
- パターンに必須フィールドが不足している

**解決策:**

1. **必須フィールドを確認**
   - `version`: 設定ファイルのバージョン
   - `patterns`: パターンの配列
   - 各パターン:
     - `name`: パターン名
     - `screen_ids`: Screen ID の配列
     - `command`: displayplacer コマンド

2. **不足しているフィールドを追加**
   ```json
   {
     "version": "1.0",
     "patterns": [
       {
         "name": "Pattern Name",
         "description": "Optional description",
         "screen_ids": ["SCREEN_ID_1", "SCREEN_ID_2"],
         "command": "displayplacer ..."
       }
     ]
   }
   ```

3. **設定ファイルを検証**
   ```bash
   display-layout-manager --validate-config
   ```

### 設定ファイルが見つからない

**症状:**
```
警告: 設定ファイルが見つかりません
デフォルト設定ファイルを作成しました
```

**原因:**
- 設定ファイルが存在しない（初回実行時は正常）

**解決策:**

1. **自動作成されたファイルを確認**
   ```bash
   open ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```

2. **現在のレイアウトを保存**
   ```bash
   display-layout-manager --save-current
   ```

3. **手動で設定ファイルを作成**
   - [設定ファイル詳細仕様](configuration.md) を参照

## ディスプレイ検出の問題

### Screen ID が取得できない

**症状:**
```
エラー: ディスプレイの検出に失敗しました
```

**原因:**
- displayplacer コマンドが失敗している
- ディスプレイが正しく接続されていない

**解決策:**

1. **displayplacer を直接実行**
   ```bash
   displayplacer list
   ```
   
   エラーが表示される場合は、displayplacer の問題です。

2. **ディスプレイ接続を確認**
   - ケーブルが正しく接続されているか
   - ディスプレイの電源が入っているか
   - システム環境設定 > ディスプレイで認識されているか

3. **詳細ログで確認**
   ```bash
   display-layout-manager --show-displays --verbose
   ```

### 一部のディスプレイが検出されない

**症状:**
- 接続されているディスプレイの一部が検出されない

**原因:**
- ディスプレイが完全に初期化されていない
- USB-C ハブやドッキングステーションの問題

**解決策:**

1. **ディスプレイを再接続**
   - ケーブルを抜き差しする
   - 数秒待ってから再接続

2. **macOS を再起動**
   - ディスプレイ設定がリセットされる

3. **ハブ/ドッキングステーションを確認**
   - ファームウェアが最新か
   - 電源供給が十分か

## パターンマッチングの問題

### パターンが一致しない

**症状:**
```
警告: 一致するパターンが見つかりません
現在の Screen IDs: [ID1, ID2]
```

**原因:**
- 設定ファイルのScreen IDsと現在のScreen IDsが一致しない
- Screen IDの順序が異なる（順序は問わないはずだが、念のため確認）

**解決策:**

1. **現在の Screen ID を確認**
   ```bash
   display-layout-manager --show-displays
   ```

2. **設定ファイルの Screen IDs を更新**
   ```bash
   open ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```
   
   現在の Screen IDs と完全に一致するように修正

3. **自動保存を使用**
   ```bash
   display-layout-manager --save-current
   ```
   
   これにより、現在の構成が自動的に保存されます。

4. **ドライランで確認**
   ```bash
   display-layout-manager --dry-run --verbose
   ```

### 複数のパターンが一致する

**症状:**
- 意図しないパターンが適用される

**原因:**
- 同じ Screen IDs を持つ複数のパターンが存在する

**解決策:**

1. **設定ファイルを確認**
   ```bash
   open ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```

2. **重複するパターンを削除または統合**
   - 同じ Screen IDs を持つパターンは1つだけにする
   - 最後に定義されたパターンが優先されます

3. **パターン名を明確にする**
   - 用途が分かりやすい名前を使用

## コマンド実行の問題

### displayplacer コマンドが失敗する

**症状:**
```
エラー: コマンドの実行に失敗しました
終了コード: 1
```

**原因:**
- Screen ID が不正
- 解像度やリフレッシュレートが対応していない
- ディスプレイが接続されていない

**解決策:**

1. **ドライランで確認**
   ```bash
   display-layout-manager --dry-run --verbose
   ```
   
   実行予定のコマンドを確認

2. **displayplacer を直接実行**
   ```bash
   # ドライランで表示されたコマンドをコピーして実行
   displayplacer "id:SCREEN_ID res:1920x1080 ..."
   ```
   
   エラーメッセージを確認

3. **対応している解像度を確認**
   ```bash
   displayplacer list
   ```
   
   "Resolutions for rotation 0:" セクションで対応解像度を確認

4. **設定ファイルを更新**
   - 対応している解像度・リフレッシュレートに変更
   - または `--save-current` で現在の設定を保存

### 権限エラー

**症状:**
```
エラー: 権限が拒否されました
```

**原因:**
- ディスプレイ設定の変更権限がない
- macOS のセキュリティ設定

**解決策:**

1. **システム環境設定を確認**
   - システム環境設定 > セキュリティとプライバシー > プライバシー
   - アクセシビリティで Terminal.app または使用しているターミナルアプリを許可

2. **管理者権限で実行（非推奨）**
   ```bash
   sudo display-layout-manager
   ```
   
   ただし、通常は不要です。

## メニューバーアプリの問題

### メニューバーアイコンが表示されない

**症状:**
- `display-layout-menubar` を実行してもアイコンが表示されない

**原因:**
- アプリが正しく起動していない
- rumps の依存関係の問題

**解決策:**

1. **ターミナルから起動して確認**
   ```bash
   display-layout-menubar
   ```
   
   エラーメッセージを確認

2. **依存関係を確認**
   ```bash
   pip show rumps pyobjc-framework-Cocoa
   ```

3. **再インストール**
   ```bash
   brew uninstall display-layout-manager
   brew install display-layout-manager
   ```

### 「レイアウトを適用」が動作しない

**症状:**
- メニュー項目をクリックしても何も起こらない

**原因:**
- 一致するパターンがない
- displayplacer コマンドが失敗している

**解決策:**

1. **ログファイルを確認**
   ```bash
   tail -f ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log
   ```
   
   メニュー項目をクリックしてログを確認

2. **CLI で動作確認**
   ```bash
   display-layout-manager --verbose
   ```
   
   CLI で正常に動作するか確認

3. **設定ファイルを確認**
   - 一致するパターンが存在するか
   - Screen IDs が正しいか

### 自動起動が動作しない

**症状:**
- 「ログイン時に起動」を有効にしてもログイン時に起動しない

**原因:**
- LaunchAgent plist が正しく作成されていない
- macOS のセキュリティ設定

**解決策:**

1. **plist ファイルを確認**
   ```bash
   cat ~/Library/LaunchAgents/com.displaylayoutmanager.menubar.plist
   ```

2. **launchctl で確認**
   ```bash
   launchctl list | grep displaylayoutmanager
   ```

3. **手動で登録**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.displaylayoutmanager.menubar.plist
   ```

4. **システム環境設定を確認**
   - システム環境設定 > ユーザとグループ > ログイン項目
   - Display Layout Manager が表示されているか

## Homebrew インストールの問題

### Formula が見つからない

**症状:**
```
Error: No available formula with the name "display-layout-manager"
```

**原因:**
- Tap が追加されていない

**解決策:**

1. **Tap を追加**
   ```bash
   brew tap eijikominami/display-layout-manager
   ```

2. **インストール**
   ```bash
   brew install display-layout-manager
   ```

### インストールが失敗する

**症状:**
```
Error: An exception occurred within a child process:
  ...
```

**原因:**
- 依存関係の問題
- ネットワークの問題

**解決策:**

1. **Homebrew を更新**
   ```bash
   brew update
   ```

2. **キャッシュをクリア**
   ```bash
   brew cleanup
   ```

3. **再試行**
   ```bash
   brew install display-layout-manager
   ```

4. **詳細ログで確認**
   ```bash
   brew install display-layout-manager --verbose --debug
   ```

### コマンドが見つからない

**症状:**
```
zsh: command not found: display-layout-manager
```

**原因:**
- PATH が正しく設定されていない
- インストールが完了していない

**解決策:**

1. **インストール状況を確認**
   ```bash
   brew list display-layout-manager
   ```

2. **PATH を確認**
   ```bash
   echo $PATH | grep homebrew
   ```

3. **PATH を設定**
   
   Apple Silicon Mac の場合:
   ```bash
   echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
   
   Intel Mac の場合:
   ```bash
   echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **確認**
   ```bash
   which display-layout-manager
   display-layout-manager --version
   ```

## ログとデバッグ

### ログファイルの場所

```
~/Library/Logs/DisplayLayoutManager/display_layout_manager_YYYYMMDD.log
```

### ログファイルの確認

```bash
# 最新のログを表示
tail -f ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log

# 特定の日付のログを表示
cat ~/Library/Logs/DisplayLayoutManager/display_layout_manager_20231215.log

# エラーのみを表示
grep ERROR ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log
```

### 詳細ログの有効化

```bash
# CLI で詳細ログを有効化
display-layout-manager --verbose

# すべてのオプションで詳細ログ
display-layout-manager --show-displays --verbose
display-layout-manager --validate-config --verbose
display-layout-manager --dry-run --verbose
```

### デバッグ情報の収集

問題を報告する際は、以下の情報を含めてください：

1. **バージョン情報**
   ```bash
   display-layout-manager --version
   displayplacer --version
   sw_vers
   ```

2. **ディスプレイ情報**
   ```bash
   display-layout-manager --show-displays
   displayplacer list
   ```

3. **設定ファイル**
   ```bash
   cat ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```

4. **ログファイル**
   ```bash
   cat ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log
   ```

5. **エラーメッセージ**
   - 完全なエラーメッセージをコピー

## よくある質問 (FAQ)

### Q: ディスプレイを接続/切断したら自動的にレイアウトが適用されますか？

A: 現在のバージョンでは、手動で `display-layout-manager` を実行するか、メニューバーアプリから「レイアウトを適用」をクリックする必要があります。将来のバージョンで自動検出機能を追加予定です。

### Q: 複数の設定ファイルを切り替えることはできますか？

A: はい、`--config` オプションで設定ファイルを指定できます：
```bash
display-layout-manager --config ~/my-config.json
```

### Q: パターン名を変更できますか？

A: はい、設定ファイルを直接編集してパターン名を変更できます。ただし、`--save-current` で保存したパターンは自動生成された名前になります。

### Q: 解像度やリフレッシュレートを変更できますか？

A: はい、設定ファイルの `command` フィールドを編集して変更できます。対応している解像度は `displayplacer list` で確認できます。

### Q: ログファイルを削除しても大丈夫ですか？

A: はい、ログファイルは自動的に再作成されます。古いログファイルは定期的に削除しても問題ありません。

## サポート

問題が解決しない場合は、以下の方法でサポートを受けることができます：

- **GitHub Issues**: https://github.com/eijikominami/display-layout-manager/issues
- **GitHub Discussions**: https://github.com/eijikominami/display-layout-manager/discussions

バグ報告や機能要望は GitHub Issues で受け付けています。

## 関連ドキュメント

- [README_JP.md](../README_JP.md) - 基本的な使用方法
- [ARCHITECTURE_JP.md](../ARCHITECTURE_JP.md) - システムアーキテクチャ
- [設定ファイル詳細仕様](configuration_jp.md) - 設定ファイルの詳細
