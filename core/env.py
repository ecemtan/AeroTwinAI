"""Load the developer's local .env (repository root) into os.environ.

Real environment variables always win (override=False). The .env file is
git-ignored; .env.example documents every supported variable.
"""

from __future__ import annotations

from dotenv import load_dotenv

from core.aircraft_registry import project_root

_loaded = False


def load_local_env() -> None:
    global _loaded
    if not _loaded:
        load_dotenv(project_root() / ".env", override=False)
        _loaded = True
