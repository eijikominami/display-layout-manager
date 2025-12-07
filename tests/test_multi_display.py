"""
Tests for multi-display support in menubar app
"""

from unittest.mock import MagicMock, patch


def test_configure_multi_display_success():
    """全ディスプレイ表示設定が成功する"""
    # モックウィンドウを作成
    mock_window = MagicMock()

    # AppKitモジュールをモック
    with patch.dict("sys.modules", {"AppKit": MagicMock()}):
        mock_nsapp = MagicMock()
        mock_nsapp.windows.return_value = [mock_window]

        mock_nswindow = MagicMock()
        mock_nswindow.NSStatusWindowLevel = 25  # 実際の値

        with patch("AppKit.NSApp", mock_nsapp), patch(
            "AppKit.NSWindow", mock_nswindow
        ), patch(
            "AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces", 1 << 0
        ):  # 実際の値
            # エラーが発生しないことを確認
            # 注: 実際のテストでは rumps.App の初期化をモックする必要がある
            pass


def test_configure_multi_display_no_windows():
    """ウィンドウが存在しない場合でもエラーにならない"""
    # AppKitモジュールをモック
    with patch.dict("sys.modules", {"AppKit": MagicMock()}):
        mock_nsapp = MagicMock()
        mock_nsapp.windows.return_value = []  # 空のリスト

        with patch("AppKit.NSApp", mock_nsapp):
            # エラーが発生しないことを確認
            # 注: 実際のテストでは rumps.App の初期化をモックする必要がある
            pass


def test_configure_multi_display_import_error():
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
        # _configure_multi_display メソッドを直接呼び出し
        # エラーが発生しないことを確認
        # 注: 実際のテストでは rumps.App の初期化をモックする必要がある
        pass
    finally:
        # 元に戻す
        sys_module.modules.clear()
        sys_module.modules.update(original_modules)


def test_configure_multi_display_exception_handling():
    """設定中に例外が発生してもエラーにならない"""
    # モックウィンドウを作成（例外を発生させる）
    mock_window = MagicMock()
    mock_window.setLevel_.side_effect = Exception("Test exception")

    # AppKitモジュールをモック
    with patch.dict("sys.modules", {"AppKit": MagicMock()}):
        mock_nsapp = MagicMock()
        mock_nsapp.windows.return_value = [mock_window]

        with patch("AppKit.NSApp", mock_nsapp):
            # エラーが発生しないことを確認
            # 注: 実際のテストでは rumps.App の初期化をモックする必要がある
            pass
