"""
パターンマッチングモジュール
ディスプレイ組み合わせのパターンマッチングを管理
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
from .config_manager import ConfigPattern
from .display_manager import DisplayConfiguration


@dataclass
class MatchResult:
    """マッチ結果クラス"""

    matched: bool
    pattern: Optional[ConfigPattern]
    confidence: float
    match_type: str  # "exact", "partial", "none"
    details: str

    def __post_init__(self):
        """初期化後の処理"""
        if self.matched and self.pattern is None:
            raise ValueError("マッチした場合はパターンが必要です")
        if not self.matched and self.pattern is not None:
            raise ValueError("マッチしなかった場合はパターンは不要です")


class PatternMatcher:
    """パターンマッチングクラス"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """ログ出力（詳細モード時のみ）"""
        if self.verbose:
            print(f"[パターンマッチ] {message}")

    def exact_match(
        self, current_screen_ids: List[str], pattern: ConfigPattern
    ) -> bool:
        """
        完全一致チェック

        Args:
            current_screen_ids: 現在のScreen IDリスト（ソート済み）
            pattern: 設定パターン

        Returns:
            bool: 完全一致するかどうか
        """
        # 両方をソートして比較
        current_sorted = sorted(current_screen_ids)
        pattern_sorted = sorted(pattern.screen_ids)

        is_match = current_sorted == pattern_sorted

        if is_match:
            self._log(f"完全一致: パターン '{pattern.name}'")
        else:
            self._log(
                f"不一致: パターン '{pattern.name}' (現在: {len(current_sorted)}個, パターン: {len(pattern_sorted)}個)"
            )

        return is_match

    def calculate_similarity(
        self, current_screen_ids: List[str], pattern: ConfigPattern
    ) -> float:
        """
        類似度を計算（Jaccard係数を使用）

        Args:
            current_screen_ids: 現在のScreen IDリスト
            pattern: 設定パターン

        Returns:
            float: 類似度（0.0-1.0）
        """
        current_set = set(current_screen_ids)
        pattern_set = set(pattern.screen_ids)

        if not current_set and not pattern_set:
            return 1.0  # 両方とも空の場合は完全一致

        intersection = current_set.intersection(pattern_set)
        union = current_set.union(pattern_set)

        similarity = len(intersection) / len(union) if union else 0.0

        self._log(f"類似度計算: パターン '{pattern.name}' = {similarity:.2f}")

        return similarity

    def find_best_match(
        self, current_screen_ids: List[str], patterns: List[ConfigPattern]
    ) -> MatchResult:
        """
        最適なパターンを検索

        Args:
            current_screen_ids: 現在のScreen IDリスト
            patterns: 設定パターンのリスト

        Returns:
            MatchResult: マッチ結果
        """
        if not patterns:
            return MatchResult(
                matched=False,
                pattern=None,
                confidence=0.0,
                match_type="none",
                details="設定パターンが存在しません",
            )

        if not current_screen_ids:
            return MatchResult(
                matched=False,
                pattern=None,
                confidence=0.0,
                match_type="none",
                details="現在のディスプレイが検出されませんでした",
            )

        self._log(
            f"パターンマッチング開始: 現在のディスプレイ {len(current_screen_ids)}個"
        )
        self._log(f"検索対象パターン: {len(patterns)}個")

        # 完全一致を優先して検索
        for pattern in patterns:
            if self.exact_match(current_screen_ids, pattern):
                return MatchResult(
                    matched=True,
                    pattern=pattern,
                    confidence=1.0,
                    match_type="exact",
                    details=f"完全一致: パターン '{pattern.name}'",
                )

        # 完全一致がない場合、類似度で最適なパターンを検索
        best_pattern = None
        best_similarity = 0.0

        for pattern in patterns:
            similarity = self.calculate_similarity(current_screen_ids, pattern)
            if similarity > best_similarity:
                best_similarity = similarity
                best_pattern = pattern

        # 類似度が一定以上の場合のみ部分一致として扱う
        similarity_threshold = 0.5

        if best_similarity >= similarity_threshold and best_pattern:
            return MatchResult(
                matched=True,
                pattern=best_pattern,
                confidence=best_similarity,
                match_type="partial",
                details=f"部分一致: パターン '{best_pattern.name}' (類似度: {best_similarity:.2f})",
            )
        else:
            # 最も類似度の高いパターンの情報を含める
            if best_pattern:
                details = f"一致するパターンなし (最も近いパターン: '{best_pattern.name}', 類似度: {best_similarity:.2f})"
            else:
                details = "一致するパターンなし"

            return MatchResult(
                matched=False,
                pattern=None,
                confidence=0.0,
                match_type="none",
                details=details,
            )

    def match_display_configuration(
        self, display_config: DisplayConfiguration, patterns: List[ConfigPattern]
    ) -> MatchResult:
        """
        ディスプレイ構成とパターンのマッチング

        Args:
            display_config: 現在のディスプレイ構成
            patterns: 設定パターンのリスト

        Returns:
            MatchResult: マッチ結果
        """
        self._log(
            f"ディスプレイ構成マッチング開始: {len(display_config.screen_ids)}個のディスプレイ"
        )

        return self.find_best_match(display_config.screen_ids, patterns)

    def validate_patterns(
        self, patterns: List[ConfigPattern]
    ) -> Tuple[bool, List[str]]:
        """
        パターンリストの検証

        Args:
            patterns: 設定パターンのリスト

        Returns:
            Tuple[bool, List[str]]: (有効フラグ, 問題のリスト)
        """
        issues = []

        if not patterns:
            issues.append("パターンが定義されていません")
            return False, issues

        # パターン名の重複チェック
        pattern_names = [p.name for p in patterns]
        if len(pattern_names) != len(set(pattern_names)):
            issues.append("重複するパターン名があります")

        # 各パターンの検証
        for i, pattern in enumerate(patterns):
            if not pattern.screen_ids:
                issues.append(f"パターン '{pattern.name}': Screen IDが空です")

            # Screen IDの重複チェック
            if len(pattern.screen_ids) != len(set(pattern.screen_ids)):
                issues.append(f"パターン '{pattern.name}': 重複するScreen IDがあります")

            # コマンドの基本チェック
            if not pattern.command.strip().startswith("displayplacer"):
                issues.append(
                    f"パターン '{pattern.name}': コマンドが 'displayplacer' で開始していません"
                )

        return len(issues) == 0, issues

    def get_match_summary(
        self, match_result: MatchResult, current_screen_ids: List[str]
    ) -> str:
        """
        マッチ結果のサマリーを生成

        Args:
            match_result: マッチ結果
            current_screen_ids: 現在のScreen IDリスト

        Returns:
            str: サマリー文字列
        """
        summary_lines = []

        summary_lines.append(f"現在のディスプレイ: {len(current_screen_ids)}個")

        if match_result.matched:
            summary_lines.append(f"マッチしたパターン: {match_result.pattern.name}")
            summary_lines.append(f"マッチタイプ: {match_result.match_type}")
            summary_lines.append(f"信頼度: {match_result.confidence:.2f}")
            if match_result.pattern.description:
                summary_lines.append(f"説明: {match_result.pattern.description}")
        else:
            summary_lines.append("マッチするパターンなし")

        summary_lines.append(f"詳細: {match_result.details}")

        return "\n".join(summary_lines)
