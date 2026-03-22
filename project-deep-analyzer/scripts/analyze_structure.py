#!/usr/bin/env python3
"""
Project Structure Analyzer for Project Deep Analyzer

Analyzes project structure to identify key files, modules, and patterns.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
import json


# Common patterns for identifying project type and key files
PATTERNS = {
    "python": {
        "extensions": [".py"],
        "entry_points": ["main.py", "run.py", "train.py", "app.py", "__main__.py"],
        "config": ["config.yaml", "config.yml", "settings.py", "hydra"],
        "requirements": ["requirements.txt", "setup.py", "pyproject.toml", "setup.cfg"],
        "tests": ["tests/", "test_", "_test.py"],
    },
    "javascript": {
        "extensions": [".js", ".jsx", ".ts", ".tsx"],
        "entry_points": ["index.js", "app.js", "main.js", "server.js"],
        "config": ["package.json", "tsconfig.json", ".env"],
        "requirements": ["package.json"],
        "tests": ["test/", "tests/", "__tests__/", ".test.js", ".spec.js"],
    },
}

# Core module patterns to identify
CORE_PATTERNS = [
    "model", "models", "network", "networks", "architecture",
    "attention", "transformer", "encoder", "decoder",
    "loss", "criterion", "objective",
    "data", "dataset", "dataloader", "preprocess",
    "trainer", "train", "training", "engine",
    "inference", "predict", "generate",
    "embedding", "token", "vocab",
]


def analyze_project(project_path: Path) -> Dict:
    """
    Analyze project structure and return comprehensive information.

    Args:
        project_path: Path to the project root

    Returns:
        Dictionary containing analysis results
    """
    result = {
        "path": str(project_path),
        "type": None,
        "structure": {},
        "key_files": [],
        "core_modules": [],
        "statistics": {},
    }

    # Detect project type
    result["type"] = detect_project_type(project_path)

    # Analyze directory structure
    result["structure"] = get_directory_tree(project_path)

    # Find key files
    result["key_files"] = find_key_files(project_path, result["type"])

    # Identify core modules
    result["core_modules"] = identify_core_modules(project_path, result["type"])

    # Get statistics
    result["statistics"] = get_statistics(project_path, result["type"])

    return result


def detect_project_type(project_path: Path) -> str:
    """Detect the primary project type based on files present."""
    files = set(f.name.lower() for f in project_path.iterdir() if f.is_file())

    # Check for Python
    if any(f.endswith(".py") for f in files) or "requirements.txt" in files or "pyproject.toml" in files:
        return "python"

    # Check for JavaScript/TypeScript
    if "package.json" in files:
        return "javascript"

    # Check for mixed or other
    extensions = defaultdict(int)
    for f in project_path.rglob("*"):
        if f.is_file() and f.suffix:
            extensions[f.suffix] += 1

    if extensions.get(".py", 0) > extensions.get(".js", 0):
        return "python"
    elif extensions.get(".js", 0) > 0:
        return "javascript"

    return "unknown"


def get_directory_tree(project_path: Path, max_depth: int = 3) -> Dict:
    """Get a simplified directory tree structure."""
    def build_tree(path: Path, depth: int = 0) -> Dict:
        if depth > max_depth:
            return {"...": "truncated"}

        tree = {}
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        except PermissionError:
            return {"...": "permission denied"}

        for item in items[:50]:  # Limit items per directory
            # Skip hidden and common ignore patterns
            if item.name.startswith(".") or item.name in ["__pycache__", "node_modules", ".git", "dist", "build"]:
                continue

            if item.is_dir():
                tree[item.name + "/"] = build_tree(item, depth + 1)
            else:
                tree[item.name] = None

        return tree

    return build_tree(project_path)


def find_key_files(project_path: Path, project_type: str) -> List[Dict]:
    """Find key files in the project."""
    key_files = []
    patterns = PATTERNS.get(project_type, PATTERNS["python"])

    # Find entry points
    for entry in patterns["entry_points"]:
        matches = list(project_path.rglob(entry))
        for match in matches:
            key_files.append({
                "path": str(match.relative_to(project_path)),
                "type": "entry_point",
                "priority": "high"
            })

    # Find config files
    for config in patterns["config"]:
        matches = list(project_path.rglob(config))
        for match in matches:
            key_files.append({
                "path": str(match.relative_to(project_path)),
                "type": "config",
                "priority": "medium"
            })

    # Find README
    readme_matches = list(project_path.glob("README*"))
    for match in readme_matches:
        key_files.append({
            "path": str(match.relative_to(project_path)),
            "type": "documentation",
            "priority": "high"
        })

    return key_files


def identify_core_modules(project_path: Path, project_type: str) -> List[Dict]:
    """Identify core modules based on naming patterns."""
    core_modules = []
    extensions = PATTERNS.get(project_type, PATTERNS["python"])["extensions"]

    for pattern in CORE_PATTERNS:
        for ext in extensions:
            # Match files containing the pattern
            matches = list(project_path.rglob(f"*{pattern}*{ext}"))
            for match in matches[:5]:  # Limit matches per pattern
                # Calculate lines of code
                try:
                    loc = sum(1 for _ in open(match, "r", encoding="utf-8", errors="ignore"))
                except:
                    loc = 0

                core_modules.append({
                    "path": str(match.relative_to(project_path)),
                    "pattern": pattern,
                    "loc": loc,
                })

    # Sort by LOC (larger files likely more important)
    core_modules.sort(key=lambda x: x["loc"], reverse=True)

    return core_modules[:20]  # Return top 20


def get_statistics(project_path: Path, project_type: str) -> Dict:
    """Get project statistics."""
    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_loc": 0,
        "by_extension": defaultdict(int),
    }

    extensions = PATTERNS.get(project_type, PATTERNS["python"])["extensions"]

    for f in project_path.rglob("*"):
        if f.is_file():
            # Skip hidden and common ignore patterns
            if any(part.startswith(".") or part in ["__pycache__", "node_modules", "dist", "build"]
                   for part in f.parts):
                continue

            stats["total_files"] += 1

            if f.suffix in extensions:
                try:
                    loc = sum(1 for _ in open(f, "r", encoding="utf-8", errors="ignore"))
                    stats["total_loc"] += loc
                    stats["by_extension"][f.suffix] += loc
                except:
                    pass

        elif f.is_dir():
            stats["total_dirs"] += 1

    stats["by_extension"] = dict(stats["by_extension"])
    return stats


def print_analysis_report(analysis: Dict) -> str:
    """Generate a human-readable analysis report."""
    lines = []
    lines.append(f"# Project Analysis: {Path(analysis['path']).name}")
    lines.append("")
    lines.append(f"**Type**: {analysis['type']}")
    lines.append("")

    # Statistics
    stats = analysis["statistics"]
    lines.append("## Statistics")
    lines.append(f"- Total files: {stats['total_files']}")
    lines.append(f"- Total directories: {stats['total_dirs']}")
    lines.append(f"- Total lines of code: {stats['total_loc']}")
    lines.append("")

    # Key files
    lines.append("## Key Files")
    for kf in analysis["key_files"][:10]:
        lines.append(f"- `{kf['path']}` ({kf['type']})")
    lines.append("")

    # Core modules
    lines.append("## Core Modules")
    for cm in analysis["core_modules"][:10]:
        lines.append(f"- `{cm['path']}` ({cm['loc']} LOC)")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze project structure")
    parser.add_argument("project_path", help="Path to the project")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"Error: Path {project_path} does not exist")
        exit(1)

    analysis = analyze_project(project_path)

    if args.json:
        output = json.dumps(analysis, indent=2)
    else:
        output = print_analysis_report(analysis)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Analysis saved to {args.output}")
    else:
        print(output)
