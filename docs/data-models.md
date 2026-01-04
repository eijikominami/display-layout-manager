English / [**日本語**](data-models_jp.md)

# Data Models

## Overview

Display Layout Manager uses dataclasses to represent configuration data and display information. This document describes the data structures, conversion logic, and validation rules.

## Core Data Models

### ConfigPattern

Represents a single display layout pattern.

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | str | Yes | Pattern name (unique identifier) |
| `description` | str | No | Pattern description (default: empty string) |
| `screen_ids` | List[str] | Yes | List of Persistent Screen IDs |
| `command` | str | Yes | displayplacer command to execute |

#### Validation Rules

- `name`: Must be non-empty string
- `screen_ids`: Must be non-empty list of strings
- `command`: Must be non-empty string starting with "displayplacer"

#### Python Definition

```python
@dataclass
class ConfigPattern:
    """設定パターンクラス"""
    name: str
    description: str
    screen_ids: List[str]
    command: str

    def __post_init__(self):
        """初期化後の検証"""
        if not self.name:
            raise ValueError("パターン名は必須です")
        if not self.screen_ids:
            raise ValueError("screen_ids は必須です")
        if not self.command:
            raise ValueError("command は必須です")
        if not self.command.strip().startswith("displayplacer"):
            raise ValueError("command は 'displayplacer' で開始する必要があります")
```

#### JSON Representation

```json
{
  "name": "Home Office Setup",
  "description": "Main display + 2 external monitors",
  "screen_ids": [
    "37D8832A-2D66-02CA-B9F7-8F30A301B230",
    "3F816611-C361-483F-8FB3-CE03208D949C"
  ],
  "command": "displayplacer \"id:37D8832A...\""
}
```

### Configuration

Represents the entire configuration file structure.

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | str | Yes | Configuration file format version |
| `patterns` | List[ConfigPattern] | Yes | List of layout patterns (at least 1 required) |

#### Validation Rules

- `version`: Must be non-empty string
- `patterns`: Must be non-empty list of ConfigPattern objects

#### Python Definition

```python
@dataclass
class Configuration:
    """設定ファイル全体の構造"""
    version: str
    patterns: List[ConfigPattern]

    def __post_init__(self):
        """初期化後の検証"""
        if not self.version:
            raise ValueError("version は必須です")
        if not self.patterns:
            raise ValueError("patterns は必須です")
```

#### JSON Representation

```json
{
  "version": "1.0",
  "patterns": [
    {
      "name": "Pattern 1",
      "description": "Description",
      "screen_ids": ["ID1", "ID2"],
      "command": "displayplacer ..."
    }
  ]
}
```

### DisplayConfiguration

Represents current display configuration detected from the system.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `screen_ids` | List[str] | List of detected Persistent Screen IDs |
| `raw_output` | str | Raw output from displayplacer command |

#### Python Definition

```python
@dataclass
class DisplayConfiguration:
    """現在のディスプレイ構成"""
    screen_ids: List[str]
    raw_output: str
```

### MatchResult

Represents the result of pattern matching operation.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `matched` | bool | Whether a pattern was matched |
| `pattern` | Optional[ConfigPattern] | Matched pattern (None if no match) |
| `match_type` | str | Type of match ("exact", "partial", or "none") |
| `confidence` | int | Confidence score (0-100) |
| `details` | str | Detailed matching information |

#### Python Definition

```python
@dataclass
class MatchResult:
    """パターンマッチング結果"""
    matched: bool
    pattern: Optional[ConfigPattern]
    match_type: str
    confidence: int
    details: str
```

### ExecutionResult

Represents the result of command execution.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether command executed successfully |
| `pattern_name` | str | Name of executed pattern |
| `command` | str | Executed command |
| `return_code` | int | Command return code |
| `stdout` | str | Standard output |
| `stderr` | str | Standard error |
| `dry_run` | bool | Whether this was a dry run |

#### Python Definition

```python
@dataclass
class ExecutionResult:
    """コマンド実行結果"""
    success: bool
    pattern_name: str
    command: str
    return_code: int
    stdout: str
    stderr: str
    dry_run: bool

    def get_summary(self) -> str:
        """実行結果のサマリーを取得"""
        # Implementation details...
```

## Data Conversion

### JSON to Python Objects

Configuration files are converted from JSON to Python dataclasses using the following process:

1. **JSON Parsing**: Load JSON file using `json.load()`
2. **Structure Validation**: Validate required fields and types
3. **Object Creation**: Create ConfigPattern objects from JSON data
4. **Configuration Assembly**: Create Configuration object with patterns

#### Conversion Flow

```
JSON File
  ↓ json.load()
Dict[str, Any]
  ↓ validate_config_structure()
Validated Dict
  ↓ ConfigPattern() for each pattern
List[ConfigPattern]
  ↓ Configuration()
Configuration Object
```

#### Implementation

```python
def load_config(self, config_path: Path) -> Tuple[bool, Optional[Configuration], List[str]]:
    """設定ファイルを読み込み"""
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    
    # 構造検証
    validation_errors = self.validate_config_structure(config_data)
    if validation_errors:
        return False, None, validation_errors
    
    # Configurationオブジェクトの作成
    patterns = []
    for pattern_data in config_data["patterns"]:
        pattern = ConfigPattern(
            name=pattern_data["name"],
            description=pattern_data.get("description", ""),
            screen_ids=pattern_data["screen_ids"],
            command=pattern_data["command"],
        )
        patterns.append(pattern)
    
    config = Configuration(version=config_data["version"], patterns=patterns)
    return True, config, []
```

### Python Objects to JSON

When saving configurations (e.g., with `--save-current`), Python objects are converted back to JSON:

```python
def save_config(self, config_path: Path, config: Configuration) -> bool:
    """設定ファイルを保存"""
    config_data = {
        "version": config.version,
        "patterns": [
            {
                "name": p.name,
                "description": p.description,
                "screen_ids": p.screen_ids,
                "command": p.command,
            }
            for p in config.patterns
        ],
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    return True
```

## Validation Logic

### Configuration Validation

The `ConfigManager.validate_config_structure()` method performs comprehensive validation:

1. **Top-level fields**: Check for required `version` and `patterns` fields
2. **Type checking**: Ensure fields have correct types
3. **Pattern validation**: Validate each pattern in the array
4. **Field requirements**: Check required fields in each pattern
5. **Command validation**: Ensure commands start with "displayplacer"

### Pattern Validation

The `PatternMatcher.validate_patterns()` method checks:

1. **Duplicate names**: Ensure pattern names are unique
2. **Screen ID format**: Validate Screen ID format (UUID-like)
3. **Command syntax**: Basic displayplacer command syntax check

## Data Flow

### Configuration Loading Flow

```
1. Determine config file path (CLI arg > env var > default)
   ↓
2. Check file existence
   ↓
3. Load JSON file
   ↓
4. Validate JSON structure
   ↓
5. Create ConfigPattern objects
   ↓
6. Create Configuration object
   ↓
7. Store in ConfigManager
```

### Layout Saving Flow

```
1. Get current display configuration (DisplayManager)
   ↓
2. Extract Screen IDs and command
   ↓
3. Generate pattern name
   ↓
4. Load existing configuration
   ↓
5. Check for duplicate Screen ID sets
   ↓
6. Add or update pattern
   ↓
7. Convert to JSON
   ↓
8. Save to file
```

## Error Handling

### Validation Errors

All validation errors are collected and returned as a list of error messages:

```python
errors = [
    "必須フィールド 'version' が見つかりません",
    "パターン 1: 必須フィールド 'name' が見つかりません",
    "パターン 2: 'command' は 'displayplacer' で開始する必要があります"
]
```

### Exception Handling

Dataclass `__post_init__` methods raise `ValueError` for invalid data:

```python
try:
    pattern = ConfigPattern(
        name="",  # Invalid: empty name
        description="Test",
        screen_ids=["ID1"],
        command="displayplacer ..."
    )
except ValueError as e:
    print(f"Validation error: {e}")
```

## Best Practices

### Creating Patterns

1. **Use descriptive names**: "Home Office Setup" instead of "Pattern1"
2. **Add descriptions**: Help users understand when to use each pattern
3. **Test commands**: Verify displayplacer commands work before saving
4. **Use --save-current**: Automatically generate patterns from current layout

### Configuration Management

1. **Validate before use**: Use `--validate-config` to check configuration
2. **Backup configurations**: Keep backup copies of working configurations
3. **Version control**: Track configuration changes in version control
4. **Document patterns**: Add clear descriptions to each pattern

### Data Integrity

1. **Immutable patterns**: Don't modify ConfigPattern objects after creation
2. **Validation on load**: Always validate configuration on load
3. **Error handling**: Handle all validation errors gracefully
4. **Atomic updates**: Save configuration atomically to prevent corruption
