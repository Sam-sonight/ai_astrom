"""
AI Astrom Environment Setup Script
----------------------------------
Creates virtual environment, installs dependencies modularly,
and verifies core imports.
"""

import os
import subprocess
import sys
from pathlib import Path

def run(cmd: str):
    print(f"→ {cmd}")
    subprocess.check_call(cmd, shell=True)

def main():
    base_dir = Path(__file__).resolve().parents[1]
    req_dir = base_dir / "requirements"
    venv_path = base_dir / ".venv"

    print("=== AI Astrom Environment Setup ===")

    # 1️⃣ Create virtual environment
    if not venv_path.exists():
        run(f"{sys.executable} -m venv .venv")

    # 2️⃣ Activate environment (platform-aware)
    if os.name == "nt":
        activate_cmd = f"{venv_path}\\Scripts\\activate"
    else:
        activate_cmd = f"source {venv_path}/bin/activate"
    print(f"Activation command: {activate_cmd}")

    # 3️⃣ Upgrade pip
    run(f"{venv_path}/Scripts/pip install --upgrade pip" if os.name == "nt" else f"{venv_path}/bin/pip install --upgrade pip")

    # 4️⃣ Install all dependencies
    run(f"{venv_path}/Scripts/pip install -r {req_dir}/all.txt" if os.name == "nt" else f"{venv_path}/bin/pip install -r {req_dir}/all.txt")

    # 5️⃣ Verify critical imports
    print("=== Verifying imports ===")
    verify_cmds = [
        "fastapi", "sqlalchemy", "pyswisseph", "openai", "celery", "pytest"
    ]
    for pkg in verify_cmds:
        try:
            __import__(pkg)
            print(f"✅ {pkg} import OK")
        except ImportError:
            print(f"⚠️ Warning: could not import {pkg}")

    print("✅ Setup complete. Activate your environment and run:")
    print("   uvicorn backend.main:app --reload")

if __name__ == "__main__":
    main()
