#!/usr/bin/env python3
"""
メニューバーアプリのテストスクリプト（修正版）
"""
import sys
sys.path.insert(0, '/Users/eiji/Documents/VisualStudioCode/display-layout-manager/src')

from display_layout_manager.menubar_app import DisplayLayoutMenuBar

if __name__ == '__main__':
    app = DisplayLayoutMenuBar()
    app.run()
