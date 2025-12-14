# 要件定義書

## 概要

macOS 用のディスプレイレイアウト自動設定アプリケーション。特定のディスプレイ環境を検出した際に、事前定義されたディスプレイレイアウトを自動的に適用するツールです。displayplacer コマンドを使用してディスプレイの配置、解像度、リフレッシュレートを制御します。

## 用語集

- **Display Layout Manager**: 本アプリケーションの名称
- **displayplacer**: macOS 用のディスプレイ設定変更コマンドラインツール
- **Persistent Screen ID**: ディスプレイの固有識別子
- **Homebrew**: macOS 用パッケージマネージャー
- **GNU grep**: テキスト検索ツール
- **LaunchAgent**: macOS でユーザーログイン時に自動起動するサービス
- **plist**: macOS の設定ファイル形式（Property List）
- **rumps**: macOS メニューバーアプリケーション作成用 Python ライブラリ

## 要件

### 要件 1

**ユーザーストーリー:** macOS ユーザーとして、アプリが自動的にディスプレイ設定を検出してほしい。手動設定なしで事前定義されたレイアウトを素早く適用できるようにするため。

#### 受け入れ基準

1. WHEN Display Layout Manager が開始される時、THE Display Layout Manager SHALL システムに displayplacer がインストールされているかチェックする
2. IF displayplacer がインストールされていない場合、THEN THE Display Layout Manager SHALL Homebrew を使用して displayplacer をインストールする
3. WHEN ディスプレイ設定をチェックする時、THE Display Layout Manager SHALL `displayplacer list | grep 'Persistent screen id'` を実行して接続されたディスプレイを取得する
4. THE Display Layout Manager SHALL 出力を解析して接続されたディスプレイの Persistent Screen ID を特定する
5. THE Display Layout Manager SHALL 比較のために現在のディスプレイ設定を保存する

### 要件 2

**ユーザーストーリー:** 複数ディスプレイを使用するユーザーとして、異なるディスプレイの組み合わせを認識してほしい。それぞれの組み合わせに応じた適切なレイアウト設定を適用できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL 設定ファイルから複数のディスプレイ組み合わせパターンを読み込む
2. WHEN ディスプレイ設定を分析する時、THE Display Layout Manager SHALL 現在接続されているすべての Persistent Screen ID を取得する
3. THE Display Layout Manager SHALL 現在の Persistent Screen ID の組み合わせと設定ファイルの各パターンを照合する
4. IF 現在の組み合わせが設定ファイルのいずれかのパターンと一致した場合、THEN THE Display Layout Manager SHALL そのパターンを「マッチした設定」として選択する
5. THE Display Layout Manager SHALL マッチした設定パターンまたは「該当なし」の結果をログに記録する

### 要件 3

**ユーザーストーリー:** ユーザーとして、検出されたディスプレイの組み合わせに応じて自動的に対応するレイアウトを適用してほしい。異なる環境で異なるレイアウトを自動適用できるようにするため。

#### 受け入れ基準

1. WHEN マッチした設定パターンが見つかった時、THE Display Layout Manager SHALL そのパターンに関連付けられた displayplacer コマンドを取得する
2. THE Display Layout Manager SHALL 取得した displayplacer コマンドを実行する
3. WHEN displayplacer コマンドが実行される時、THE Display Layout Manager SHALL コマンドの出力と終了コードを取得する
4. IF コマンドが成功した場合（終了コード 0）、THEN THE Display Layout Manager SHALL 適用されたパターン名と成功メッセージをログに記録する
5. IF コマンドが失敗した場合（非ゼロ終了コード）、THEN THE Display Layout Manager SHALL パターン名と詳細を含むエラーメッセージをログに記録する

### 要件 4

**ユーザーストーリー:** ユーザーとして、アプリが不足している依存関係を適切に処理してほしい。必要なツールが事前インストールされていなくてもアプリを使用できるようにするため。

#### 受け入れ基準

1. WHEN Display Layout Manager が開始される時、THE Display Layout Manager SHALL Homebrew がインストールされているかチェックする
2. IF Homebrew がインストールされていない場合、THEN THE Display Layout Manager SHALL ユーザーにインストール手順を提供する
3. WHEN displayplacer をインストールする時、THE Display Layout Manager SHALL `brew install jakehilborn/jakehilborn/displayplacer` を実行する
4. WHEN GNU grep をインストールする時、THE Display Layout Manager SHALL `brew install grep` を実行する
5. IF 依存関係のインストールが失敗した場合、THEN THE Display Layout Manager SHALL 明確なエラーメッセージとトラブルシューティングガイダンスを提供する

### 要件 5

**ユーザーストーリー:** ユーザーとして、複数のディスプレイ組み合わせパターンを管理したい。異なるディスプレイの組み合わせに応じて異なるレイアウトコマンドを定義できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL 設定ファイル（JSON または YAML 形式）を読み込む機能を提供する
2. THE Display Layout Manager SHALL 設定ファイルに複数のディスプレイ組み合わせパターンを定義できる
3. WHEN 設定ファイルが存在しない場合、THE Display Layout Manager SHALL サンプル設定を含むデフォルト設定ファイルを作成する
4. THE Display Layout Manager SHALL 各パターンに Persistent Screen ID のリスト（完全一致）と対応する displayplacer コマンドを関連付ける
5. THE Display Layout Manager SHALL 設定ファイルの構文エラーを検出し、適切なエラーメッセージを表示する

### 要件 6

**ユーザーストーリー:** ユーザーとして、アプリの動作について明確なフィードバックを受け取りたい。何をしているかを理解し、必要に応じて問題をトラブルシューティングできるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL 明確なステータスメッセージを持つコマンドラインインターフェースを提供する
2. WHEN 依存関係をチェックする時、THE Display Layout Manager SHALL 各必要ツールのステータスを表示する
3. WHEN ディスプレイを検出する時、THE Display Layout Manager SHALL 検出された Persistent Screen ID のリストを表示する
4. WHEN レイアウトを適用する時、THE Display Layout Manager SHALL 進捗と結果メッセージを表示する
5. THE Display Layout Manager SHALL 詳細なトラブルシューティング情報のための詳細ログオプションを提供する
6. THE Display Layout Manager SHALL 構造化ログファイルを macOS 標準ディレクトリ（~/Library/Logs/DisplayLayoutManager/）に出力する
7. THE Display Layout Manager SHALL セッション終了時にサマリー情報を表示する

### 要件 7

**ユーザーストーリー:** ユーザーとして、実際にコマンドを実行する前に動作を確認したい。設定変更前に安全にテストできるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL ドライランモード（--dry-run）を提供する
2. WHEN ドライランモードで実行される時、THE Display Layout Manager SHALL 実際のコマンドを実行せずに実行予定のコマンドを表示する
3. THE Display Layout Manager SHALL ドライランモードでも通常の検出・マッチング処理を実行する
4. THE Display Layout Manager SHALL ドライランモードの実行結果を明確に表示する

### 要件 8

**ユーザーストーリー:** ユーザーとして、包括的なエラーハンドリングとトラブルシューティングガイドを受け取りたい。問題が発生した際に迅速に解決できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL カテゴリ別のエラーコード体系を提供する
2. THE Display Layout Manager SHALL 各エラーに対してユーザーフレンドリーなメッセージを表示する
3. THE Display Layout Manager SHALL 各エラーに対して具体的な解決策を提示する
4. THE Display Layout Manager SHALL エラーの種類に応じて適切な終了コードを返す
5. THE Display Layout Manager SHALL 詳細モードでスタックトレースと技術的詳細を提供する

### 要件 9

**ユーザーストーリー:** ユーザーとして、統合テスト機能を使用してシステムの動作を検証したい。アプリケーションが正常に動作することを確認できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL 統合テストスイート（--run-tests）を提供する
2. THE Display Layout Manager SHALL 各コンポーネントの動作テストを実行する
3. THE Display Layout Manager SHALL テスト結果のサマリーを表示する
4. THE Display Layout Manager SHALL テスト失敗時に詳細な診断情報を提供する
5. THE Display Layout Manager SHALL テスト成功率を計算して表示する

### 要件 10

**ユーザーストーリー:** ユーザーとして、Homebrew を使用して簡単にインストールしたい。標準的なmacOSパッケージ管理方法でアプリを利用できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL Homebrew Formula を提供する
2. THE Display Layout Manager SHALL Python setuptools 互換のパッケージ構造を持つ
3. THE Display Layout Manager SHALL macOS 標準ディレクトリ構造に準拠する
4. THE Display Layout Manager SHALL インストール後の設定ディレクトリを自動作成する
5. THE Display Layout Manager SHALL アンインストール時のクリーンアップを提供する
6. THE Display Layout Manager SHALL 独自の Homebrew Tap (eijikominami/display-layout-manager) を提供する
7. THE Display Layout Manager SHALL GitHub Releases との統合を提供する

### 要件 11

**ユーザーストーリー:** ユーザーとして、現在のディスプレイレイアウトを簡単に設定パターンとして保存したい。手動でのJSON編集や複雑なコマンド入力なしに、現在の構成を再利用可能にするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL --save-current オプションを提供する
2. WHEN --save-current が実行される時、THE Display Layout Manager SHALL 現在のディスプレイ構成を自動検出する
3. THE Display Layout Manager SHALL 検出されたScreen IDsから一意のパターン名を自動生成する
4. THE Display Layout Manager SHALL 生成されたパターン名の形式を "{ディスプレイ数}_Displays_{Screen ID短縮形}" とする
5. WHEN 同じScreen IDsの組み合わせのパターンが既に存在する場合、THE Display Layout Manager SHALL 既存パターンを自動的に上書きする
6. THE Display Layout Manager SHALL displayplacer list コマンドから現在の設定コマンドを抽出する
7. THE Display Layout Manager SHALL 保存されたパターンの詳細をユーザーに表示する

### 要件 12

**ユーザーストーリー:** 開発者として、リリースプロセスを自動化したい。手動作業を最小限にして、一貫性のあるリリースを提供できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL GitHub Actions による CI/CD パイプラインを提供する
2. WHEN バージョンタグがプッシュされる時、THE Display Layout Manager SHALL 自動的にテストを実行する
3. WHEN テストが成功した場合、THE Display Layout Manager SHALL 自動的に GitHub Release を作成する
4. THE Display Layout Manager SHALL リリース時に SHA256 ハッシュを自動計算する
5. THE Display Layout Manager SHALL Homebrew Formula を自動更新する
6. THE Display Layout Manager SHALL Homebrew Tap リポジトリを自動更新する
7. THE Display Layout Manager SHALL リリース失敗時に適切なエラー通知を提供する
8. THE Display Layout Manager SHALL プルリクエスト時に Homebrew Formula のインストールテストを実行する
9. THE Display Layout Manager SHALL すべてのエントリーポイントが正しく作成されることを検証する
10. THE Display Layout Manager SHALL テストカバレッジを測定し Codecov にアップロードする

### 要件 13

**ユーザーストーリー:** ユーザーとして、macOS のメニューバーから簡単にディスプレイレイアウトを操作したい。ターミナルを開かずに、クリック操作だけでレイアウトの適用と保存ができるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL macOS メニューバー（Status Bar）にアイコンを表示する
2. THE Display Layout Manager SHALL 接続されているすべてのディスプレイのメニューバーにアイコンを表示する
3. WHEN ユーザーがメニューバーアイコンをクリックした時、THE Display Layout Manager SHALL ドロップダウンメニューを表示する
4. THE Display Layout Manager SHALL メニューに「レイアウトを適用」ボタンを提供する
5. WHEN ユーザーが「レイアウトを適用」をクリックした時、THE Display Layout Manager SHALL 現在のディスプレイ構成に一致するレイアウトを適用する
6. THE Display Layout Manager SHALL メニューに「現在の設定を保存」ボタンを提供する
7. WHEN ユーザーが「現在の設定を保存」をクリックした時、THE Display Layout Manager SHALL 現在のディスプレイ構成を設定ファイルに保存する
8. THE Display Layout Manager SHALL メニューに「ログイン時に起動」トグルメニュー項目を提供する
9. WHEN ユーザーが「ログイン時に起動」をクリックした時、THE Display Layout Manager SHALL 自動起動の有効/無効を切り替える
10. THE Display Layout Manager SHALL 「ログイン時に起動」メニュー項目に現在の状態を示すチェックマークを表示する
11. THE Display Layout Manager SHALL メニューに「終了」ボタンを提供する
12. THE Display Layout Manager SHALL メニューバーアプリと CLI の両方を同時に使用できる
13. WHEN メニューバーアプリが既に起動している時、THE Display Layout Manager SHALL 新しいインスタンスの起動を防止する
14. IF ユーザーが既に起動中のメニューバーアプリを再度起動しようとした場合、THEN THE Display Layout Manager SHALL 既存のインスタンスを前面に表示し、新しいインスタンスは起動しない

### 要件 14

**ユーザーストーリー:** 開発者として、品質を可視化したい。プロジェクトの健全性を一目で確認できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL README にビルドステータスバッジを表示する
2. THE Display Layout Manager SHALL README にリリースステータスバッジを表示する
3. THE Display Layout Manager SHALL README に最新リリースバージョンバッジを表示する
4. THE Display Layout Manager SHALL README にテストカバレッジバッジを表示する
5. THE Display Layout Manager SHALL README にライセンスバッジを表示する
6. THE Display Layout Manager SHALL README に Python バージョンバッジを表示する

### 要件 15

**ユーザーストーリー:** ユーザーとして、詳細なドキュメントを参照したい。アプリケーションの使い方や問題解決方法を理解できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL アーキテクチャドキュメント（ARCHITECTURE.md）を提供する
2. THE Display Layout Manager SHALL 設定ファイル詳細仕様（docs/configuration.md）を提供する
3. THE Display Layout Manager SHALL トラブルシューティングガイド（docs/troubleshooting.md）を提供する
4. THE Display Layout Manager SHALL 各ドキュメント間の相互参照リンクを提供する
5. THE Display Layout Manager SHALL 初見のユーザーでも理解できる説明を提供する

### 要件 16

**ユーザーストーリー:** 国際的なユーザーとして、英語と日本語の両方でドキュメントを読みたい。母国語でアプリケーションの使い方を理解できるようにするため。

#### 受け入れ基準

1. THE Display Layout Manager SHALL すべての主要ドキュメントを英語版と日本語版で提供する
2. THE Display Layout Manager SHALL 英語版を基本言語として、日本語版を追加言語として提供する
3. THE Display Layout Manager SHALL 各ドキュメントの冒頭に言語切り替えリンクを提供する
4. THE Display Layout Manager SHALL 英語版ドキュメントに `English / [**日本語**](filename_JP.md)` 形式のリンクを表示する
5. THE Display Layout Manager SHALL 日本語版ドキュメントに `[**English**](filename.md) / 日本語` 形式のリンクを表示する
6. THE Display Layout Manager SHALL 以下のドキュメントを両言語で提供する:
   - README.md / README_JP.md
   - ARCHITECTURE.md / ARCHITECTURE_JP.md
   - docs/configuration.md / docs/configuration_jp.md
   - docs/troubleshooting.md / docs/troubleshooting_jp.md


### 要件 17

**ユーザーストーリー:** 国際的なユーザーとして、CLI とメニューバーアプリのメッセージを自分の言語で読みたい。日本語環境では日本語で、それ以外の環境では英語でメッセージを表示してほしい。

#### 受け入れ基準

1. THE Display Layout Manager SHALL システムのロケール設定を検出する
2. WHEN システムロケールが日本語（ja、ja_JP 等）の場合、THEN THE Display Layout Manager SHALL すべてのメッセージを日本語で表示する
3. WHEN システムロケールが日本語以外の場合、THEN THE Display Layout Manager SHALL すべてのメッセージを英語で表示する
4. THE Display Layout Manager SHALL CLI のすべての出力メッセージ（標準出力・標準エラー出力）を国際化対応する
5. THE Display Layout Manager SHALL メニューバーアプリのすべてのメニュー項目を国際化対応する
6. THE Display Layout Manager SHALL ログファイルのメッセージを常に英語で記録する
7. THE Display Layout Manager SHALL 言語切り替えのための環境変数オーバーライド機能を提供する
8. THE Display Layout Manager SHALL メッセージカタログを辞書形式で管理する
