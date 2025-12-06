#!/usr/bin/env python3
"""
Display Layout Manager セットアップスクリプト
"""

from setuptools import setup, find_packages
from pathlib import Path

# バージョン情報を読み込み
version_file = Path(__file__).parent / "src" / "display_layout_manager" / "__init__.py"
version = {}
with open(version_file, encoding='utf-8') as f:
    exec(f.read(), version)

# README.mdを読み込み
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, encoding='utf-8') as f:
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
        "pyobjc-framework-Cocoa>=10.0",  # macOS 通知システム統合用
    ],
    
    # エントリーポイント
    entry_points={
        "console_scripts": [
            "display-layout-manager=display_layout_manager.main:main",
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