"""
Test Runner Skill for Claude Code
This module allows Claude Code to run configurable tests with custom settings.
"""

import subprocess
import sys
import os
from pathlib import Path

def run(args: str = ""):
    """
    Execute the test runner skill with the provided arguments.

    Args:
        args: Command line arguments to pass to the test runner
    """
    script_path = Path(__file__).parent / "test_runner.py"

    if not script_path.exists():
        print(f"Error: Test runner script not found at {script_path}")
        return

    # Parse arguments
    import shlex
    try:
        arg_list = shlex.split(args) if args else []
    except ValueError as e:
        print(f"Error parsing arguments: {e}")
        arg_list = []

    # Prepend script path
    cmd = [sys.executable, str(script_path)] + arg_list

    try:
        result = subprocess.run(cmd, check=True)
        print(f"Test runner completed with exit code: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"Test runner failed with exit code: {e.returncode}")
    except Exception as e:
        print(f"Error running test runner: {e}")

# For direct command line execution
if __name__ == "__main__":
    import sys
    args = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    run(args)