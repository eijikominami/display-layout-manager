"""
Tests for SingleInstanceManager
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from display_layout_manager.single_instance_manager import SingleInstanceManager


@pytest.fixture
def temp_pid_file(tmp_path):
    """一時的なPIDファイルパスを提供するフィクスチャ"""
    pid_file = tmp_path / "test_menubar.pid"
    return pid_file


@pytest.fixture
def instance_manager(temp_pid_file):
    """テスト用のSingleInstanceManagerインスタンスを提供"""
    manager = SingleInstanceManager()
    # テスト用に一時ファイルパスを使用
    manager.pid_file = temp_pid_file
    return manager


def test_is_already_running_no_pid_file(instance_manager):
    """PIDファイルが存在しない場合、起動していないと判定される"""
    assert not instance_manager.is_already_running()


def test_is_already_running_with_valid_pid(instance_manager):
    """有効なPIDファイルが存在する場合、起動していると判定される"""
    # 現在のプロセスのPIDを書き込む
    with open(instance_manager.pid_file, "w") as f:
        f.write(str(os.getpid()))

    assert instance_manager.is_already_running()


def test_is_already_running_with_invalid_pid(instance_manager):
    """無効なPIDファイルが存在する場合、起動していないと判定される"""
    # 存在しないPIDを書き込む
    with open(instance_manager.pid_file, "w") as f:
        f.write("999999")

    assert not instance_manager.is_already_running()


def test_is_already_running_with_corrupted_pid_file(instance_manager):
    """破損したPIDファイルが存在する場合、起動していないと判定される"""
    # 無効な内容を書き込む
    with open(instance_manager.pid_file, "w") as f:
        f.write("invalid_pid")

    assert not instance_manager.is_already_running()


def test_acquire_lock_success(instance_manager):
    """ロック取得が成功する"""
    assert instance_manager.acquire_lock()

    # PIDファイルが作成されている
    assert instance_manager.pid_file.exists()

    # 現在のプロセスIDが書き込まれている
    with open(instance_manager.pid_file, "r") as f:
        pid = int(f.read().strip())
    assert pid == os.getpid()

    # ファイル権限が600である
    stat_info = os.stat(instance_manager.pid_file)
    assert stat_info.st_mode & 0o777 == 0o600


def test_acquire_lock_already_running(instance_manager):
    """既に起動している場合、ロック取得が失敗する"""
    # 最初のロック取得は成功
    assert instance_manager.acquire_lock()

    # 2回目のロック取得は失敗
    assert not instance_manager.acquire_lock()


def test_release_lock(instance_manager):
    """ロック解放が成功する"""
    # ロックを取得
    instance_manager.acquire_lock()
    assert instance_manager.pid_file.exists()

    # ロックを解放
    instance_manager.release_lock()
    assert not instance_manager.pid_file.exists()


def test_release_lock_no_file(instance_manager):
    """PIDファイルが存在しない場合でもエラーにならない"""
    # PIDファイルが存在しない状態でrelease_lockを呼び出す
    instance_manager.release_lock()
    # エラーが発生しないことを確認（例外が発生しなければOK）


def test_bring_existing_to_front_no_app(instance_manager):
    """既存のアプリが見つからない場合でもエラーにならない"""
    # AppKitモジュール全体をモック
    with patch.dict("sys.modules", {"AppKit": MagicMock()}):
        mock_ns = MagicMock()
        mock_ns.runningApplicationsWithBundleIdentifier_.return_value = []

        with patch("AppKit.NSRunningApplication", mock_ns):
            # エラーが発生しないことを確認
            instance_manager.bring_existing_to_front()


def test_bring_existing_to_front_with_app(instance_manager):
    """既存のアプリが見つかった場合、アクティブ化される"""
    # モックアプリケーションを作成
    mock_app = MagicMock()

    # AppKitモジュール全体をモック
    with patch.dict("sys.modules", {"AppKit": MagicMock()}):
        mock_ns = MagicMock()
        mock_ns.runningApplicationsWithBundleIdentifier_.return_value = [mock_app]

        with patch("AppKit.NSRunningApplication", mock_ns):
            # 既存インスタンスを前面に表示
            instance_manager.bring_existing_to_front()

            # activateWithOptions_が呼ばれたことを確認
            mock_app.activateWithOptions_.assert_called_once()


def test_bring_existing_to_front_import_error(instance_manager):
    """AppKitのインポートに失敗してもエラーにならない"""
    # AppKitのインポートを失敗させる
    import sys as sys_module

    original_modules = sys_module.modules.copy()

    # AppKitを削除
    if "AppKit" in sys_module.modules:
        del sys_module.modules["AppKit"]

    # インポートエラーを発生させる
    sys_module.modules["AppKit"] = None

    try:
        # エラーが発生しないことを確認
        instance_manager.bring_existing_to_front()
    finally:
        # 元に戻す
        sys_module.modules.clear()
        sys_module.modules.update(original_modules)


def test_full_lifecycle(instance_manager):
    """完全なライフサイクルテスト"""
    # 初期状態: 起動していない
    assert not instance_manager.is_already_running()

    # ロック取得: 成功
    assert instance_manager.acquire_lock()

    # 起動中と判定される
    assert instance_manager.is_already_running()

    # 2回目のロック取得: 失敗
    assert not instance_manager.acquire_lock()

    # ロック解放
    instance_manager.release_lock()

    # 起動していないと判定される
    assert not instance_manager.is_already_running()

    # 再度ロック取得: 成功
    assert instance_manager.acquire_lock()

    # クリーンアップ
    instance_manager.release_lock()
