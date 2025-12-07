#!/usr/bin/env python3
"""
LayoutSaver の単体テスト
"""
import json
import sys
import tempfile
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from display_layout_manager.config_manager import ConfigPattern, Configuration
from display_layout_manager.layout_saver import LayoutSaver, SaveResult


def test_generate_pattern_name():
    """パターン名生成のテスト"""
    print("\n=== test_generate_pattern_name ===")

    saver = LayoutSaver(verbose=True)

    # 単一ディスプレイ
    screen_ids_single = ["37D8832A-2D66-02CA-B9F7-8F30A301B230"]
    pattern_name = saver.generate_pattern_name(screen_ids_single)
    print(f"単一ディスプレイのパターン名: {pattern_name}")

    assert "Single_Display" in pattern_name, "単一ディスプレイのパターン名が正しくありません"
    assert "37D8832A" in pattern_name, "Screen IDの一部が含まれていません"

    # 複数ディスプレイ
    screen_ids_multiple = [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230",
        "69733B7E-4C7B-8BDB-11A0-C8F9D6A3E2F1",
    ]
    pattern_name = saver.generate_pattern_name(screen_ids_multiple)
    print(f"複数ディスプレイのパターン名: {pattern_name}")

    assert "2_Displays" in pattern_name, "複数ディスプレイのパターン名が正しくありません"
    assert "37D8832A" in pattern_name, "最初のScreen IDの一部が含まれていません"
    assert "69733B7E" in pattern_name, "2番目のScreen IDの一部が含まれていません"

    print("✓ test_generate_pattern_name 成功")


def test_extract_current_command():
    """現在設定コマンド抽出のテスト"""
    print("\n=== test_extract_current_command ===")

    saver = LayoutSaver(verbose=True)

    # テスト用のdisplayplacer出力
    test_output = """
Persistent screen id: 37D8832A-2D66-02CA-B9F7-8F30A301B230
Resolution: 1920x1080
Origin: (0,0) - main display
Rotation: 0

Execute the command below to set your screens to the current arrangement:

displayplacer "id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1920x1080 origin:(0,0) degree:0"
"""

    command = saver.extract_current_command(test_output)
    print(f"抽出されたコマンド: {command[:50]}...")

    assert command.startswith("displayplacer"), "コマンドがdisplayplacerで始まっていません"
    assert "37D8832A-2D66-02CA-B9F7-8F30A301B230" in command, "Screen IDが含まれていません"
    assert "res:1920x1080" in command, "解像度が含まれていません"

    print("✓ test_extract_current_command 成功")


def test_extract_current_command_empty():
    """空の出力からのコマンド抽出テスト"""
    print("\n=== test_extract_current_command_empty ===")

    saver = LayoutSaver(verbose=True)

    # 空の出力
    test_output = ""

    command = saver.extract_current_command(test_output)
    print(f"抽出されたコマンド: '{command}'")

    assert command == "", "空の出力から空文字列が返されませんでした"

    print("✓ test_extract_current_command_empty 成功")


def test_find_existing_pattern_by_screen_ids():
    """既存パターン検索のテスト"""
    print("\n=== test_find_existing_pattern_by_screen_ids ===")

    saver = LayoutSaver(verbose=True)

    # テスト用パターン
    patterns = [
        ConfigPattern(
            name="Pattern 1",
            description="Test pattern 1",
            screen_ids=["37D8832A-2D66-02CA-B9F7-8F30A301B230"],
            command="displayplacer test1",
        ),
        ConfigPattern(
            name="Pattern 2",
            description="Test pattern 2",
            screen_ids=[
                "69733B7E-4C7B-8BDB-11A0-C8F9D6A3E2F1",
                "37D8832A-2D66-02CA-B9F7-8F30A301B230",
            ],
            command="displayplacer test2",
        ),
    ]

    # 存在するパターンを検索
    screen_ids_existing = ["37D8832A-2D66-02CA-B9F7-8F30A301B230"]
    found_pattern = saver.find_existing_pattern_by_screen_ids(
        screen_ids_existing, patterns
    )

    print(f"検索結果: {found_pattern.name if found_pattern else 'なし'}")

    assert found_pattern is not None, "既存パターンが見つかりませんでした"
    assert found_pattern.name == "Pattern 1", "間違ったパターンが見つかりました"

    # 存在しないパターンを検索
    screen_ids_not_existing = ["AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA"]
    found_pattern = saver.find_existing_pattern_by_screen_ids(
        screen_ids_not_existing, patterns
    )

    print(f"検索結果（存在しない）: {found_pattern.name if found_pattern else 'なし'}")

    assert found_pattern is None, "存在しないパターンが見つかってしまいました"

    # 順序が異なるScreen IDsでも検索できることを確認
    screen_ids_reversed = [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230",
        "69733B7E-4C7B-8BDB-11A0-C8F9D6A3E2F1",
    ]
    found_pattern = saver.find_existing_pattern_by_screen_ids(
        screen_ids_reversed, patterns
    )

    print(f"検索結果（順序逆）: {found_pattern.name if found_pattern else 'なし'}")

    assert found_pattern is not None, "順序が異なるScreen IDsで検索できませんでした"
    assert found_pattern.name == "Pattern 2", "間違ったパターンが見つかりました"

    print("✓ test_find_existing_pattern_by_screen_ids 成功")


def test_save_config_to_file():
    """設定ファイル保存のテスト"""
    print("\n=== test_save_config_to_file ===")

    saver = LayoutSaver(verbose=True)

    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = Path(f.name)

    try:
        # テスト用設定
        config = Configuration(
            version="1.0",
            patterns=[
                ConfigPattern(
                    name="Test Pattern",
                    description="Test description",
                    screen_ids=["37D8832A-2D66-02CA-B9F7-8F30A301B230"],
                    command="displayplacer test",
                )
            ],
        )

        # 保存
        success = saver.save_config_to_file(config, temp_path)
        print(f"保存結果: {'✓ 成功' if success else '✗ 失敗'}")

        assert success, "設定ファイルの保存に失敗しました"
        assert temp_path.exists(), "設定ファイルが作成されませんでした"

        # 保存された内容を確認
        with open(temp_path, "r", encoding="utf-8") as f:
            saved_data = json.load(f)

        print(f"保存されたデータ: {json.dumps(saved_data, indent=2, ensure_ascii=False)}")

        assert saved_data["version"] == "1.0", "バージョンが正しく保存されていません"
        assert len(saved_data["patterns"]) == 1, "パターン数が正しくありません"
        assert saved_data["patterns"][0]["name"] == "Test Pattern", "パターン名が正しく保存されていません"

        print("✓ test_save_config_to_file 成功")

    finally:
        # 一時ファイルを削除
        if temp_path.exists():
            temp_path.unlink()


def test_save_result_dataclass():
    """SaveResult データクラスのテスト"""
    print("\n=== test_save_result_dataclass ===")

    # 成功ケース
    result_success = SaveResult(
        success=True,
        pattern_name="Test Pattern",
        action="created",
        screen_count=2,
        screen_ids=["ID1", "ID2"],
        message="パターンを作成しました",
    )

    print(f"成功ケース:")
    print(f"  success: {result_success.success}")
    print(f"  pattern_name: {result_success.pattern_name}")
    print(f"  action: {result_success.action}")
    print(f"  message: {result_success.message}")

    assert result_success.success, "successフラグが正しくありません"
    assert result_success.action == "created", "actionが正しくありません"
    assert result_success.screen_count == 2, "screen_countが正しくありません"
    assert len(result_success.screen_ids) == 2, "screen_idsの数が正しくありません"

    # 失敗ケース
    result_failure = SaveResult(
        success=False,
        pattern_name="",
        action="",
        screen_count=0,
        screen_ids=[],
        message="エラーが発生しました",
        error_details="詳細なエラー情報",
    )

    print(f"失敗ケース:")
    print(f"  success: {result_failure.success}")
    print(f"  message: {result_failure.message}")
    print(f"  error_details: {result_failure.error_details}")

    assert not result_failure.success, "successフラグが正しくありません"
    assert result_failure.error_details is not None, "error_detailsが設定されていません"

    print("✓ test_save_result_dataclass 成功")


def main():
    """メイン関数"""
    print("=" * 80)
    print("LayoutSaver 単体テスト")
    print("=" * 80)

    tests = [
        test_generate_pattern_name,
        test_extract_current_command,
        test_extract_current_command_empty,
        test_find_existing_pattern_by_screen_ids,
        test_save_config_to_file,
        test_save_result_dataclass,
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
