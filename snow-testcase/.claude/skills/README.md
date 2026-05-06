# Test Runner Skill Quick Start Guide

## Overview
The Test Runner skill provides a configurable way to run tests in your project with customizable directories, ignore rules, and test reports.

## Setup
1. The skill is already installed at `.claude/skills/test_runner.py`
2. Default configuration is at `.claude/config/test_runner.json`
3. Modify the configuration as needed for your project

## Running Tests
Execute the test runner using Python:
```
python .claude/skills/test_runner.py
```

## Configuration Options
You can customize the test runner by editing `.claude/config/test_runner.json`:

- `test_directories`: Where to look for test files
- `ignore_patterns`: Which directories/files to skip
- `report_format`: Output format ("summary" or "detailed")
- `fail_fast`: Stop on first failure

## Command Line Options
- `--config` or `-c`: Use a different config file
- `--directory` or `-d`: Add additional test directory (can be used multiple times)
- `--format` or `-f`: Specify report format ("summary" or "detailed")
- `--list`: Show found test files without running them

## Example Commands
List all test files:
```
python .claude/skills/test_runner.py --list
```

Run with additional test directory:
```
python .claude/skills/test_runner.py --directory integration_tests
```

Run with detailed output:
```
python .claude/skills/test_runner.py --format detailed
```

## Integration with Claude Code
To use this skill from Claude Code, you can call:
```
Skill(skill="test_runner", args="")
```

Or create a convenience function in your Claude setup to run this automatically.