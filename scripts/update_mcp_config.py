import json, shutil, os

config_path = r"C:\Users\manpr\.gemini\config\mcp_config.json"
backup_path = r"C:\Users\manpr\.gemini\config\mcp_config.json.bak"

with open(r"C:\Users\manpr\Documents\42 Kalidasa\scripts\janction_key.json", "r", encoding="utf-8") as f:
    key_data = json.load(f)
api_key = key_data["api_key"]

# Backup existing config
shutil.copy2(config_path, backup_path)
print(f"Backed up existing mcp_config.json to {backup_path}")

with open(config_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

if "mcpServers" not in cfg:
    cfg["mcpServers"] = {}

# Preserve existing servers
existing_servers = list(cfg["mcpServers"].keys())
print("Preserving existing servers:", existing_servers)

# Add janction-render
cfg["mcpServers"]["janction-render"] = {
    "url": "https://render.janction.jp/mcp",
    "headers": {
        "Authorization": f"Bearer {api_key}"
    }
}

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2)

print("Updated mcp_config.json with janction-render while preserving other servers!")

