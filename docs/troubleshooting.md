English / [**日本語**](troubleshooting_jp.md)

# Troubleshooting Guide

## Overview

This guide explains potential issues that may occur while using Display Layout Manager and their solutions.

## Table of Contents

- [Dependency Issues](#dependency-issues)
- [Configuration File Issues](#configuration-file-issues)
- [Display Detection Issues](#display-detection-issues)
- [Pattern Matching Issues](#pattern-matching-issues)
- [Command Execution Issues](#command-execution-issues)
- [Menu Bar App Issues](#menu-bar-app-issues)
- [Homebrew Installation Issues](#homebrew-installation-issues)
- [Logging and Debugging](#logging-and-debugging)

## Dependency Issues

### Homebrew Not Found

**Symptoms:**
```
Error: Homebrew not found
```

**Causes:**
- Homebrew not installed
- PATH not configured correctly

**Solutions:**

1. **Install Homebrew**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Configure PATH**

   For Apple Silicon Mac:
   ```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
   source ~/.zshrc
   ```

   For Intel Mac:
   ```bash
   echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify**
   ```bash
   brew --version
   ```

### displayplacer Not Found

**Symptoms:**
```
Error: displayplacer not found
```

**Causes:**
- displayplacer not installed
- Auto-installation failed

**Solutions:**

1. **Install manually**
   ```bash
   brew install jakehilborn/jakehilborn/displayplacer
   ```

2. **Verify**
   ```bash
   displayplacer --version
   ```

3. **If still not working**
   - Download directly from GitHub: https://github.com/jakehilborn/displayplacer/releases
   - Place binary in `/usr/local/bin/`
   - Grant execute permission: `chmod +x /usr/local/bin/displayplacer`

### GNU grep Not Found

**Symptoms:**
```
Error: GNU grep not found
```

**Causes:**
- GNU grep not installed
- Using macOS default grep

**Solutions:**

1. **Install GNU grep**
   ```bash
   brew install grep
   ```

2. **Configure PATH (optional)**

   For Apple Silicon Mac:
   ```bash
   echo 'export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

   For Intel Mac:
   ```bash
   echo 'export PATH="/usr/local/opt/grep/libexec/gnubin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify**
   ```bash
   grep --version | head -1
   # Confirm GNU grep is displayed
   ```

## Configuration File Issues

### JSON Syntax Error

**Symptoms:**
```
Error: Configuration file syntax error
Details: Expecting ',' delimiter: line 5 column 3 (char 123)
```

**Causes:**
- Invalid JSON syntax
- Incorrect commas, brackets, or quotes

**Solutions:**

1. **Use online JSON validator**
   - https://jsonlint.com/
   - Paste configuration file content for validation

2. **Common syntax errors**

   **Trailing comma**
   ```json
   // ❌ Bad
   {
     "patterns": [
       {
         "name": "Pattern 1",
       }
     ]
   }

   // ✅ Good
   {
     "patterns": [
       {
         "name": "Pattern 1"
       }
     ]
   }
   ```

3. **Validate configuration file**
   ```bash
   display-layout-manager --validate-config --verbose
   ```

### Missing Required Fields

**Symptoms:**
```
Error: Configuration file validation error
Details: Pattern 'Home Office Setup' missing required field 'command'
```

**Causes:**
- Pattern missing required fields

**Solutions:**

1. **Check required fields**
   - `version`: Configuration file version
   - `patterns`: Pattern array
   - Each pattern:
     - `name`: Pattern name
     - `screen_ids`: Screen ID array
     - `command`: displayplacer command

2. **Add missing fields**
   ```json
   {
     "version": "1.0",
     "patterns": [
       {
         "name": "Pattern Name",
         "description": "Optional description",
         "screen_ids": ["SCREEN_ID_1", "SCREEN_ID_2"],
         "command": "displayplacer ..."
       }
     ]
   }
   ```

3. **Validate configuration file**
   ```bash
   display-layout-manager --validate-config
   ```

## Display Detection Issues

### Cannot Get Screen IDs

**Symptoms:**
```
Error: Display detection failed
```

**Causes:**
- displayplacer command failed
- Display not connected properly

**Solutions:**

1. **Run displayplacer directly**
   ```bash
   displayplacer list
   ```

   If error appears, it's a displayplacer issue.

2. **Check display connection**
   - Cable connected properly
   - Display powered on
   - Recognized in System Preferences > Displays

3. **Check with verbose logs**
   ```bash
   display-layout-manager --show-displays --verbose
   ```

## Pattern Matching Issues

### Pattern Doesn't Match

**Symptoms:**
```
Warning: No matching pattern found
Current Screen IDs: [ID1, ID2]
```

**Causes:**
- Screen IDs in config file don't match current Screen IDs
- Screen ID order different (order shouldn't matter, but check anyway)

**Solutions:**

1. **Check current Screen IDs**
   ```bash
   display-layout-manager --show-displays
   ```

2. **Update Screen IDs in config file**
   ```bash
   open ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```

   Modify to exactly match current Screen IDs

3. **Use auto-save**
   ```bash
   display-layout-manager --save-current
   ```

   This automatically saves current configuration.

4. **Verify with dry run**
   ```bash
   display-layout-manager --dry-run --verbose
   ```

## Command Execution Issues

### displayplacer Command Fails

**Symptoms:**
```
Error: Command execution failed
Exit code: 1
```

**Causes:**
- Invalid Screen ID
- Unsupported resolution or refresh rate
- Display not connected

**Solutions:**

1. **Check with dry run**
   ```bash
   display-layout-manager --dry-run --verbose
   ```

   Check command to be executed

2. **Run displayplacer directly**
   ```bash
   # Copy and run command shown in dry run
   displayplacer "id:SCREEN_ID res:1920x1080 ..."
   ```

   Check error message

3. **Check supported resolutions**
   ```bash
   displayplacer list
   ```

   Check supported resolutions in "Resolutions for rotation 0:" section

4. **Update configuration file**
   - Change to supported resolution/refresh rate
   - Or save current settings with `--save-current`

## Menu Bar App Issues

### Menu Bar Icon Not Displayed

**Symptoms:**
- Icon not displayed after running `display-layout-menubar`

**Causes:**
- App not starting correctly
- rumps dependency issue

**Solutions:**

1. **Launch from terminal and check**
   ```bash
   display-layout-menubar
   ```

   Check error messages

2. **Check dependencies**
   ```bash
   pip show rumps pyobjc-framework-Cocoa
   ```

3. **Reinstall**
   ```bash
   brew uninstall display-layout-manager
   brew install display-layout-manager
   ```

### "Apply Layout" Not Working

**Symptoms:**
- Nothing happens when clicking menu item

**Causes:**
- No matching pattern
- displayplacer command failed

**Solutions:**

1. **Check log files**
   ```bash
   tail -f ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log
   ```

   Click menu item and check logs

2. **Verify with CLI**
   ```bash
   display-layout-manager --verbose
   ```

   Check if CLI works normally

3. **Check configuration file**
   - Matching pattern exists
   - Screen IDs are correct

## Homebrew Installation Issues

### Formula Not Found

**Symptoms:**
```
Error: No available formula with the name "display-layout-manager"
```

**Causes:**
- Tap not added

**Solutions:**

1. **Add tap**
   ```bash
   brew tap eijikominami/display-layout-manager
   ```

2. **Install**
   ```bash
   brew install display-layout-manager
   ```

### Installation Fails

**Symptoms:**
```
Error: An exception occurred within a child process:
  ...
```

**Causes:**
- Dependency issues
- Network issues

**Solutions:**

1. **Update Homebrew**
   ```bash
   brew update
   ```

2. **Clear cache**
   ```bash
   brew cleanup
   ```

3. **Retry**
   ```bash
   brew install display-layout-manager
   ```

4. **Check with verbose logs**
   ```bash
   brew install display-layout-manager --verbose --debug
   ```

## Logging and Debugging

### Log File Location

```
~/Library/Logs/DisplayLayoutManager/display_layout_manager_YYYYMMDD.log
```

### Checking Log Files

```bash
# Show latest logs
tail -f ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log

# Show logs for specific date
cat ~/Library/Logs/DisplayLayoutManager/display_layout_manager_20231215.log

# Show errors only
grep ERROR ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log
```

### Enable Verbose Logging

```bash
# Enable verbose logging in CLI
display-layout-manager --verbose

# Verbose logging for all options
display-layout-manager --show-displays --verbose
display-layout-manager --validate-config --verbose
display-layout-manager --dry-run --verbose
```

### Collecting Debug Information

When reporting issues, include the following information:

1. **Version information**
   ```bash
   display-layout-manager --version
   displayplacer --version
   sw_vers
   ```

2. **Display information**
   ```bash
   display-layout-manager --show-displays
   displayplacer list
   ```

3. **Configuration file**
   ```bash
   cat ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```

4. **Log files**
   ```bash
   cat ~/Library/Logs/DisplayLayoutManager/display_layout_manager_*.log
   ```

5. **Error messages**
   - Copy complete error messages

## Frequently Asked Questions (FAQ)

### Q: Will layouts be applied automatically when connecting/disconnecting displays?

A: In the current version, you need to manually run `display-layout-manager` or click "Apply Layout" from the menu bar app. Automatic detection feature is planned for future versions.

### Q: Can I switch between multiple configuration files?

A: Yes, you can specify configuration files with the `--config` option:
```bash
display-layout-manager --config ~/my-config.json
```

### Q: Can I change pattern names?

A: Yes, you can edit the configuration file directly to change pattern names. However, patterns saved with `--save-current` will have auto-generated names.

### Q: Can I change resolution or refresh rate?

A: Yes, you can edit the `command` field in the configuration file. Check supported resolutions with `displayplacer list`.

### Q: Is it safe to delete log files?

A: Yes, log files are automatically recreated. You can periodically delete old log files without issues.

## Support

If issues persist, you can get support through:

- **GitHub Issues**: https://github.com/eijikominami/display-layout-manager/issues
- **GitHub Discussions**: https://github.com/eijikominami/display-layout-manager/discussions

Bug reports and feature requests are accepted on GitHub Issues.

## Related Documents

- [README.md](../README.md) - Basic usage
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture
- [Configuration File Specification](configuration.md) - Configuration details
