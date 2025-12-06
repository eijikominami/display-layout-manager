English / [**日本語**](configuration_jp.md)

# Configuration File Specification

## Overview

Display Layout Manager uses JSON format configuration files to manage display layout patterns. This document explains the detailed specification of configuration files and advanced configuration examples.

## Configuration File Location

### Default Location

```
~/Library/Application Support/DisplayLayoutManager/config.json
```

### Priority Order

Configuration files are searched in the following priority order (highest first):

1. **Command-line argument**: `--config /path/to/config.json`
2. **Environment variable**: `DISPLAY_LAYOUT_CONFIG=/path/to/config.json`
3. **macOS default**: `~/Library/Application Support/DisplayLayoutManager/config.json`

### Configuration Examples

```bash
# Specify with command-line argument
display-layout-manager --config ~/my-custom-config.json

# Specify with environment variable
export DISPLAY_LAYOUT_CONFIG=~/my-custom-config.json
display-layout-manager
```

## Configuration File Structure

### Basic Structure

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Pattern Name",
      "description": "Pattern description",
      "screen_ids": ["Screen ID 1", "Screen ID 2"],
      "command": "displayplacer command"
    }
  ]
}
```

### Field Details

#### version (Required)

- **Type**: String
- **Description**: Configuration file version
- **Current Version**: `"1.0"`
- **Purpose**: Future compatibility management

```json
{
  "version": "1.0"
}
```

#### patterns (Required)

- **Type**: Array
- **Description**: List of display layout patterns
- **Minimum Elements**: 0 (empty array is valid)
- **Maximum Elements**: No limit

```json
{
  "patterns": []
}
```

### Pattern Object

#### name (Required)

- **Type**: String
- **Description**: Unique pattern name
- **Constraints**: 
  - Cannot be empty string
  - Duplicate names not recommended (last one takes precedence)
- **Recommendation**: Use descriptive names

```json
{
  "name": "Home Office Setup"
}
```

#### description (Optional)

- **Type**: String
- **Description**: Detailed pattern description
- **Purpose**: Log output, user information
- **Recommendation**: Clearly describe pattern purpose

```json
{
  "description": "Main display + 2 external monitors"
}
```

#### screen_ids (Required)

- **Type**: Array of strings
- **Description**: List of Persistent Screen IDs
- **Constraints**:
  - Cannot be empty array
  - Each element cannot be empty string
  - Order doesn't matter (compared as set)
- **How to Get**: `displayplacer list` or `display-layout-manager --show-displays`

```json
{
  "screen_ids": [
    "37D8832A-2D66-02CA-B9F7-8F30A301B230",
    "3F816611-C361-483F-8FB3-CE03208D949C"
  ]
}
```

#### command (Required)

- **Type**: String
- **Description**: displayplacer command to apply
- **Constraints**:
  - Cannot be empty string
  - Must start with "displayplacer"
- **How to Get**: Line after "Execute the command below" from `displayplacer list` output

```json
{
  "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\""
}
```

## Complete Configuration Examples

### Single Display

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
    }
  ]
}
```

### Dual Display

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Dual Monitor Setup",
      "description": "Laptop + 1 external monitor",
      "screen_ids": [
        "37D8832A-2D66-02CA-B9F7-8F30A301B230",
        "3F816611-C361-483F-8FB3-CE03208D949C"
      ],
      "command": "displayplacer \"id:37D8832A-2D66-02CA-B9F7-8F30A301B230 res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0\" \"id:3F816611-C361-483F-8FB3-CE03208D949C res:1920x1080 hz:120 color_depth:4 enabled:true scaling:off origin:(1470,0) degree:0\""
    }
  ]
}
```

### Triple Display

```json
{
  "version": "1.0",
  "patterns": [
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

## How to Create Configuration Files

### Method 1: Auto-Save (Recommended)

Automatically save current display configuration:

```bash
# Save current layout
display-layout-manager --save-current
```

Advantages of this method:
- No manual Screen ID input required
- Automatic displayplacer command extraction
- Automatic pattern name generation
- Automatic overwrite of existing patterns

### Method 2: Manual Creation

1. **Check Screen IDs**
   ```bash
   display-layout-manager --show-displays
   ```

2. **Get displayplacer command**
   ```bash
   displayplacer list
   ```
   
   Copy the line after "Execute the command below"

3. **Edit configuration file**
   ```bash
   open ~/Library/Application\ Support/DisplayLayoutManager/config.json
   ```

4. **Add pattern**
   - `name`: Descriptive name
   - `description`: Pattern description
   - `screen_ids`: Screen IDs from step 1
   - `command`: Command from step 2

5. **Validate configuration file**
   ```bash
   display-layout-manager --validate-config
   ```

## Configuration File Validation

### Validation Commands

```bash
# Validate configuration file
display-layout-manager --validate-config

# Show detailed validation results
display-layout-manager --validate-config --verbose
```

### Validation Items

1. **JSON Syntax**: Valid JSON format
2. **Required Fields**: `version`, `patterns` exist
3. **Pattern Structure**: Each pattern has required fields
4. **screen_ids**: Non-empty string array
5. **command**: Starts with "displayplacer"

## Advanced Configuration

### Using Environment Variables

```bash
# Development environment configuration
export DISPLAY_LAYOUT_CONFIG=~/dev-config.json

# Production environment configuration
export DISPLAY_LAYOUT_CONFIG=~/prod-config.json
```

### Managing Multiple Configuration Files

```bash
# Configuration file directory structure
~/display-configs/
├── home.json          # Home
├── office.json        # Office
└── presentation.json  # Presentation

# Usage examples
display-layout-manager --config ~/display-configs/home.json
display-layout-manager --config ~/display-configs/office.json
```

## File Permissions and Security

### Recommended Permissions

```bash
# Configuration directory
chmod 700 ~/Library/Application\ Support/DisplayLayoutManager/

# Configuration file
chmod 600 ~/Library/Application\ Support/DisplayLayoutManager/config.json
```

### Security Considerations

- Don't include sensitive information in configuration files
- Prevent access from other users
- Protect backup files with same permissions

## Troubleshooting

For configuration file issues, see [Troubleshooting Guide](troubleshooting.md).

## Related Documents

- [README.md](../README.md) - Basic usage
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture
- [Troubleshooting Guide](troubleshooting.md) - Problem solving
