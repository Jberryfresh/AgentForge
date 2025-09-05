"""
Config loader for the project agent.

Usage
- Programmatic:
    from agent.load_config import load_config, load_system_prompt
    cfg = load_config()
    prompt = load_system_prompt(cfg)
- CLI check:
    python3 agent/load_config.py --check
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


class ConfigError(Exception):
    pass


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise ConfigError(msg)


def load_config(config_path: str | Path = "agent/config.json", base_dir: str | Path | None = None) -> Dict[str, Any]:
    base = Path(base_dir) if base_dir is not None else Path.cwd()
    cfg_path = Path(config_path)
    if not cfg_path.is_absolute():
        cfg_path = base / cfg_path

    try:
        raw = cfg_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {cfg_path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {cfg_path}: {e}") from e

    # Validate required fields
    _require(isinstance(data.get("model"), str) and data["model"].strip(), "'model' must be a non-empty string")
    _require(isinstance(data.get("temperature"), (int, float)), "'temperature' must be a number")
    _require(isinstance(data.get("top_p"), (int, float)), "'top_p' must be a number")
    _require(isinstance(data.get("system_prompt_path"), str) and data["system_prompt_path"].strip(), "'system_prompt_path' must be a non-empty string path")

    # Bounds checks (lenient defaults)
    temp = float(data["temperature"])  # type: ignore[arg-type]
    top_p = float(data["top_p"])  # type: ignore[arg-type]
    _require(0.0 <= temp <= 2.0, "'temperature' must be between 0.0 and 2.0")
    _require(0.0 < top_p <= 1.0, "'top_p' must be in (0.0, 1.0]")

    # Prompt path exists
    prompt_path = data["system_prompt_path"]
    prompt_abs = (base / prompt_path) if not Path(prompt_path).is_absolute() else Path(prompt_path)
    _require(prompt_abs.exists(), f"system_prompt_path not found: {prompt_abs}")

    # Stash resolved path for convenience
    data["_resolved_system_prompt_path"] = str(prompt_abs)
    return data


def load_system_prompt(config: Dict[str, Any]) -> str:
    """Load the system prompt text from the resolved path in the config.

    Falls back to `system_prompt_path` if `_resolved_system_prompt_path` is missing.
    Raises ConfigError with a clear message if the path is absent or unreadable.
    """
    raw_path = config.get("_resolved_system_prompt_path") or config.get("system_prompt_path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ConfigError("system_prompt_path is missing or invalid in config")
    try:
        p = Path(raw_path)
        return p.read_text(encoding="utf-8").strip()
    except Exception as e:
        raise ConfigError(f"Failed to read system prompt from {raw_path}: {e}") from e


def _main() -> int:
    parser = argparse.ArgumentParser(description="Validate and inspect agent config")
    parser.add_argument("--check", action="store_true", help="Validate config and prompt path")
    parser.add_argument("--print", dest="do_print", action="store_true", help="Print resolved config and first 120 chars of prompt")
    args = parser.parse_args()

    try:
        cfg = load_config()
        if args.do_print:
            prompt = load_system_prompt(cfg)
            preview = (prompt[:120] + ("…" if len(prompt) > 120 else "")).replace("\n", " ")
            print(json.dumps({
                "model": cfg["model"],
                "temperature": cfg["temperature"],
                "top_p": cfg["top_p"],
                "system_prompt_path": cfg["_resolved_system_prompt_path"],
                "prompt_preview": preview,
            }, indent=2))
        elif args.check:
            print("OK: agent/config.json and system prompt look good.")
        else:
            print("Config loads successfully. Use --check or --print for details.")
        return 0
    except ConfigError as e:
        print(f"ERROR: {e}", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(_main())
