English / [**日本語**](README_JP.md)

# Display Layout Manager

[![Build](https://github.com/eijikominami/display-layout-manager/actions/workflows/test.yml/badge.svg)](https://github.com/eijikominami/display-layout-manager/actions/workflows/test.yml)
[![Release](https://github.com/eijikominami/display-layout-manager/actions/workflows/release.yml/badge.svg)](https://github.com/eijikominami/display-layout-manager/actions/workflows/release.yml)
[![Release Version](https://img.shields.io/github/v/release/eijikominami/display-layout-manager)](https://github.com/eijikominami/display-layout-manager/releases)
[![codecov](https://codecov.io/gh/eijikominami/display-layout-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/eijikominami/display-layout-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

Automatic display layout configuration tool for macOS

## Overview

Display Layout Manager is a command-line tool for automatically managing multiple display configurations on macOS. It automatically applies predefined layout settings based on different display combinations.

## Key Features

- **Automatic Display Detection**: Automatically detects Persistent Screen IDs of currently connected displays
- **Pattern Matching**: Automatically selects optimal layout patterns based on display configuration
- **Configuration File Management**: Manages multiple layout patterns with JSON format configuration files
- **Current Layout Saving**: Easily save current display configuration with `--save-current`
- **Dependency Management**: Automatic installation and verification of required tools
- **Comprehensive Logging**: Structured log output and session summaries
- **Menu Bar App**: Easy-to-use GUI accessible from macOS menu bar
- **Error Handling**: User-friendly error messages and troubleshooting guides
- **Integration Testing**: Quality assurance through comprehensive test suites

## System Requirements

- **OS**: macOS 10.14 (Mojave) or later
- **Python**: 3.8 or later
- **Dependencies**: Homebrew, displayplacer, GNU grep (automatic installation supported)

## Language Support

Display Layout Manager supports **English** and **Japanese** interfaces.

### Automatic Language Detection

The application automatically detects your system locale and displays messages in the appropriate language:
- **Japanese locale** (ja, ja_JP, etc.): All CLI and menu bar messages in Japanese
- **Other locales**: All CLI and menu bar messages in English

### Manual Language Override

You can override the automatic language detection using the `DISPLAY_LAYOUT_LANG` environment variable:

```bash
# Force English interface
export DISPLAY_LAYOUT_LANG=en
display-layout-manager

# Force Japanese interface
export DISPLAY_LAYOUT_LANG=ja
display-layout-manager

# One-time override
DISPLAY_LAYOUT_LANG=en display-layout-manager --show-displays
```

### Log Files

**Note**: Log files are always written in English (technical records), regardless of the interface language. This ensures consistency for debugging and troubleshooting.

- **CLI/Menu Bar Output**: Internationalized (English/Japanese)
- **Log Files**: Always English (`~/Library/Logs/DisplayLayoutManager/`)

## Installation

### Using Homebrew (Recommended)

```bash
# Add Homebrew tap
brew tap eijikominami/display-layout-manager

# Install Display Layout Manager
brew install display-layout-manager
```

### Using pip

```bash
# Install from PyPI
pip install display-layout-manager

# Or install directly from GitHub
pip install git+https://github.com/eijikominami/display-layout-manager.git
```

### Install from Source

```bash
# Clone repository
git clone https://github.com/eijikominami/display-layout-manager.git
cd display-layout-manager

# Install in development mode
pip install -e .
```

## Usage

### Menu Bar Application (Recommended)

A GUI application that can be easily operated from the macOS menu bar.

```bash
# Launch menu bar app
display-layout-menubar

# Launch in background
display-layout-menubar &

# Enable auto-launch at login
display-layout-menubar --enable-auto-launch

# Disable auto-launch at login
display-layout-menubar --disable-auto-launch
```

#### Menu Bar App Features

A ⧈ icon appears in the menu bar, providing the following features:

- **Apply Layout**: Apply layout matching current display configuration with one click
- **Save Current Settings**: Save current display configuration to config file
- **✓ Launch at Login**: Toggle auto-launch on/off (checkmark shows current state)
- **Quit**: Exit menu bar app

Operation results are recorded in log files (`~/Library/Logs/DisplayLayoutManager/`).

### CLI Commands

```bash
# Basic execution (automatically apply display layout)
display-layout-manager

# Show current display configuration
display-layout-manager --show-displays

# Validate configuration file
display-layout-manager --validate-config

# Dry run (don't actually execute commands)
display-layout-manager --dry-run

# Execute with verbose logging
display-layout-manager --verbose

# Run integration tests
display-layout-manager --run-tests

# Save current layout
display-layout-manager --save-current

# Show help
display-layout-manager --help
```

### Configuration File

Configuration files are automatically created in the following locations:
- **Default**: `~/Library/Application Support/DisplayLayoutManager/config.json`
- **Environment Variable**: Can be specified with `DISPLAY_LAYOUT_CONFIG`
- **Command Line**: Can be specified with `--config` option

#### Configuration File Example

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Laptop Only",
      "description": "Laptop only usage",
      "screen_ids": [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230"
      ],
      "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\""
    },
    {
      "name": "Home Office Setup",
      "description": "Main display + 2 external monitors",
      "screen_ids": [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230",
        "3F816611-C361-483F-8FB3-CE03208D949C",
        "AE0F5F39-5D5C-4FF1-A7BA-8E5CBE679211"
      ],
      "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\" \"id:3F816611-C361-483F-8FB3-CE03208D949C res:1920x1080 hz:120 color_depth:4 enabled:true scaling:off origin:(-1278,-1080) degree:0\" \"id:AE0F5F39-5D5C-4FF1-A7BA-8E5CBE679211 res:1920x1080 hz:120 color_depth:4 enabled:true scaling:off origin:(642,-1080) degree:0\""
    }
  ]
}
```

### Setup Steps

1. **Check current display configuration**
   ```bash
   display-layout-manager --show-displays
   ```

2. **Edit configuration file**
   - Create patterns using the output Screen IDs
   - Get current command with `displayplacer list` command

3. **Validate configuration file**
   ```bash
   display-layout-manager --validate-config
   ```

4. **Test with dry run**
   ```bash
   display-layout-manager --dry-run --verbose
   ```

### Auto-Save Current Layout

If you want to avoid manual configuration file editing, you can automatically save the current display layout:

```bash
# Save current display layout
display-layout-manager --save-current

# Example output:
# Saving current display configuration...
# Detected displays: 3
# ✓ Created pattern '3_Displays_37D8832A_3F816611_AE0F5F39'
```

Features:
- **Automatic Pattern Name Generation**: Generates unique names from Screen IDs
- **Automatic Overwrite**: Automatically updates if same display configuration already exists
- **Current Settings Extraction**: Automatically extracts current settings command from displayplacer

## Logging and Debugging

### Log Files

- **Location**: `~/Library/Logs/DisplayLayoutManager/`
- **Format**: JSON structured logs
- **File Types**:
  - `display_layout_manager_YYYYMMDD.log` - Normal execution logs (daily rotation)

### Debug Options

```bash
# Show verbose logs
display-layout-manager --verbose

# Run integration tests
display-layout-manager --run-tests --verbose

# Validate configuration file
display-layout-manager --validate-config --verbose
```

## Troubleshooting

### Dependency Issues

**Homebrew not found**
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Restart shell or set PATH
eval "$(/opt/homebrew/bin/brew shellenv)"  # Apple Silicon Mac
eval "$(/usr/local/bin/brew shellenv)"     # Intel Mac
```

**displayplacer not found**
```bash
# Install displayplacer
brew install jakehilborn/jakehilborn/displayplacer

# Or download manually
# https://github.com/jakehilborn/displayplacer/releases
```

**GNU grep not found**
```bash
# Install GNU grep
brew install grep

# Set PATH (if needed)
export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"  # Apple Silicon Mac
export PATH="/usr/local/opt/grep/libexec/gnubin:$PATH"     # Intel Mac
```

### Configuration File Issues

**JSON syntax error**
- Use online JSON validator
- Check commas, brackets, and quotes
- Use `--validate-config` option for detailed check

**Pattern doesn't match**
```bash
# Check current Screen IDs
display-layout-manager --show-displays

# Update screen_ids in configuration file
# Exact match required (order doesn't matter)
```

### Command Execution Issues

**displayplacer command fails**
- Check if Screen ID is correct
- Check if resolution and refresh rate are supported
- Pre-check command with `--dry-run` option

## Development & Contributing

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/eijikominami/display-layout-manager.git
cd display-layout-manager

# Install in development mode
pip install -e .

# Run integration tests
python -m src.display_layout_manager.main --run-tests
```

### Development Setup

1. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

   This will automatically run the following checks before each commit:
   - **Black**: Code formatting
   - **isort**: Import statement organization
   - **flake8**: Linting
   - **Trailing whitespace removal**
   - **End-of-file fixer**
   - **YAML validation**

3. **Manual pre-commit run** (optional)
   ```bash
   # Run on all files
   pre-commit run --all-files

   # Run specific hook
   pre-commit run black --all-files
   ```

### Testing

```bash
# Run all test suites (recommended)
python3 tests/run_all_tests.py

# Measure test coverage
python3 tests/run_coverage.py
# HTML report: htmlcov/index.html

# CLI component unit tests
python3 tests/test_cli_components.py      # ConfigManager, PatternMatcher, CLIBridge
python3 tests/test_dependency_manager.py  # DependencyManager
python3 tests/test_display_manager.py     # DisplayManager
python3 tests/test_command_executor.py    # CommandExecutor
python3 tests/test_layout_saver.py        # LayoutSaver

# Menu bar app tests
python3 tests/test_menubar_checkbox.py    # AutoLaunchManager
python3 tests/test_menubar_logic.py       # Menu bar logic
python3 tests/test_menubar_integration.py # Menu bar integration tests

# CLI integration tests
display-layout-manager --run-tests --verbose

# Manual tests
display-layout-manager --dry-run --verbose
display-layout-manager --show-displays
display-layout-manager --validate-config
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing & Support

- **Bug Reports**: [GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/eijikominami/display-layout-manager/issues)
- **Documentation**: [GitHub Wiki](https://github.com/eijikominami/display-layout-manager/wiki)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## Related Projects

- [displayplacer](https://github.com/jakehilborn/displayplacer) - macOS display configuration tool
- [Homebrew](https://brew.sh/) - macOS package manager
