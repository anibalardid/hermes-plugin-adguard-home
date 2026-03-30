"""Hermes AdGuard Home plugin.

Controls a local AdGuard Home instance via its REST API.
Provides 17 tools covering protection, filtering, query logs,
statistics, clients, DNS rewrites, blocked services, and access control.

Requires: AdGuard Home running locally (default: http://127.0.0.1:3000).
Configure via environment variables:
  ADGUARD_HOST     — base URL (default: http://127.0.0.1:3000)
  ADGUARD_USER     — username (default: admin)
  ADGUARD_PASSWORD — password (default: empty)
"""

import logging
import shutil
from pathlib import Path

from . import schemas
from . import tools

logger = logging.getLogger(__name__)

_PLUGIN_DIR = Path(__file__).parent


def _install_skill():
    """Copy bundled skill.md to ~/.hermes/skills/ on first load."""
    try:
        from hermes_cli.config import get_hermes_home
        dest = get_hermes_home() / "skills" / "adguard-home-plugin" / "SKILL.md"
    except Exception:
        dest = Path.home() / ".hermes" / "skills" / "adguard-home-plugin" / "SKILL.md"

    source = _PLUGIN_DIR / "skill.md"
    if not source.exists() or dest.exists():
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    logger.info("Installed adguard-home-plugin skill to %s", dest)


def register(ctx):
    """Register all 17 AdGuard Home tools."""

    schema_map = {s["name"]: s for s in schemas.ALL_SCHEMAS}

    _tool_handlers = {
        "adguard_status": tools.adguard_status,
        "adguard_protection": tools.adguard_protection,
        "adguard_cache_clear": tools.adguard_cache_clear,
        "adguard_stats": tools.adguard_stats,
        "adguard_stats_reset": tools.adguard_stats_reset,
        "adguard_querylog": tools.adguard_querylog,
        "adguard_querylog_clear": tools.adguard_querylog_clear,
        "adguard_filtering_status": tools.adguard_filtering_status,
        "adguard_filtering_add": tools.adguard_filtering_add,
        "adguard_filtering_remove": tools.adguard_filtering_remove,
        "adguard_filtering_refresh": tools.adguard_filtering_refresh,
        "adguard_filtering_rules": tools.adguard_filtering_rules,
        "adguard_filtering_check": tools.adguard_filtering_check,
        "adguard_clients": tools.adguard_clients,
        "adguard_rewrite": tools.adguard_rewrite,
        "adguard_blocked_services": tools.adguard_blocked_services,
        "adguard_access": tools.adguard_access,
    }

    for name, handler in _tool_handlers.items():
        ctx.register_tool(
            name=name,
            toolset="adguard",
            schema=schema_map[name],
            handler=handler,
        )

    _install_skill()

    logger.info("AdGuard Home plugin loaded: %d tools", len(_tool_handlers))
