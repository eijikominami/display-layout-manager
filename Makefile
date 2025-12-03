# Display Layout Manager - Makefile

.PHONY: help install install-dev test clean build upload

# デフォルトターゲット
help:
	@echo "Display Layout Manager - 利用可能なコマンド:"
	@echo ""
	@echo "  install      - パッケージをインストール"
	@echo "  install-dev  - 開発モードでインストール"
	@echo "  test         - テストを実行"
	@echo "  clean        - ビルド成果物を削除"
	@echo "  build        - パッケージをビルド"
	@echo "  upload       - PyPI にアップロード"
	@echo "  run          - アプリケーションを実行"
	@echo ""

# パッケージインストール
install:
	pip install .

# 開発モードでインストール
install-dev:
	pip install -e .

# テスト実行（将来実装予定）
test:
	@echo "テスト機能は後続のタスクで実装予定"
	# python -m pytest

# ビルド成果物の削除
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# パッケージビルド
build: clean
	python setup.py sdist bdist_wheel

# PyPI アップロード（将来実装予定）
upload: build
	@echo "PyPI アップロード機能は将来実装予定"
	# twine upload dist/*

# アプリケーション実行
run:
	python -m display_layout_manager.main

# 開発用：アプリケーション実行（詳細ログ付き）
run-verbose:
	python -m display_layout_manager.main --verbose

# 開発用：ドライラン実行
run-dry:
	python -m display_layout_manager.main --dry-run --verbose