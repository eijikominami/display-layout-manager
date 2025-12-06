#!/usr/bin/env python3
"""
DisplayManager の単体テスト
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from display_layout_manager.display_manager import DisplayConfiguration, DisplayManager


def test_extract_screen_ids():
    """Screen ID 抽出機能のテスト"""
    print("\n=== test_extract_screen_ids ===")

    manager = DisplayManager(verbose=True)

    # テスト用のdisplayplacer出力
    test_output = """
Persistent screen id: 37D8832A-2D66-02CA-B9F7-8F30A301B230
Resolution: 1920x1080
Origin: (0,0) - main display
Rotation: 0

Persistent screen id: 69733B7E-4C7B-8BDB-11A0-C8F9D6A3E2F1
Resolution: 2560x1440
Origin: (1920,0)
Rotation: 0
"""

    screen_ids = manager.extract_screen_ids(test_output)

    print(f"抽出されたScreen IDs: {len(screen_ids)}個")
    for screen_id in screen_ids:
        print(f"  - {screen_id}")

    assert (
        len(screen_ids) == 2
    ), f"2個のScreen IDを期待しましたが、{len(screen_ids)}個でした"
    assert (
        "37D8832A-2D66-02CA-B9F7-8F30A301B230" in screen_ids
    ), "最初のScreen IDが見つかりません"
    assert (
        "69733B7E-4C7B-8BDB-11A0-C8F9D6A3E2F1" in screen_ids
    ), "2番目のScreen IDが見つかりません"

    print("✓ test_extract_screen_ids 成功")


def test_extract_screen_ids_single():
    """単一ディスプレイのScreen ID抽出テスト"""
    print("\n=== test_extract_screen_ids_single ===")

    manager = DisplayManager(verbose=True)

    # 単一ディスプレイの出力
    test_output = """
Persistent screen id: 37D8832A-2D66-02CA-B9F7-8F30A301B230
Resolution: 1920x1080
Origin: (0,0) - main display
Rotation: 0
"""

    screen_ids = manager.extract_screen_ids(test_output)

    print(f"抽出されたScreen IDs: {len(screen_ids)}個")

    assert (
        len(screen_ids) == 1
    ), f"1個のScreen IDを期待しましたが、{len(screen_ids)}個でした"
    assert (
        "37D8832A-2D66-02CA-B9F7-8F30A301B230" in screen_ids
    ), "Screen IDが見つかりません"

    print("✓ test_extract_screen_ids_single 成功")


def test_extract_screen_ids_empty():
    """空の出力からのScreen ID抽出テスト"""
    print("\n=== test_extract_screen_ids_empty ===")

    manager = DisplayManager(verbose=True)

    # 空の出力
    test_output = ""

    screen_ids = manager.extract_screen_ids(test_output)

    print(f"抽出されたScreen IDs: {len(screen_ids)}個")

    assert (
        len(screen_ids) == 0
    ), f"0個のScreen IDを期待しましたが、{len(screen_ids)}個でした"

    print("✓ test_extract_screen_ids_empty 成功")


def test_get_current_displays():
    """現在のディスプレイ構成取得のテスト"""
    print("\n=== test_get_current_displays ===")

    manager = DisplayManager(verbose=True)

    success, config, error = manager.get_current_displays()

    print(f"結果: {'✓ 成功' if success else '✗ 失敗'}")

    if success:
        print(f"検出されたディスプレイ: {len(config.screen_ids)}個")
        for i, screen_id in enumerate(config.screen_ids, 1):
            print(f"  {i}. {screen_id}")

        assert config is not None, "DisplayConfiguration が None です"
        assert len(config.screen_ids) > 0, "Screen IDが検出されませんでした"
        assert config.timestamp is not None, "タイムスタンプが設定されていません"
        assert config.raw_output, "生出力が空です"
    else:
        print(f"エラー: {error}")
        assert False, f"ディスプレイ構成の取得に失敗しました: {error}"

    print("✓ test_get_current_displays 成功")


def test_validate_displayplacer_output():
    """displayplacer出力の検証テスト"""
    print("\n=== test_validate_displayplacer_output ===")

    manager = DisplayManager(verbose=True)

    # 有効な出力
    valid_output = """
Persistent screen id: 37D8832A-2D66-02CA-B9F7-8F30A301B230
Resolution: 1920x1080
"""

    is_valid, issues = manager.validate_displayplacer_output(valid_output)
    print(f"有効な出力の検証: {'✓ 有効' if is_valid else '✗ 無効'}")
    if issues:
        print(f"  問題: {issues}")

    assert is_valid, f"有効な出力が無効と判定されました: {issues}"

    # 無効な出力（Screen IDなし）
    invalid_output = """
Resolution: 1920x1080
Origin: (0,0)
"""

    is_valid, issues = manager.validate_displayplacer_output(invalid_output)
    print(f"無効な出力の検証: {'✓ 無効と判定' if not is_valid else '✗ 有効と判定'}")
    if issues:
        print(f"  問題: {issues}")

    assert not is_valid, "無効な出力が有効と判定されました"
    assert len(issues) > 0, "問題が検出されませんでした"

    # 空の出力
    empty_output = ""

    is_valid, issues = manager.validate_displayplacer_output(empty_output)
    print(f"空の出力の検証: {'✓ 無効と判定' if not is_valid else '✗ 有効と判定'}")

    assert not is_valid, "空の出力が有効と判定されました"

    print("✓ test_validate_displayplacer_output 成功")


def test_get_screen_ids():
    """Screen IDリスト取得のテスト"""
    print("\n=== test_get_screen_ids ===")

    manager = DisplayManager(verbose=False)

    screen_ids = manager.get_screen_ids()

    print(f"取得されたScreen IDs: {len(screen_ids)}個")
    for i, screen_id in enumerate(screen_ids, 1):
        print(f"  {i}. {screen_id}")

    assert len(screen_ids) > 0, "Screen IDが取得できませんでした"

    # 2回目の呼び出しでキャッシュが使われることを確認
    screen_ids_2 = manager.get_screen_ids()
    assert screen_ids == screen_ids_2, "キャッシュされた値が異なります"

    print("✓ test_get_screen_ids 成功")


def test_refresh_display_config():
    """ディスプレイ構成の再取得テスト"""
    print("\n=== test_refresh_display_config ===")

    manager = DisplayManager(verbose=True)

    # 初回取得
    success1 = manager.refresh_display_config()
    assert success1, "初回のディスプレイ構成取得に失敗しました"

    screen_ids_1 = manager.get_screen_ids()

    # 再取得
    success2 = manager.refresh_display_config()
    assert success2, "ディスプレイ構成の再取得に失敗しました"

    screen_ids_2 = manager.get_screen_ids()

    # 同じディスプレイ構成であることを確認
    assert screen_ids_1 == screen_ids_2, "再取得後のScreen IDが異なります"

    print("✓ test_refresh_display_config 成功")


def main():
    """メイン関数"""
    print("=" * 80)
    print("DisplayManager 単体テスト")
    print("=" * 80)

    tests = [
        test_extract_screen_ids,
        test_extract_screen_ids_single,
        test_extract_screen_ids_empty,
        test_get_current_displays,
        test_validate_displayplacer_output,
        test_get_screen_ids,
        test_refresh_display_config,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 失敗: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} エラー: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"テスト結果: {passed}/{len(tests)} 成功, {failed}/{len(tests)} 失敗")
    print("=" * 80)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
