"""
依存関係管理モジュール
必要な外部ツールの存在確認とインストールを管理
"""

import subprocess
import shutil
from typing import Tuple, Optional
from pathlib import Path


class DependencyManager:
    """依存関係管理クラス"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """ログ出力（詳細モード時のみ）"""
        if self.verbose:
            print(f"[依存関係] {message}")

    def _run_command(self, command: list, timeout: int = 30) -> Tuple[bool, str, str]:
        """
        コマンドを実行し、結果を返す

        Returns:
            Tuple[bool, str, str]: (成功フラグ, stdout, stderr)
        """
        try:
            self._log(f"コマンド実行: {' '.join(command)}")
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=timeout
            )

            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if success:
                self._log(f"コマンド成功: {stdout[:100]}...")
            else:
                self._log(
                    f"コマンド失敗 (終了コード: {result.returncode}): {stderr[:100]}..."
                )

            return success, stdout, stderr

        except subprocess.TimeoutExpired:
            self._log(f"コマンドタイムアウト: {' '.join(command)}")
            return False, "", "コマンドがタイムアウトしました"
        except Exception as e:
            self._log(f"コマンド実行エラー: {e}")
            return False, "", str(e)

    def check_homebrew(self) -> bool:
        """Homebrewがインストールされているかチェック"""
        self._log("Homebrew の存在確認中...")

        # brewコマンドの存在確認
        if shutil.which("brew") is None:
            self._log("Homebrew が見つかりません")
            return False

        # brewコマンドの動作確認
        success, stdout, stderr = self._run_command(["brew", "--version"])
        if success:
            self._log(
                f"Homebrew 確認完了: {stdout.split()[1] if stdout.split() else 'バージョン不明'}"
            )
            return True
        else:
            self._log(f"Homebrew の動作確認に失敗: {stderr}")
            return False

    def check_displayplacer(self) -> bool:
        """displayplacerがインストールされているかチェック"""
        self._log("displayplacer の存在確認中...")

        # displayplacerコマンドの存在確認
        if shutil.which("displayplacer") is None:
            self._log("displayplacer が見つかりません")
            return False

        # displayplacerコマンドの動作確認
        success, stdout, stderr = self._run_command(["displayplacer", "--version"])
        if success:
            self._log(f"displayplacer 確認完了")
            return True
        else:
            # --versionオプションがない場合があるので、helpで確認
            success, stdout, stderr = self._run_command(["displayplacer", "--help"])
            if success and "displayplacer" in stdout.lower():
                self._log("displayplacer 確認完了")
                return True
            else:
                self._log(f"displayplacer の動作確認に失敗: {stderr}")
                return False

    def check_gnu_grep(self) -> bool:
        """GNU grepがインストールされているかチェック"""
        self._log("GNU grep の存在確認中...")

        # HomebrewのGNU grepを確認（ggrep, gegrep, gfgrep）
        homebrew_grep_commands = [
            "ggrep",  # GNU grep
            "gegrep",  # GNU egrep
            "gfgrep",  # GNU fgrep
        ]

        for grep_cmd in homebrew_grep_commands:
            if shutil.which(grep_cmd):
                success, stdout, stderr = self._run_command([grep_cmd, "--version"])
                if success and "GNU grep" in stdout:
                    self._log(f"GNU grep 確認完了: {grep_cmd}")
                    return True

        # Homebrewのインストールパスを直接確認
        homebrew_grep_paths = [
            "/opt/homebrew/opt/grep/bin/ggrep",  # Apple Silicon Mac
            "/usr/local/opt/grep/bin/ggrep",  # Intel Mac
        ]

        for grep_path in homebrew_grep_paths:
            if Path(grep_path).exists():
                success, stdout, stderr = self._run_command([grep_path, "--version"])
                if success and "GNU grep" in stdout:
                    self._log(f"GNU grep 確認完了: {grep_path}")
                    return True

        # システムのgrepコマンドの存在確認
        grep_path = shutil.which("grep")
        if grep_path is None:
            self._log("grep が見つかりません")
            return False

        # GNU grepかどうか確認
        success, stdout, stderr = self._run_command(["grep", "--version"])
        if success and "GNU grep" in stdout:
            self._log("GNU grep 確認完了")
            return True
        else:
            self._log("BSD grep が検出されました。GNU grep が必要です")
            return False

    def install_displayplacer(self) -> bool:
        """displayplacerをインストール"""
        self._log("displayplacer のインストールを開始...")

        if not self.check_homebrew():
            print("エラー: Homebrew が必要ですが見つかりません")
            return False

        success, stdout, stderr = self._run_command(
            ["brew", "install", "jakehilborn/jakehilborn/displayplacer"], timeout=120
        )

        if success:
            print("displayplacer のインストールが完了しました")
            return True
        else:
            print(f"displayplacer のインストールに失敗しました: {stderr}")
            self._print_displayplacer_troubleshooting()
            return False

    def _print_displayplacer_troubleshooting(self) -> None:
        """displayplacer インストール失敗時のトラブルシューティングガイド"""
        print("\nトラブルシューティング:")
        print("1. Homebrew を更新してください:")
        print("   brew update")
        print("2. tap を追加してから再度インストールしてください:")
        print("   brew tap jakehilborn/jakehilborn")
        print("   brew install displayplacer")
        print("3. 手動でダウンロードしてインストールしてください:")
        print("   https://github.com/jakehilborn/displayplacer/releases")
        print("4. Homebrew の診断を実行してください:")
        print("   brew doctor")

    def install_gnu_grep(self) -> bool:
        """GNU grepをインストール"""
        self._log("GNU grep のインストールを開始...")

        if not self.check_homebrew():
            print("エラー: Homebrew が必要ですが見つかりません")
            return False

        success, stdout, stderr = self._run_command(
            ["brew", "install", "grep"], timeout=120
        )

        if success:
            print("GNU grep のインストールが完了しました")
            print(
                "注意: Homebrew の GNU grep は 'ggrep' コマンドとしてインストールされます"
            )
            print("  - 通常の grep の代わりに ggrep を使用してください")
            print("  - または、以下を ~/.zshrc に追加して PATH を設定してください:")
            print(
                '    export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"  # Apple Silicon Mac'
            )
            print(
                '    export PATH="/usr/local/opt/grep/libexec/gnubin:$PATH"     # Intel Mac'
            )
            return True
        else:
            print(f"GNU grep のインストールに失敗しました: {stderr}")
            self._print_gnu_grep_troubleshooting()
            return False

    def _print_gnu_grep_troubleshooting(self) -> None:
        """GNU grep インストール失敗時のトラブルシューティングガイド"""
        print("\nトラブルシューティング:")
        print("1. Homebrew を更新してください:")
        print("   brew update")
        print("2. 手動でインストールを試してください:")
        print("   brew install grep")
        print("3. 既にインストール済みの場合、PATH を確認してください:")
        print("   echo $PATH")
        print("4. Homebrew の診断を実行してください:")
        print("   brew doctor")

    def check_all_dependencies(self) -> Tuple[bool, dict]:
        """
        すべての依存関係をチェック

        Returns:
            Tuple[bool, dict]: (すべて利用可能フラグ, 各依存関係の状態)
        """
        print("依存関係をチェック中...")

        status = {
            "homebrew": self.check_homebrew(),
            "displayplacer": self.check_displayplacer(),
            "gnu_grep": self.check_gnu_grep(),
        }

        # 結果表示
        for tool, available in status.items():
            status_text = "✓ 利用可能" if available else "✗ 未インストール"
            print(f"  {tool}: {status_text}")

        all_available = all(status.values())
        return all_available, status

    def install_missing_dependencies(self, status: dict) -> bool:
        """不足している依存関係をインストール"""
        success = True

        if not status["homebrew"]:
            print("\nHomebrew が見つかりません。")
            print("以下のコマンドでインストールしてください：")
            print(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            )
            print("\nインストール後、以下を実行してください：")
            print("1. シェルを再起動するか、以下のコマンドを実行:")
            print('   eval "$(/opt/homebrew/bin/brew shellenv)"  # Apple Silicon Mac')
            print('   eval "$(/usr/local/bin/brew shellenv)"     # Intel Mac')
            print("2. 再度このプログラムを実行してください")
            return False

        if not status["displayplacer"]:
            print("\ndisplayplacer をインストール中...")
            if not self.install_displayplacer():
                success = False

        if not status["gnu_grep"]:
            print("\nGNU grep をインストール中...")
            if not self.install_gnu_grep():
                success = False

        return success

    def ensure_dependencies(self) -> bool:
        """
        依存関係を確認し、不足している場合はインストール

        Returns:
            bool: すべての依存関係が利用可能になったかどうか
        """
        all_available, status = self.check_all_dependencies()

        if all_available:
            print("すべての依存関係が利用可能です")
            return True

        print("\n不足している依存関係をインストールします...")
        install_success = self.install_missing_dependencies(status)

        if install_success:
            # 再チェック
            print("\n依存関係を再チェック中...")
            all_available, _ = self.check_all_dependencies()

            if all_available:
                print("すべての依存関係のインストールが完了しました")
                return True
            else:
                print("一部の依存関係のインストールに失敗しました")
                return False
        else:
            print("依存関係のインストールに失敗しました")
            return False
