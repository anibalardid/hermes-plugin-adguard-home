# hermes-adguard-home-plugin

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) plugin to control a local [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) instance. Manage protection, filtering lists, custom rules, clients, DNS rewrites, query logs, statistics, and access control — all from natural language.

## Install

```bash
cd ~/.hermes/plugins
git clone https://github.com/your-org/hermes-adguard-home-plugin adguard-home
```

Restart Hermes — the plugin loads automatically. Verify with `/plugins`.

## Prerequisites

AdGuard Home must be installed and running locally before loading the plugin.

### Install AdGuard Home

**Automated install (Linux/macOS):**
```bash
curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v
```

**macOS via Homebrew:**
```bash
brew install adguard-home
sudo brew services start adguard-home
```

**Docker:**
```bash
docker run --name adguardhome \
  -p 53:53/tcp -p 53:53/udp \
  -p 3000:3000/tcp \
  -v /opt/adguardhome/work:/opt/adguardhome/work \
  -v /opt/adguardhome/conf:/opt/adguardhome/conf \
  --restart unless-stopped \
  adguard/adguardhome
```

**Manual download:**
Download from the [releases page](https://github.com/AdguardTeam/AdGuardHome/releases), then run:
```bash
./AdGuardHome -s install
```

After installing, complete the initial setup at `http://127.0.0.1:3000` in your browser.

## Configuration

The plugin connects to AdGuard Home via its REST API using environment variables.

| Variable | Default | Description |
|----------|---------|-------------|
| `ADGUARD_HOST` | `http://127.0.0.1:3000` | Base URL of your AdGuard Home instance |
| `ADGUARD_USER` | `admin` | Login username |
| `ADGUARD_PASSWORD` | _(empty)_ | Login password |

### Setting environment variables

Add to your shell profile (`~/.zshrc`, `~/.bashrc`):

```bash
export ADGUARD_HOST=http://127.0.0.1:3000
export ADGUARD_USER=admin
export ADGUARD_PASSWORD=your_password
```

Or in a Hermes `.env` file:

```env
ADGUARD_HOST=http://127.0.0.1:3000
ADGUARD_USER=admin
ADGUARD_PASSWORD=your_password
```

### Non-standard port or remote instance

```bash
export ADGUARD_HOST=http://192.168.1.1:8080   # router-hosted AdGuard Home
export ADGUARD_HOST=https://adguard.local      # HTTPS with custom domain
```

## Tools

| Tool | Description |
|------|-------------|
| `adguard_status` | Server status, protection state, DNS settings |
| `adguard_protection` | Enable/disable/pause protection |
| `adguard_stats` | DNS query statistics and top domains |
| `adguard_stats_reset` | Reset statistics to zero |
| `adguard_querylog` | Browse/search DNS query history |
| `adguard_querylog_clear` | Clear query log |
| `adguard_filtering_status` | List active filter lists and custom rules |
| `adguard_filtering_add` | Subscribe to a new filter list by URL |
| `adguard_filtering_remove` | Remove a filter list |
| `adguard_filtering_refresh` | Force-update all filter lists |
| `adguard_filtering_rules` | Set custom adblock-syntax rules |
| `adguard_filtering_check` | Check if a domain would be blocked |
| `adguard_clients` | List/add/update/delete/find clients |
| `adguard_rewrite` | Manage DNS rewrite rules |
| `adguard_blocked_services` | Block services (YouTube, TikTok, etc.) |
| `adguard_access` | Manage allowed/blocked client IPs |
| `adguard_cache_clear` | Clear DNS cache |

## Usage

Ask Hermes naturally:

```
is adguard running?
show me the top blocked domains from today
block tiktok and instagram for everyone
add this blocklist: https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt
why is example.com being blocked?
add a DNS rewrite for myapp.local -> 127.0.0.1
show me what 192.168.1.42 has been querying
pause ad blocking for 10 minutes
set up a client called "Kids TV" with YouTube and TikTok blocked
```

## File Structure

```
~/.hermes/plugins/adguard-home/
├── plugin.yaml     # Hermes plugin manifest
├── __init__.py     # register(ctx) — wires 17 tools + installs skill
├── schemas.py      # Tool schemas (what the LLM sees)
├── tools.py        # Handler implementations
├── client.py       # Thin HTTP client for the AdGuard Home REST API
├── skill.md        # Usage guide installed to ~/.hermes/skills/
└── README.md
```

## Troubleshooting

**`Cannot reach AdGuard Home`**
- Check AdGuard Home is running: open `http://127.0.0.1:3000` in your browser
- Verify `ADGUARD_HOST` matches the port AdGuard Home is listening on (default 3000 during setup, can be changed)
- On macOS with Homebrew: `brew services list | grep adguard`

**`HTTP 401: Unauthorized`**
- Set `ADGUARD_USER` and `ADGUARD_PASSWORD` to match your AdGuard Home credentials
- If you haven't set a password during setup, try leaving `ADGUARD_PASSWORD` empty

**`HTTP 403: Forbidden`**
- Your IP may be blocked by AdGuard Home's access control list
- Check `adguard_access(action="get")` or log into the web UI

**Port 53 already in use on macOS**
macOS has a built-in DNS resolver on port 53. AdGuard Home can use a different port or replace it:
```bash
sudo lsof -i :53   # see what's using port 53
```

## Requirements

- AdGuard Home running locally (or on your network)
- No additional Python dependencies (uses stdlib `urllib` only)

## License

MIT
