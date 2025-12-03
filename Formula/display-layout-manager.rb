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