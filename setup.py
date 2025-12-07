#!/usr/bin/env python3
"""
Display Layout Manager セットアップスクリプト
"""

from pathlib import Path

from setuptools import find_packages, setup

# バージョン情報を読み込み
version_file = Path(__file__).parent / "src" / "display_layout_manager" / "__init__.py"
version = {}
with open(version_file, encoding="utf-8") as f:
    exec(f.read(), version)

# README.mdを読み込み
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="display-layout-manager",
    version=version["__version__"],
    description="macOS用ディスプレイレイアウト自動設定ツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Display Layout Manager Team",
    author_email="eijikominami@gmail.com",
    url="https://github.com/eijikominami/display-layout-manager",
    license="MIT",
    # パッケージ設定
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # Python バージョン要件
    python_requires=">=3.8",
    # 依存関係
    install_requires=[
        "rumps>=0.4.0",  # メニューバーアプリフレームワーク
        "pyobjc-framework-Cocoa>=9.0",  # macOS API アクセス
    ],
    # 開発依存関係
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "coverage>=7.3.0",
            "black>=23.12.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
            "pre-commit>=3.6.0",
        ],
    },
    # エントリーポイント
    entry_points={
        "console_scripts": [
            "display-layout-manager=display_layout_manager.main:main",
            "display-layout-menubar=display_layout_manager.menubar:main",
        ],
    },
    # 分類
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Desktop Environment",
        "Topic :: System :: Hardware",
        "Topic :: Utilities",
    ],
    # キーワード
    keywords="macos display monitor layout displayplacer automation",
    # プロジェクトURL
    project_urls={
        "Bug Reports": "https://github.com/eijikominami/display-layout-manager/issues",
        "Source": "https://github.com/eijikominami/display-layout-manager",
        "Documentation": "https://github.com/eijikominami/display-layout-manager/blob/main/README.md",
    },
    # 追加ファイル
    include_package_data=True,
    zip_safe=False,
)
