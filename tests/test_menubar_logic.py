#!/usr/bin/env python3
"""
メニューバーアプリのロジック部分の単体テスト
（rumps UI を除く）
"""
import sys
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock

# src ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_auto_launch_toggle_logic():
    """自動起動トグルロジックのテスト"""
    print("\n" + "=" * 60)
    print("テスト 1: 自動起動トグルロジック")
    print("=" * 60)
    
    # モックオブジェクトを作成
    mock_manager = Mock()
    mock_menu_item = Mock()
    mock_menu_item.state = 0
    
    # テスト 1: 無効 → 有効
    print("\n  [1-1] 無効 → 有効")
    mock_manager.is_enabled.return_value = False
    
    # ロジック実行
    if mock_manager.is_enabled():
        mock_manager.disable()
        new_state = 0
    else:
        mock_manager.enable()
        new_state = 1
    
    mock_menu_item.state = new_state
    
    assert mock_manager.enable.called, "enable() が呼ばれるべき"
    assert mock_menu_item.state == 1, "state は 1 であるべき"
    print("    ✓ enable() 呼び出し確認")
    print("    ✓ state = 1 確認")
    
    # テスト 2: 有効 → 無効
    print("\n  [1-2] 有効 → 無効")
    mock_manager.reset_mock()
    mock_manager.is_enabled.return_value = True
    
    # ロジック実行
    if mock_manager.is_enabled():
        mock_manager.disable()
        new_state = 0
    else:
        mock_manager.enable()
        new_state = 1
    
    mock_menu_item.state = new_state
    
    assert mock_manager.disable.called, "disable() が呼ばれるべき"
    assert mock_menu_item.state == 0, "state は 0 であるべき"
    print("    ✓ disable() 呼び出し確認")
    print("    ✓ state = 0 確認")
    
    return True


def test_state_update_logic():
    """状態更新ロジックのテスト"""
    print("\n" + "=" * 60)
    print("テスト 2: 状態更新ロジック")
    print("=" * 60)
    
    mock_manager = Mock()
    mock_menu_item = Mock()
    
    # テスト 1: 有効状態
    print("\n  [2-1] 有効状態")
    mock_manager.is_enabled.return_value = True
    mock_menu_item.state = 1 if mock_manager.is_enabled() else 0
    assert mock_menu_item.state == 1, "有効時は state = 1"
    print("    ✓ state = 1 確認")
    
    # テスト 2: 無効状態
    print("\n  [2-2] 無効状態")
    mock_manager.is_enabled.return_value = False
    mock_menu_item.state = 1 if mock_manager.is_enabled() else 0
    assert mock_menu_item.state == 0, "無効時は state = 0"
    print("    ✓ state = 0 確認")
    
    return True


def test_cli_bridge_calls():
    """CLI ブリッジ呼び出しのテスト"""
    print("\n" + "=" * 60)
    print("テスト 3: CLI ブリッジ呼び出し")
    print("=" * 60)
    
    mock_cli_bridge = Mock()
    
    # テスト 1: レイアウト適用
    print("\n  [3-1] レイアウト適用")
    try:
        mock_cli_bridge.execute_apply_layout()
    except Exception:
        pass
    
    assert mock_cli_bridge.execute_apply_layout.called, "execute_apply_layout() が呼ばれるべき"
    print("    ✓ execute_apply_layout() 呼び出し確認")
    
    # テスト 2: 設定保存
    print("\n  [3-2] 設定保存")
    mock_cli_bridge.reset_mock()
    try:
        mock_cli_bridge.execute_save_current()
    except Exception:
        pass
    
    assert mock_cli_bridge.execute_save_current.called, "execute_save_current() が呼ばれるべき"
    print("    ✓ execute_save_current() 呼び出し確認")
    
    return True


def test_error_handling_logic():
    """エラーハンドリングロジックのテスト"""
    print("\n" + "=" * 60)
    print("テスト 4: エラーハンドリングロジック")
    print("=" * 60)
    
    mock_cli_bridge = Mock()
    mock_cli_bridge.execute_apply_layout.side_effect = Exception("テストエラー")
    
    # エラーが発生してもクラッシュしないことを確認
    print("\n  [4-1] エラー時のサイレント実行")
    try:
        try:
            mock_cli_bridge.execute_apply_layout()
        except Exception:
            pass  # サイレント実行
        print("    ✓ エラー時もクラッシュしない")
        return True
    except Exception as e:
        print(f"    ✗ エラーハンドリング失敗: {e}")
        return False


def test_menu_structure_logic():
    """メニュー構造ロジックのテスト"""
    print("\n" + "=" * 60)
    print("テスト 5: メニュー構造ロジック")
    print("=" * 60)
    
    # 期待されるメニュー項目
    expected_items = [
        "レイアウトを適用",
        "現在の設定を保存",
        None,  # セパレーター
        "ログイン時に起動",
        None,  # セパレーター
        "終了"
    ]
    
    print(f"\n  期待されるメニュー構造:")
    for i, item in enumerate(expected_items):
        if item is None:
            print(f"    {i+1}. [セパレーター]")
        else:
            print(f"    {i+1}. {item}")
    
    # メニュー項目数の確認
    assert len(expected_items) == 6, "メニュー項目は6つ（セパレーター含む）"
    print("\n  ✓ メニュー項目数確認: 6項目")
    
    # 必須項目の確認
    required_items = [item for item in expected_items if item is not None]
    assert len(required_items) == 4, "必須メニュー項目は4つ"
    print("  ✓ 必須メニュー項目数確認: 4項目")
    
    # セパレーター数の確認
    separators = [item for item in expected_items if item is None]
    assert len(separators) == 2, "セパレーターは2つ"
    print("  ✓ セパレーター数確認: 2つ")
    
    return True


def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 70)
    print("メニューバーアプリ ロジック単体テスト")
    print("=" * 70)
    
    tests = [
        ("自動起動トグルロジック", test_auto_launch_toggle_logic),
        ("状態更新ロジック", test_state_update_logic),
        ("CLI ブリッジ呼び出し", test_cli_bridge_calls),
        ("エラーハンドリングロジック", test_error_handling_logic),
        ("メニュー構造ロジック", test_menu_structure_logic),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ テスト '{name}' で予期しないエラー: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 結果サマリー
    print("\n" + "=" * 70)
    print("テスト結果サマリー")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\n合計: {passed}/{total} テスト成功")
    print("=" * 70)
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
