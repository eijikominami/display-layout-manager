#!/bin/bash
# Release script for Display Layout Manager
# Usage: ./scripts/release.sh 1.0.1

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.1"
    exit 1
fi

echo "🚀 Preparing release v$VERSION"

# Update version in __init__.py
echo "📝 Updating version in __init__.py..."
sed -i '' "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" src/display_layout_manager/__init__.py

# Update CHANGELOG.md
echo "📝 Please update CHANGELOG.md with changes for v$VERSION"
echo "Press Enter when ready to continue..."
read

# Commit version changes
echo "💾 Committing version changes..."
git add src/display_layout_manager/__init__.py CHANGELOG.md
git commit -m "Bump version to v$VERSION"

# Create and push tag
echo "🏷️  Creating and pushing tag v$VERSION..."
git tag "v$VERSION"
git push origin main
git push origin "v$VERSION"

echo "✅ Release v$VERSION initiated!"
echo "🔄 GitHub Actions will now:"
echo "   1. Run tests on macOS"
echo "   2. Create GitHub Release"
echo "   3. Update Homebrew Formula"
echo "   4. Update Homebrew Tap"
echo ""
echo "📊 Monitor progress at: https://github.com/eijikominami/display-layout-manager/actions"