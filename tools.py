import json

from . import client


# ---------------------------------------------------------------------------
# Status & Control
# ---------------------------------------------------------------------------

def adguard_status(args: dict, **kwargs) -> str:
    try:
        return json.dumps(client.get("/status"))
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_protection(args: dict, **kwargs) -> str:
    try:
        body: dict = {"enabled": args["enabled"]}
        duration = args.get("duration_ms")
        if duration is not None:
            body["duration"] = duration
        client.post("/protection", body)
        state = "enabled" if args["enabled"] else "disabled"
        return json.dumps({"ok": True, "protection": state})
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_cache_clear(args: dict, **kwargs) -> str:
    try:
        client.post("/cache_clear")
        return json.dumps({"ok": True})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def adguard_stats(args: dict, **kwargs) -> str:
    try:
        params = {}
        if args.get("recent_ms") is not None:
            params["recent"] = args["recent_ms"]
        return json.dumps(client.get("/stats", params or None))
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_stats_reset(args: dict, **kwargs) -> str:
    try:
        client.post("/stats_reset")
        return json.dumps({"ok": True})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Query Log
# ---------------------------------------------------------------------------

def adguard_querylog(args: dict, **kwargs) -> str:
    try:
        params = {
            "limit": args.get("limit", 100),
            "offset": args.get("offset"),
            "search": args.get("search"),
            "response_status": args.get("response_status"),
        }
        return json.dumps(client.get("/querylog", params))
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_querylog_clear(args: dict, **kwargs) -> str:
    try:
        client.post("/querylog_clear")
        return json.dumps({"ok": True})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def adguard_filtering_status(args: dict, **kwargs) -> str:
    try:
        return json.dumps(client.get("/filtering/status"))
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_filtering_add(args: dict, **kwargs) -> str:
    try:
        body = {
            "url": args["url"],
            "name": args["name"],
            "whitelist": args.get("whitelist", False),
        }
        client.post("/filtering/add_url", body)
        return json.dumps({"ok": True, "added": args["url"]})
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_filtering_remove(args: dict, **kwargs) -> str:
    try:
        body = {
            "url": args["url"],
            "whitelist": args.get("whitelist", False),
        }
        client.post("/filtering/remove_url", body)
        return json.dumps({"ok": True, "removed": args["url"]})
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_filtering_refresh(args: dict, **kwargs) -> str:
    try:
        body = {"whitelist": args.get("whitelist", False)}
        result = client.post("/filtering/refresh", body)
        return json.dumps({"ok": True, "updated": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_filtering_rules(args: dict, **kwargs) -> str:
    try:
        rules: list[str] = args["rules"]
        body = {"rules": rules}
        client.post("/filtering/set_rules", body)
        return json.dumps({"ok": True, "rules_count": len(rules)})
    except Exception as e:
        return json.dumps({"error": str(e)})


def adguard_filtering_check(args: dict, **kwargs) -> str:
    try:
        params = {"name": args["host"]}
        result = client.get("/filtering/check_host", params)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------

def adguard_clients(args: dict, **kwargs) -> str:
    try:
        action = args["action"]

        if action == "list":
            return json.dumps(client.get("/clients"))

        if action == "find":
            query = args.get("query")
            if not query:
                return json.dumps({"error": "query is required for find"})
            result = client.get("/clients/find", {"ip0": query})
            return json.dumps(result)

        if action == "add":
            if not args.get("name") or not args.get("ids"):
                return json.dumps({"error": "name and ids are required for add"})
            body = _build_client_body(args)
            client.post("/clients/add", body)
            return json.dumps({"ok": True, "added": args["name"]})

        if action == "update":
            if not args.get("name"):
                return json.dumps({"error": "name is required for update"})
            body = {"name": args["name"], "data": _build_client_body(args)}
            client.post("/clients/update", body)
            return json.dumps({"ok": True, "updated": args["name"]})

        if action == "delete":
            if not args.get("name"):
                return json.dumps({"error": "name is required for delete"})
            client.post("/clients/delete", {"name": args["name"]})
            return json.dumps({"ok": True, "deleted": args["name"]})

        return json.dumps({"error": f"Unknown action: {action}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def _build_client_body(args: dict) -> dict:
    body: dict = {"name": args["name"]}
    if args.get("ids"):
        body["ids"] = args["ids"]
    body["use_global_settings"] = args.get("use_global_settings", True)
    if args.get("filtering_enabled") is not None:
        body["filtering_enabled"] = args["filtering_enabled"]
    if args.get("safebrowsing_enabled") is not None:
        body["safebrowsing_enabled"] = args["safebrowsing_enabled"]
    if args.get("parental_enabled") is not None:
        body["parental_enabled"] = args["parental_enabled"]
    if args.get("blocked_services") is not None:
        body["blocked_services"] = args["blocked_services"]
    if args.get("tags") is not None:
        body["tags"] = args["tags"]
    return body


# ---------------------------------------------------------------------------
# DNS Rewrites
# ---------------------------------------------------------------------------

def adguard_rewrite(args: dict, **kwargs) -> str:
    try:
        action = args["action"]

        if action == "list":
            return json.dumps(client.get("/rewrite/list"))

        if action == "add":
            if not args.get("domain") or not args.get("answer"):
                return json.dumps({"error": "domain and answer are required for add"})
            body = {"domain": args["domain"], "answer": args["answer"]}
            client.post("/rewrite/add", body)
            return json.dumps({"ok": True, "added": f"{args['domain']} -> {args['answer']}"})

        if action == "delete":
            if not args.get("domain") or not args.get("answer"):
                return json.dumps({"error": "domain and answer are required for delete"})
            body = {"domain": args["domain"], "answer": args["answer"]}
            client.post("/rewrite/delete", body)
            return json.dumps({"ok": True, "deleted": args["domain"]})

        return json.dumps({"error": f"Unknown action: {action}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Blocked Services
# ---------------------------------------------------------------------------

def adguard_blocked_services(args: dict, **kwargs) -> str:
    try:
        action = args["action"]

        if action == "list":
            return json.dumps(client.get("/blocked_services/all"))

        if action == "get":
            return json.dumps(client.get("/blocked_services/get"))

        if action == "set":
            if args.get("services") is None:
                return json.dumps({"error": "services list is required for set"})
            body: dict = {"ids": args["services"]}
            if args.get("schedule"):
                body["schedule"] = args["schedule"]
            client.post("/blocked_services/update", body)
            return json.dumps({"ok": True, "blocked_services": args["services"]})

        return json.dumps({"error": f"Unknown action: {action}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Access Control
# ---------------------------------------------------------------------------

def adguard_access(args: dict, **kwargs) -> str:
    try:
        action = args["action"]

        if action == "get":
            return json.dumps(client.get("/access/list"))

        if action == "set":
            body = {
                "allowed_clients": args.get("allowed_clients", []),
                "disallowed_clients": args.get("disallowed_clients", []),
                "blocked_hosts": args.get("blocked_hosts", []),
            }
            client.post("/access/set", body)
            return json.dumps({"ok": True})

        return json.dumps({"error": f"Unknown action: {action}"})
    except Exception as e:
        return json.dumps({"error": str(e)})
