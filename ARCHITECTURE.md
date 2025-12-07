English / [**日本語**](ARCHITECTURE_JP.md)

# Architecture Document

## System Overview

Display Layout Manager is a tool for automatically managing display layouts on macOS. It provides two interfaces: CLI and menu bar app, automating display configuration detection, pattern matching, and layout application.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
├──────────────────────────┬──────────────────────────────────┤
│   CLI (main.py)          │  Menu Bar App (menubar_app.py)   │
│   - Command-line parsing │  - rumps-based GUI               │
│   - Interactive ops      │  - Menu item management          │
└──────────────┬───────────┴────────────┬─────────────────────┘
               │                        │
               └────────┬───────────────┘
                        │
         ┌──────────────┴──────────────┐
         │   CLI Bridge (cli_bridge.py) │
         │   - UI to business logic     │
         └──────────────┬──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │      Business Logic Layer    │
         ├─────────────────────────────┤
         │  Config Manager              │
         │  - Config file loading       │
         │  - JSON parsing/validation   │
         ├─────────────────────────────┤
         │  Display Manager             │
         │  - Display detection         │
         │  - Screen ID extraction      │
         ├─────────────────────────────┤
         │  Pattern Matcher             │
         │  - Pattern matching          │
         │  - Optimal layout selection  │
         ├─────────────────────────────┤
         │  Layout Saver                │
         │  - Current layout saving     │
         │  - Config file update        │
         ├─────────────────────────────┤
         │  Command Executor            │
         │  - displayplacer execution   │
         │  - Command validation        │
         ├─────────────────────────────┤
         │  Dependency Manager          │
         │  - Dependency checking       │
         │  - Auto installation         │
         ├─────────────────────────────┤
         │  Auto Launch Manager         │
         │  - LaunchAgent management    │
         │  - Auto-launch configuration │
         └──────────────┬──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │    Infrastructure Layer      │
         ├─────────────────────────────┤
         │  Logger (logger.py)          │
         │  - Structured logging        │
         │  - File rotation             │
         ├─────────────────────────────┤
         │  Error Handler               │
         │  - Error handling            │
         │  - User-friendly messages    │
         └──────────────┬──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │      External Dependencies   │
         ├─────────────────────────────┤
         │  displayplacer               │
         │  - Display configuration     │
         ├─────────────────────────────┤
         │  GNU grep                    │
         │  - Text search               │
         ├─────────────────────────────┤
         │  Homebrew                    │
         │  - Package management        │
         └─────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### CLI (main.py)
- **Responsibility**: Command-line argument parsing, user input processing
- **Key Features**:
  - Argument parsing with `argparse`
  - Processing various options (`--show-displays`, `--save-current`, `--dry-run`, etc.)
  - Delegation to CLI Bridge
- **Dependencies**: `cli_bridge.CLIBridge`, `logger.Logger`

#### Menu Bar App (menubar_app.py)
- **Responsibility**: Providing macOS menu bar application
- **Key Features**:
  - GUI using `rumps` framework
  - Dynamic menu item generation
  - User action handling
  - Auto-launch configuration management
- **Dependencies**: `rumps`, `cli_bridge.CLIBridge`, `auto_launch_manager.AutoLaunchManager`

### 2. Business Logic Layer

#### CLI Bridge (cli_bridge.py)
- **Responsibility**: Bridge between UI layer and business logic layer
- **Key Features**:
  - Integration of various operations (layout application, saving, display, etc.)
  - Unified error handling
  - Unified log output
- **Dependencies**: All business logic components

#### Config Manager (config_manager.py)
- **Responsibility**: Configuration file management
- **Key Features**:
  - JSON configuration file loading
  - Configuration file validation
  - Default configuration generation
  - Configuration file updates
- **Data Structure**:
  ```python
  {
      "version": str,
      "patterns": [
          {
              "name": str,
              "description": str,
              "screen_ids": List[str],
              "command": str
          }
      ]
  }
  ```

#### Display Manager (display_manager.py)
- **Responsibility**: Display information retrieval
- **Key Features**:
  - Executing `displayplacer list` command
  - Persistent Screen ID extraction
  - Current display configuration retrieval
- **Dependencies**: `subprocess`, `re`

#### Pattern Matcher (pattern_matcher.py)
- **Responsibility**: Display configuration and pattern matching
- **Key Features**:
  - Screen ID set comparison
  - Optimal pattern selection
  - Matching result return
- **Algorithm**: Exact set matching (order-independent)

#### Layout Saver (layout_saver.py)
- **Responsibility**: Current layout saving
- **Key Features**:
  - Current display configuration retrieval
  - Command extraction from `displayplacer list`
  - Automatic pattern name generation
  - Configuration file addition/update
- **Naming Convention**: `{count}_Displays_{id1}_{id2}_{id3}`

#### Command Executor (command_executor.py)
- **Responsibility**: displayplacer command execution
- **Key Features**:
  - Command validation
  - Dry-run mode support
  - Command execution and error handling
- **Dependencies**: `subprocess`

#### Dependency Manager (dependency_manager.py)
- **Responsibility**: External dependency management
- **Key Features**:
  - Homebrew existence check
  - displayplacer existence check and installation
  - GNU grep existence check and installation
  - Installation status reporting
- **Dependencies**: `subprocess`, `shutil`

#### Auto Launch Manager (auto_launch_manager.py)
- **Responsibility**: Login auto-launch management
- **Key Features**:
  - LaunchAgent plist file creation
  - Auto-launch enable/disable
  - Current state checking
- **File**: `~/Library/LaunchAgents/com.displaylayoutmanager.menubar.plist`

### 3. Infrastructure Layer

#### Logger (logger.py)
- **Responsibility**: Log output management
- **Key Features**:
  - Structured logging (JSON format)
  - File rotation (daily)
  - Console and file output
  - Log level management
- **Log Files**: `~/Library/Logs/DisplayLayoutManager/`

#### Error Handler (error_handler.py)
- **Responsibility**: Unified error handling
- **Key Features**:
  - Custom exception class definitions
  - User-friendly error messages
  - Troubleshooting guide provision
- **Exception Hierarchy**:
  ```
  DisplayLayoutError (base class)
  ├── ConfigError (configuration file errors)
  ├── DisplayDetectionError (display detection errors)
  ├── PatternMatchError (pattern matching errors)
  ├── CommandExecutionError (command execution errors)
  └── DependencyError (dependency errors)
  ```

## Data Flow

### Layout Application Flow

```
1. User Input
   ↓
2. CLI / Menu Bar App
   ↓
3. CLI Bridge.apply_layout()
   ↓
4. Dependency Manager.check_dependencies()
   ├→ Homebrew check
   ├→ displayplacer check
   └→ GNU grep check
   ↓
5. Config Manager.load_config()
   ├→ Config file loading
   └→ JSON parsing/validation
   ↓
6. Display Manager.get_current_displays()
   ├→ displayplacer list execution
   └→ Screen ID extraction
   ↓
7. Pattern Matcher.find_matching_pattern()
   ├→ Screen ID set comparison
   └→ Optimal pattern selection
   ↓
8. Command Executor.execute()
   ├→ Command validation
   └→ displayplacer execution
   ↓
9. Result return
```

### Layout Saving Flow

```
1. User Input (--save-current)
   ↓
2. CLI / Menu Bar App
   ↓
3. CLI Bridge.save_current_layout()
   ↓
4. Display Manager.get_current_displays()
   ├→ displayplacer list execution
   └→ Screen ID extraction
   ↓
5. Layout Saver.save_current_layout()
   ├→ Current command retrieval
   ├→ Pattern name generation
   └→ Config file update
   ↓
6. Config Manager.save_config()
   ├→ JSON serialization
   └→ File writing
   ↓
7. Result return
```

## Design Principles

### 1. Single Responsibility Principle (SRP)
Each component has only one responsibility. For example, `ConfigManager` handles only configuration file management, while display detection is handled by `DisplayManager`.

### 2. Dependency Inversion Principle (DIP)
High-level modules (CLI Bridge) depend on low-level modules (managers), but maintain loose coupling through interfaces.

### 3. Open-Closed Principle (OCP)
New features (e.g., new pattern matching algorithms) can be added without modifying existing code.

### 4. Error Handling
All errors are properly caught and provide user-friendly messages and troubleshooting guides.

### 5. Logging
All important operations are logged for easy debugging and troubleshooting.

## Testing Strategy

### Unit Tests
Each component can be tested independently:
- `test_config_manager.py`: Configuration file loading/validation
- `test_display_manager.py`: Display detection
- `test_pattern_matcher.py`: Pattern matching
- `test_command_executor.py`: Command execution
- `test_layout_saver.py`: Layout saving

### Integration Tests
- `test_cli_components.py`: CLI component integration tests
- `test_menubar_integration.py`: Menu bar app integration tests
- `integration_test.py`: End-to-end tests

### Test Coverage
- Target: 70%+
- Current: Automatically measured in CI/CD
- Reports: Visualized with Codecov

## Performance Considerations

### Startup Time
- Dependency check: ~100ms
- Config file loading: ~10ms
- Display detection: ~200ms
- Total: ~300ms

### Memory Usage
- CLI: ~20MB
- Menu Bar App: ~30MB

### Disk Usage
- Application: ~3.5MB
- Log files: ~1MB/day (automatic rotation)

## Security Considerations

### File Permissions
- Config files: `0600` (user read/write only)
- Log files: `0600` (user read/write only)
- LaunchAgent plist: `0644` (standard permissions)

### Command Execution
- Safe command execution using `subprocess`
- Shell injection prevention
- Command validation

### Dependencies
- Install only from trusted sources (Homebrew)
- Version pinning for reproducibility

## Extensibility

### New Pattern Matching Algorithms
Extend the `PatternMatcher` class to add more advanced matching logic.

### New Interfaces
Use CLI Bridge to easily add new UIs (e.g., web interface).

### Plugin System
Future plans to provide extension points for custom plugins.

## Future Improvements

1. **Profile Feature**: Support multiple configuration profiles
2. **Cloud Sync**: Configuration sync using iCloud
3. **Hotkey Support**: Layout switching with keyboard shortcuts
4. **Notifications**: Notification display when applying layouts
5. **Plugin System**: Support for adding custom features
