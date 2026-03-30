---
name: adguard-home-plugin
description: Guide for using the AdGuard Home plugin — protection control, filtering, clients, query logs, DNS rewrites, and statistics
version: 1.0.0
metadata:
  hermes:
    tags: [adguard, dns, blocking, filtering, network]
    category: network
---

# AdGuard Home Plugin Usage Guide

You have 17 tools to control a local AdGuard Home instance. Always use `adguard_status` first to confirm the server is reachable.

## Tool Selection

**"Is AdGuard running? / what's the status?"** → `adguard_status`
**"Turn on/off blocking / pause AdGuard"** → `adguard_protection`
**"Show me stats / how many queries were blocked?"** → `adguard_stats`
**"Reset statistics"** → `adguard_stats_reset`
**"Show recent DNS queries / what did [client] query?"** → `adguard_querylog`
**"Clear the query log"** → `adguard_querylog_clear`
**"What filter lists are active?"** → `adguard_filtering_status`
**"Add a blocklist / subscribe to a filter list"** → `adguard_filtering_add`
**"Remove a filter list"** → `adguard_filtering_remove`
**"Update / refresh filter lists"** → `adguard_filtering_refresh`
**"Add a custom rule / block this domain / whitelist this site"** → `adguard_filtering_rules`
**"Would [domain] be blocked?"** → `adguard_filtering_check`
**"List/add/remove clients"** → `adguard_clients`
**"Add a DNS rewrite / point domain to IP"** → `adguard_rewrite`
**"Block YouTube / Instagram / TikTok"** → `adguard_blocked_services`
**"Who can use this DNS server?"** → `adguard_access`
**"Clear DNS cache"** → `adguard_cache_clear`

## IMPORTANT: Only these 17 tools exist

`adguard_status`, `adguard_protection`, `adguard_stats`, `adguard_stats_reset`,
`adguard_querylog`, `adguard_querylog_clear`, `adguard_filtering_status`,
`adguard_filtering_add`, `adguard_filtering_remove`, `adguard_filtering_refresh`,
`adguard_filtering_rules`, `adguard_filtering_check`, `adguard_clients`,
`adguard_rewrite`, `adguard_blocked_services`, `adguard_access`, `adguard_cache_clear`

Do NOT try to call any other tool names.

## Rules

1. **Check status first.** Use `adguard_status` before any other operation to confirm the server is reachable and see the current state.
2. **Clear cache after rule changes.** After adding/removing filter rules, rewrites, or blocklists, call `adguard_cache_clear` so changes take effect immediately.
3. **Custom rules are replace-not-append.** `adguard_filtering_rules` replaces ALL custom rules. To add one rule, first call `adguard_filtering_status` to get existing rules, then pass all existing rules plus the new one.
4. **Blocked services are global.** `adguard_blocked_services` with action='set' applies to all clients unless per-client overrides exist. Use `adguard_clients` to set per-client blocked services.
5. **Access lists are replace-not-append.** `adguard_access` with action='set' replaces all three lists. Always read first with action='get' before modifying.
6. **Filter by status for useful querylog results.** Use `response_status="blocked"` to see what's being blocked, or `search="192.168.1.x"` to debug a specific client.

## Common Workflows

### Check if a domain is blocked
```
adguard_filtering_check(host="ads.example.com")
```

### Block a domain with a custom rule
```
1. adguard_filtering_status()  ← get current custom rules
2. adguard_filtering_rules(rules=[...existing..., "||ads.example.com^"])
3. adguard_cache_clear()
```

### Whitelist a domain that's being blocked
```
adguard_filtering_rules(rules=[...existing..., "@@||safe.example.com^"])
adguard_cache_clear()
```

### Add a blocklist subscription
```
adguard_filtering_add(url="https://...", name="My Blocklist")
adguard_filtering_refresh()
```

### Pause protection for 5 minutes
```
adguard_protection(enabled=false, duration_ms=300000)
```

### Set up a local dev domain
```
adguard_rewrite(action="add", domain="myapp.local", answer="127.0.0.1")
adguard_cache_clear()
```

### See what a client has been querying
```
adguard_querylog(search="192.168.1.42", limit=50)
```

### Block social media globally
```
adguard_blocked_services(action="set", services=["youtube", "instagram", "tiktok", "facebook"])
```

### Find available service IDs to block
```
adguard_blocked_services(action="list")
```

## Custom Rule Syntax

| Rule | Effect |
|------|--------|
| `\|\|example.com^` | Block example.com and all subdomains |
| `@@\|\|example.com^` | Allow/whitelist (override block) |
| `\|\|ads.example.com^` | Block specific subdomain only |
| `0.0.0.0 example.com` | Hosts-file style block |
| `! comment` | Comment line |

## adguard_clients Examples

```
# List all clients
adguard_clients(action="list")

# Add a client
adguard_clients(action="add", name="My Phone", ids=["192.168.1.10"])

# Block specific services per client
adguard_clients(action="add", name="Kids TV", ids=["192.168.1.20"],
  use_global_settings=false, blocked_services=["youtube", "tiktok"])

# Find client by IP
adguard_clients(action="find", query="192.168.1.42")
```
