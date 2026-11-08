#!/bin/bash
# Jarvis on the Mac: a tiny local server at http://localhost:4180 that starts at login.
# Needed so Safari lets Jarvis talk to Ollama (Safari blocks that from the GitHub https page).
#
# Install:   curl -fsSL https://jannickspielt.github.io/jarvis/mac/install.sh | bash
# Uninstall: launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.jannick.jarvis-local.plist
#            rm -rf ~/Library/LaunchAgents/com.jannick.jarvis-local.plist "$HOME/Library/Application Support/Jarvis"
set -euo pipefail

DIR="$HOME/Library/Application Support/Jarvis"
PLIST="$HOME/Library/LaunchAgents/com.jannick.jarvis-local.plist"

mkdir -p "$DIR" "$HOME/Library/LaunchAgents"
curl -fsSL https://jannickspielt.github.io/jarvis/mac/jarvis-local.py -o "$DIR/jarvis-local.py"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.jannick.jarvis-local</string>
  <key>ProgramArguments</key>
  <array><string>/usr/bin/python3</string><string>$DIR/jarvis-local.py</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

for _ in $(seq 1 20); do curl -s -o /dev/null http://localhost:4180/ && break; sleep 0.5; done
open "http://localhost:4180"
echo "Fertig: Jarvis läuft unter http://localhost:4180 – in Safari jetzt Ablage › Zum Dock hinzufügen."
