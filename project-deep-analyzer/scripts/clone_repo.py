#!/usr/bin/env python3
"""
Repository Cloning Utility for Project Deep Analyzer

Clones a Git repository to a temporary directory for analysis.
Supports shallow clone for efficiency.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional
import argparse


def clone_repository(
    repo_url: str,
    target_dir: Optional[str] = None,
    shallow: bool = True,
    branch: Optional[str] = None
) -> Path:
    """
    Clone a Git repository for analysis.

    Args:
        repo_url: URL of the Git repository
        target_dir: Target directory (default: temp directory)
        shallow: Whether to perform shallow clone (depth=1)
        branch: Specific branch to clone

    Returns:
        Path to the cloned repository

    Raises:
        subprocess.CalledProcessError: If git clone fails
    """
    if target_dir is None:
        # Create temp directory
        target_dir = tempfile.mkdtemp(prefix="repo_analysis_")

    target_path = Path(target_dir)

    # Build git clone command
    cmd = ["git", "clone"]

    if shallow:
        cmd.extend(["--depth", "1"])

    if branch:
        cmd.extend(["--branch", branch])

    cmd.extend([repo_url, str(target_path)])

    print(f"Cloning repository: {repo_url}")
    print(f"Target directory: {target_path}")

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Clone successful!")
        return target_path
    except subprocess.CalledProcessError as e:
        print(f"Clone failed: {e.stderr}")
        raise


def cleanup_repo(repo_path: Path) -> None:
    """
    Remove the cloned repository.

    Args:
        repo_path: Path to the repository
    """
    if repo_path.exists():
        shutil.rmtree(repo_path)
        print(f"Cleaned up: {repo_path}")


def get_repo_info(repo_path: Path) -> dict:
    """
    Get basic information about the repository.

    Args:
        repo_path: Path to the repository

    Returns:
        Dictionary with repo info
    """
    info = {}

    # Get remote URL
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        info["remote_url"] = result.stdout.strip()
    except subprocess.CalledProcessError:
        info["remote_url"] = "Unknown"

    # Get current branch
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        info["branch"] = result.stdout.strip()
    except subprocess.CalledProcessError:
        info["branch"] = "Unknown"

    # Get last commit
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H %s"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        info["last_commit"] = result.stdout.strip()
    except subprocess.CalledProcessError:
        info["last_commit"] = "Unknown"

    return info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clone repository for analysis")
    parser.add_argument("repo_url", help="URL of the Git repository")
    parser.add_argument("--target", "-t", help="Target directory")
    parser.add_argument("--no-shallow", action="store_true", help="Disable shallow clone")
    parser.add_argument("--branch", "-b", help="Specific branch to clone")
    parser.add_argument("--info", "-i", action="store_true", help="Show repo info after cloning")

    args = parser.parse_args()

    repo_path = clone_repository(
        args.repo_url,
        args.target,
        shallow=not args.no_shallow,
        branch=args.branch
    )

    if args.info:
        info = get_repo_info(repo_path)
        print("\nRepository Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
