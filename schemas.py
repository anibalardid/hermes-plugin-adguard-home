ADGUARD_STATUS = {
    "name": "adguard_status",
    "description": (
        "Get AdGuard Home server status: whether protection is enabled, DNS upstream servers, "
        "version, running state, and general settings. Use this as a first check to confirm "
        "the server is reachable and see the current configuration at a glance."
    ),
    "parameters": {"type": "object", "properties": {}, "required": []},
}

ADGUARD_PROTECTION = {
    "name": "adguard_protection",
    "description": (
        "Enable or disable AdGuard Home protection (ad/tracker blocking). "
        "Use enabled=true to turn protection on, enabled=false to turn it off. "
        "Optionally pause protection for a number of milliseconds with duration_ms "
        "(e.g. 300000 = 5 minutes), after which it re-enables automatically."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "description": "True to enable protection, false to disable",
            },
            "duration_ms": {
                "type": "integer",
                "description": "Pause duration in milliseconds (optional). Only used when enabled=false.",
            },
        },
        "required": ["enabled"],
    },
}

ADGUARD_STATS = {
    "name": "adguard_stats",
    "description": (
        "Get DNS query statistics: total queries, blocked queries, blocked percentage, "
        "top queried domains, top blocked domains, top clients, and queries over time. "
        "Use to understand traffic patterns and what's being blocked."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "recent_ms": {
                "type": "integer",
                "description": (
                    "Lookback period in milliseconds. Must be a multiple of 3600000 (1 hour). "
                    "Defaults to the configured statistics interval if omitted."
                ),
            }
        },
        "required": [],
    },
}

ADGUARD_STATS_RESET = {
    "name": "adguard_stats_reset",
    "description": "Reset all AdGuard Home statistics to zero. Use when starting fresh tracking.",
    "parameters": {"type": "object", "properties": {}, "required": []},
}

ADGUARD_QUERYLOG = {
    "name": "adguard_querylog",
    "description": (
        "Get the DNS query log. Shows recent DNS queries with domain, client IP, "
        "response status (blocked/allowed/rewritten), upstream used, and latency. "
        "Can be filtered by domain/IP search term and response status. "
        "Use to debug why a site is blocked, check what a client is querying, "
        "or investigate suspicious traffic."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Max number of records to return (default 100)",
                "default": 100,
            },
            "offset": {
                "type": "integer",
                "description": "Skip this many records (for pagination)",
            },
            "search": {
                "type": "string",
                "description": "Filter by domain name or client IP address",
            },
            "response_status": {
                "type": "string",
                "enum": [
                    "all", "filtered", "blocked", "blocked_safebrowsing",
                    "blocked_parental", "whitelisted", "rewritten",
                    "safe_search", "processed",
                ],
                "description": "Filter by query result status",
            },
        },
        "required": [],
    },
}

ADGUARD_QUERYLOG_CLEAR = {
    "name": "adguard_querylog_clear",
    "description": "Clear the AdGuard Home query log. All DNS query history will be deleted.",
    "parameters": {"type": "object", "properties": {}, "required": []},
}

ADGUARD_FILTERING_STATUS = {
    "name": "adguard_filtering_status",
    "description": (
        "Get the current state of filtering: whether it's enabled, the list of subscribed "
        "filter lists (name, URL, enabled state, rule count), and any custom user rules. "
        "Use to see what blocklists are active."
    ),
    "parameters": {"type": "object", "properties": {}, "required": []},
}

ADGUARD_FILTERING_ADD = {
    "name": "adguard_filtering_add",
    "description": (
        "Add a new filter list (blocklist or allowlist) by URL. "
        "The list must be in hosts or adblock format. "
        "Example URLs: https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL of the filter list",
            },
            "name": {
                "type": "string",
                "description": "Display name for the filter list",
            },
            "whitelist": {
                "type": "boolean",
                "description": "True if this is an allowlist (whitelist), false for blocklist",
                "default": False,
            },
        },
        "required": ["url", "name"],
    },
}

ADGUARD_FILTERING_REMOVE = {
    "name": "adguard_filtering_remove",
    "description": "Remove a filter list by URL.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL of the filter list to remove",
            },
            "whitelist": {
                "type": "boolean",
                "description": "True if this is an allowlist",
                "default": False,
            },
        },
        "required": ["url"],
    },
}

ADGUARD_FILTERING_REFRESH = {
    "name": "adguard_filtering_refresh",
    "description": (
        "Force a refresh/update of all filter lists, downloading the latest rules. "
        "Use when lists may be stale or after adding a new list."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "whitelist": {
                "type": "boolean",
                "description": "True to refresh allowlists, false for blocklists",
                "default": False,
            }
        },
        "required": [],
    },
}

ADGUARD_FILTERING_RULES = {
    "name": "adguard_filtering_rules",
    "description": (
        "Set custom user-defined filtering rules. These rules take priority over filter lists. "
        "Use adblock syntax: '||example.com^' to block, '@@||example.com^' to allow/whitelist. "
        "Pass a list of rule strings. This REPLACES all existing custom rules."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "rules": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "List of adblock-syntax rules. Examples: "
                    "'||ads.example.com^' (block), '@@||safe.example.com^' (allow)"
                ),
            }
        },
        "required": ["rules"],
    },
}

ADGUARD_FILTERING_CHECK = {
    "name": "adguard_filtering_check",
    "description": (
        "Check whether a specific domain would be blocked, allowed, or rewritten "
        "by the current filtering configuration. Useful for debugging why something "
        "is or isn't being blocked without making an actual DNS query."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "host": {
                "type": "string",
                "description": "Domain name to check, e.g. 'ads.example.com'",
            }
        },
        "required": ["host"],
    },
}

ADGUARD_CLIENTS = {
    "name": "adguard_clients",
    "description": (
        "Manage AdGuard Home clients. Actions: "
        "'list' to see all configured clients; "
        "'add' to create a new client (requires name and at least one identifier); "
        "'update' to change a client's settings; "
        "'delete' to remove a client by name; "
        "'find' to look up a client by IP/MAC."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list", "add", "update", "delete", "find"],
                "description": "Operation to perform",
            },
            "name": {
                "type": "string",
                "description": "Client name (required for add/update/delete)",
            },
            "ids": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Client identifiers: IP, CIDR, MAC, or hostname (required for add)",
            },
            "use_global_settings": {
                "type": "boolean",
                "description": "Inherit global filtering settings (default true)",
                "default": True,
            },
            "filtering_enabled": {
                "type": "boolean",
                "description": "Enable filtering for this client (when use_global_settings=false)",
            },
            "safebrowsing_enabled": {
                "type": "boolean",
                "description": "Enable safe browsing for this client",
            },
            "parental_enabled": {
                "type": "boolean",
                "description": "Enable parental controls for this client",
            },
            "blocked_services": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of service IDs to block for this client",
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Tags to assign to this client",
            },
            "query": {
                "type": "string",
                "description": "IP, CIDR, or MAC to look up (required for find)",
            },
        },
        "required": ["action"],
    },
}

ADGUARD_REWRITE = {
    "name": "adguard_rewrite",
    "description": (
        "Manage DNS rewrite rules — custom DNS records that override upstream responses. "
        "Actions: 'list' to see all rewrites; 'add' to create a new rewrite; 'delete' to remove one. "
        "Use to point a domain to a specific IP (e.g. local dev server), "
        "or block a domain by rewriting it to 0.0.0.0."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list", "add", "delete"],
                "description": "Operation to perform",
            },
            "domain": {
                "type": "string",
                "description": "Domain name for the rewrite rule (required for add/delete). Wildcards supported: '*.example.com'",
            },
            "answer": {
                "type": "string",
                "description": "IP address or CNAME target (required for add). Use '0.0.0.0' to block.",
            },
        },
        "required": ["action"],
    },
}

ADGUARD_BLOCKED_SERVICES = {
    "name": "adguard_blocked_services",
    "description": (
        "Manage globally blocked services (social media, streaming, gaming, etc.). "
        "Actions: 'list' to see all available service IDs; "
        "'get' to see which services are currently blocked; "
        "'set' to update the list of blocked services (replaces current list)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list", "get", "set"],
                "description": "Operation to perform",
            },
            "services": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Service IDs to block (required for 'set'). Example: ['youtube', 'instagram', 'tiktok']",
            },
            "schedule": {
                "type": "object",
                "description": "Optional schedule for when blocking is active (for 'set')",
            },
        },
        "required": ["action"],
    },
}

ADGUARD_ACCESS = {
    "name": "adguard_access",
    "description": (
        "Manage AdGuard Home access control lists: who can use this DNS server. "
        "Actions: 'get' to see current allowed/blocked clients and blocked hosts; "
        "'set' to update the lists (replaces current). "
        "allowed_clients: IPs/CIDRs that are always allowed. "
        "disallowed_clients: IPs/CIDRs to block. "
        "blocked_hosts: additional domains to block for all clients."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["get", "set"],
                "description": "Operation to perform",
            },
            "allowed_clients": {
                "type": "array",
                "items": {"type": "string"},
                "description": "IPs or CIDRs to always allow (required for 'set')",
            },
            "disallowed_clients": {
                "type": "array",
                "items": {"type": "string"},
                "description": "IPs or CIDRs to block (required for 'set')",
            },
            "blocked_hosts": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Additional domains to block for all clients (required for 'set')",
            },
        },
        "required": ["action"],
    },
}

ADGUARD_CACHE_CLEAR = {
    "name": "adguard_cache_clear",
    "description": (
        "Clear the AdGuard Home DNS cache. Use after adding rules or rewrites "
        "so changes take effect immediately without waiting for TTL expiry."
    ),
    "parameters": {"type": "object", "properties": {}, "required": []},
}

ALL_SCHEMAS = [
    ADGUARD_STATUS,
    ADGUARD_PROTECTION,
    ADGUARD_STATS,
    ADGUARD_STATS_RESET,
    ADGUARD_QUERYLOG,
    ADGUARD_QUERYLOG_CLEAR,
    ADGUARD_FILTERING_STATUS,
    ADGUARD_FILTERING_ADD,
    ADGUARD_FILTERING_REMOVE,
    ADGUARD_FILTERING_REFRESH,
    ADGUARD_FILTERING_RULES,
    ADGUARD_FILTERING_CHECK,
    ADGUARD_CLIENTS,
    ADGUARD_REWRITE,
    ADGUARD_BLOCKED_SERVICES,
    ADGUARD_ACCESS,
    ADGUARD_CACHE_CLEAR,
]
