English / [**日本語**](api-specification_jp.md)

# API Specification

## CLI Commands

### display-layout-manager

Main command for automatic display layout configuration.

#### Synopsis

```bash
display-layout-manager [OPTIONS]
```

#### Options

| Option | Type | Description |
|--------|------|-------------|
| `--version` | flag | Show version and exit |
| `--config PATH` | path | Configuration file path (default: `~/Library/Application Support/DisplayLayoutManager/config.json`) |
| `--verbose`, `-v` | flag | Enable verbose logging |
| `--dry-run` | flag | Dry run mode (don't execute commands) |
| `--show-displays` | flag | Show current display configuration and exit |
| `--validate-config` | flag | Validate configuration file only |
| `--run-tests` | flag | Run integration tests |
| `--save-current` | flag | Save current display layout as pattern |

#### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error or user interruption |
| 2 | Configuration file error |
| 3 | Display detection error |
| 4 | Pattern matching error |
| 5 | Command execution error |
| 6 | Dependency error |

#### Examples

```bash
# Basic execution
display-layout-manager

# Show current displays
display-layout-manager --show-displays

# Validate configuration
display-layout-manager --validate-config

# Dry run with verbose output
display-layout-manager --dry-run --verbose

# Save current layout
display-layout-manager --save-current

# Run integration tests
display-layout-manager --run-tests --verbose
```

### display-layout-menubar

Menu bar application for GUI-based display layout management.

#### Synopsis

```bash
display-layout-menubar [OPTIONS]
```

#### Options

| Option | Type | Description |
|--------|------|-------------|
| `--enable-auto-launch` | flag | Enable auto-launch at login |
| `--disable-auto-launch` | flag | Disable auto-launch at login |

#### Menu Items

| Item | Action |
|------|--------|
| Apply Layout | Apply layout matching current display configuration |
| Save Current Settings | Save current display configuration to config file |
| ✓ Launch at Login | Toggle auto-launch on/off (checkmark shows current state) |
| Quit | Exit menu bar app |

#### Examples

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

## Configuration File Format

### File Location

Configuration files are loaded in the following priority order:

1. Command-line argument (`--config`)
2. Environment variable (`DISPLAY_LAYOUT_CONFIG`)
3. Default location (`~/Library/Application Support/DisplayLayoutManager/config.json`)

### JSON Schema

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "string (required)",
      "description": "string (optional)",
      "screen_ids": ["string (required, at least 1)"],
      "command": "string (required, must start with 'displayplacer')"
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Configuration file format version |
| `patterns` | array | Yes | Array of layout patterns (at least 1 required) |
| `patterns[].name` | string | Yes | Pattern name (unique identifier) |
| `patterns[].description` | string | No | Pattern description |
| `patterns[].screen_ids` | array | Yes | Array of Persistent Screen IDs (at least 1 required) |
| `patterns[].command` | string | Yes | displayplacer command to execute |

### Validation Rules

1. **version**: Must be a non-empty string
2. **patterns**: Must be a non-empty array
3. **patterns[].name**: Must be a non-empty string
4. **patterns[].screen_ids**: Must be a non-empty array of strings
5. **patterns[].command**: Must start with "displayplacer"

### Example Configuration

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

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DISPLAY_LAYOUT_CONFIG` | Configuration file path | `~/Library/Application Support/DisplayLayoutManager/config.json` |
| `DISPLAY_LAYOUT_LANG` | Interface language (`en` or `ja`) | Auto-detected from system locale |

## Output Format

### Standard Output

#### Success Case

```
Display Layout Manager v1.5.0 started
==================================================
Configuration file: /Users/username/Library/Application Support/DisplayLayoutManager/config.json
✓ Configuration loaded: 2 patterns

==================================================
Checking current display configuration...
✓ Displays detected: 3

==================================================
Pattern matching...
Pattern match result:
✓ Pattern matched: Home Office Setup
Match type: exact
Confidence: 100%

==================================================
Executing command...
✓ Command executed successfully

==================================================
Display Layout Manager completed successfully
```

#### Error Case

```
Display Layout Manager v1.5.0 started
==================================================
Configuration file: /Users/username/Library/Application Support/DisplayLayoutManager/config.json
✗ Configuration invalid
  - JSON syntax error: Expecting ',' delimiter (line 5, column 3)

Error: CONFIG_SYNTAX_ERROR
Configuration file has JSON syntax errors

Troubleshooting:
1. Use online JSON validator to check syntax
2. Check for missing commas, brackets, or quotes
3. Use --validate-config option for detailed validation
```

### Log Files

Log files are written to `~/Library/Logs/DisplayLayoutManager/` in JSON format.

#### Log Entry Format

```json
{
  "timestamp": "2025-12-07T10:30:45.123456",
  "level": "INFO",
  "component": "display",
  "message": "Display detection started",
  "data": {}
}
```

#### Log Levels

| Level | Description |
|-------|-------------|
| `DEBUG` | Detailed debugging information |
| `INFO` | General informational messages |
| `WARNING` | Warning messages |
| `ERROR` | Error messages |
| `SUCCESS` | Success messages |

## Internationalization

### Language Detection

The application automatically detects the system locale and displays messages in the appropriate language:

- **Japanese locale** (`ja`, `ja_JP`, etc.): All CLI and menu bar messages in Japanese
- **Other locales**: All CLI and menu bar messages in English

### Language Override

Use the `DISPLAY_LAYOUT_LANG` environment variable to override automatic detection:

```bash
# Force English
export DISPLAY_LAYOUT_LANG=en
display-layout-manager

# Force Japanese
export DISPLAY_LAYOUT_LANG=ja
display-layout-manager
```

### Log File Language

Log files are always written in English (technical records), regardless of the interface language.

## Error Handling

### Error Categories

| Category | Exit Code | Description |
|----------|-----------|-------------|
| Configuration Error | 2 | Configuration file issues |
| Display Detection Error | 3 | Display detection failures |
| Pattern Match Error | 4 | Pattern matching failures |
| Command Execution Error | 5 | displayplacer command failures |
| Dependency Error | 6 | Missing dependencies |

### Error Response Format

All errors include:
- Error code
- User-friendly error message
- Troubleshooting steps
- Related log file location

## Integration with External Tools

### displayplacer

Display Layout Manager uses [displayplacer](https://github.com/jakehilborn/displayplacer) for display configuration.

#### Required Commands

- `displayplacer list`: Get current display configuration
- `displayplacer <config>`: Apply display configuration

### Homebrew

Used for dependency installation:
- `brew --version`: Check Homebrew availability
- `brew install <package>`: Install dependencies

### GNU grep

Used for text processing:
- `grep --version`: Check GNU grep availability
