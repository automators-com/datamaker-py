#!/usr/bin/env python3
"""Test runner script for datamaker-py tests."""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'=' * 60}")

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Main test runner function."""
    print("DataMaker Python Client Test Suite")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("../../src/datamaker"):
        print("Error: Please run this script from the project root directory")
        sys.exit(1)

    # Install test dependencies
    print("\nInstalling test dependencies...")
    if not run_command(
        "pip install pytest pytest-mock pytest-cov", "Installing test dependencies"
    ):
        print("Failed to install test dependencies")
        sys.exit(1)

    # Run unit tests
    print("\nRunning unit tests...")
    if not run_command(
        "python -m pytest ../test_main.py ../test_routes.py -v", "Unit tests"
    ):
        print("Unit tests failed")
        sys.exit(1)

    # Run integration tests
    print("\nRunning integration tests...")
    if not run_command(
        "python -m pytest ../test_integration.py -v", "Integration tests"
    ):
        print("Integration tests failed")
        sys.exit(1)

    # Run all tests with coverage
    print("\nRunning all tests with coverage...")
    if not run_command(
        "python -m pytest ../ --cov=../../src/datamaker --cov-report=term-missing",
        "All tests with coverage",
    ):
        print("Tests with coverage failed")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
