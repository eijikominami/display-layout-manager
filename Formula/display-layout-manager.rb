class DisplayLayoutManager < Formula
  include Language::Python::Virtualenv

  desc "macOS用ディスプレイレイアウト自動設定ツール"
  homepage "https://github.com/eijikominami/display-layout-manager"
  url "https://github.com/eijikominami/display-layout-manager/archive/v1.0.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"  # GitHub Actionsで自動更新
  license "MIT"

  depends_on "python@3.11"
  depends_on "jakehilborn/jakehilborn/displayplacer"
  depends_on "grep"

  def install
    virtualenv_install_with_resources
  end

  def post_install
    # 設定ディレクトリの作成
    config_dir = "#{Dir.home}/Library/Application Support/DisplayLayoutManager"
    system "mkdir", "-p", config_dir
    system "chmod", "700", config_dir

    # ログディレクトリの作成
    log_dir = "#{Dir.home}/Library/Logs/DisplayLayoutManager"
    system "mkdir", "-p", log_dir
    system "chmod", "700", log_dir

    # 常駐機能の自動セットアップ
    system "#{bin}/display-layout-manager", "--enable-daemon"
    
    # セットアップ完了メッセージ
    puts <<~EOS
      Display Layout Manager がインストールされました。
      
      常駐監視機能が自動的に有効化されています。
      ディスプレイ設定の変更時に自動的にレイアウトが適用されます。
      
      管理コマンド:
        display-layout-manager --status-daemon    # 状態確認
        display-layout-manager --disable-daemon   # 無効化
        display-layout-manager --enable-daemon    # 有効化
      
      設定ファイル:
        ~/Library/Application Support/DisplayLayoutManager/config.json
        ~/Library/Application Support/DisplayLayoutManager/daemon.json
      
      ログファイル:
        ~/Library/Logs/DisplayLayoutManager/
    EOS
  end

  def uninstall_preflight
    # 常駐機能を停止・削除
    system "#{bin}/display-layout-manager", "--disable-daemon"
  end

  test do
    # バージョン確認テスト
    assert_match "Display Layout Manager v#{version}", shell_output("#{bin}/display-layout-manager --version")
    
    # ヘルプ表示テスト
    assert_match "usage:", shell_output("#{bin}/display-layout-manager --help")
    
    # 依存関係チェックテスト（ドライラン）
    system "#{bin}/display-layout-manager", "--dry-run", "--verbose"
  end
end