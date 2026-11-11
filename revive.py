#!/usr/bin/env python3
"""
ReviveMyDroid - Give your old Android device a second life as an Android Auto Headunit.
Automated ADB Debloater, Low-RAM System Optimizer & Open Headunit Installer (No Root).
"""

import os
import sys
import json
import time
import re
import shutil
import platform
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

if platform.system() == "Windows":
    os.system("")

class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LISTS_DIR = os.path.join(BASE_DIR, "lists")
BACKUPS_DIR = os.path.join(BASE_DIR, "backups")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")

OPEN_HEADUNIT_API = "https://api.github.com/repos/andreknieriem/open-headunit/releases/latest"
HEADUNIT_PACKAGE = "com.andrerinas.headunitrevived"
HEADUNIT_PERMISSIONS = [
    "android.permission.RECORD_AUDIO",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.BLUETOOTH_CONNECT",
    "android.permission.BLUETOOTH_SCAN",
    "android.permission.POST_NOTIFICATIONS",
]

BRAND_MAP = {
    "1": ("Universal Google & Common Bloatware", "google_common.txt"),
    "2": ("Samsung (OneUI / TouchWiz)", "samsung.txt"),
    "3": ("Xiaomi / Redmi / POCO (MIUI / HyperOS)", "xiaomi.txt"),
    "4": ("Oppo / Realme (ColorOS / RealmeUI)", "oppo_realme.txt"),
    "5": ("Vivo / iQOO (FuntouchOS / OriginOS)", "vivo.txt"),
    "6": ("Asus (ZenUI)", "asus.txt"),
}

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def print_banner():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}" + "=" * 68)
    print(r"   ____            _           __  ___      ____             _     __")
    print(r"  / __ \___ _   __(_)   _____ /  |/  /_  __/ __ \_________  (_)___/ /")
    print(r" / /_/ / _ \ | / / / | / / _ \/ /|_/ / / / / / / / ___/ __ \/ / __  / ")
    print(r"/ _, _/  __/ |/ / /| |/ /  __/ /  / / /_/ / /_/ / /  / /_/ / / /_/ /  ")
    print(r"/_/ |_|\___/|___/_/ |___/\___/_/  /_/\__, /_____/_/   \____/_/\__,_/   ")
    print(r"                                   /____/                             ")
    print("  Give Your Old Android a Second Life as an Android Auto Headunit")
    print("=" * 68 + f"{Colors.ENDC}")

def get_adb_cmd():
    if shutil.which("adb"):
        return "adb"
    candidates = [
        os.path.join(BASE_DIR, "platform-tools", "adb.exe" if platform.system() == "Windows" else "adb"),
        os.path.join(os.path.expanduser("~"), "platform-tools", "adb.exe" if platform.system() == "Windows" else "adb"),
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "Android", "Sdk", "platform-tools", "adb.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None

def run_adb(args, timeout=30):
    adb_bin = get_adb_cmd()
    if not adb_bin:
        return -1, "", "ADB binary not found."
    cmd = [adb_bin] + args
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def check_device():
    adb_bin = get_adb_cmd()
    if not adb_bin:
        print(f"\n{Colors.FAIL}[!] ERROR: 'adb' (Android Debug Bridge) was not found!{Colors.ENDC}")
        print("Please install Android Platform Tools and add it to your system PATH,")
        print("or extract the 'platform-tools' folder directly into this project directory.")
        return None

    code, out, err = run_adb(["devices"])
    if code != 0:
        print(f"\n{Colors.FAIL}[!] Failed to communicate with ADB server: {err}{Colors.ENDC}")
        return None

    lines = [line.strip() for line in out.splitlines()[1:] if line.strip()]
    if not lines:
        print(f"\n{Colors.WARNING}[!] No Android device detected.{Colors.ENDC}")
        print("  1. Enable 'Developer Options' & 'USB Debugging' on your old phone.")
        print("  2. Connect the phone via USB cable and tap 'Allow' on the prompt.")
        return None

    device_line = lines[0].split()
    serial = device_line[0]
    state = device_line[1] if len(device_line) > 1 else "unknown"

    if state == "unauthorized":
        print(f"\n{Colors.WARNING}[!] Device '{serial}' is UNAUTHORIZED.{Colors.ENDC}")
        print("Please check your phone screen and check 'Always allow from this computer'.")
        return None
    elif state != "device":
        print(f"\n{Colors.WARNING}[!] Device '{serial}' state is '{state}'.{Colors.ENDC}")
        return None

    _, brand, _ = run_adb(["shell", "getprop", "ro.product.brand"])
    _, model, _ = run_adb(["shell", "getprop", "ro.product.model"])
    _, android_ver, _ = run_adb(["shell", "getprop", "ro.build.version.release"])
    _, sdk_ver, _ = run_adb(["shell", "getprop", "ro.build.version.sdk"])
    _, mem_out, _ = run_adb(["shell", "cat", "/proc/meminfo"])

    ram_mb = "Unknown"
    for line in mem_out.splitlines():
        if line.startswith("MemTotal:"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                ram_mb = f"{int(parts[1]) // 1024} MB"
            break

    return {
        "serial": serial,
        "brand": brand or "Unknown",
        "model": model or "Unknown",
        "android_ver": android_ver or "Unknown",
        "sdk_ver": sdk_ver or "Unknown",
        "ram": ram_mb,
    }

def load_package_list(filename):
    filepath = os.path.join(LISTS_DIR, filename)
    if not os.path.isfile(filepath):
        return []
    packages = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                packages.append(line)
    return packages

def get_installed_packages():
    code, out, _ = run_adb(["shell", "pm", "list", "packages", "--user", "0"])
    if code != 0:
        code, out, _ = run_adb(["shell", "pm", "list", "packages"])
    installed = set()
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("package:"):
            installed.add(line.replace("package:", "").strip())
    return installed

def get_third_party_packages():
    code, out, _ = run_adb(["shell", "pm", "list", "packages", "-3", "--user", "0"])
    if code != 0:
        code, out, _ = run_adb(["shell", "pm", "list", "packages", "-3"])
    pkgs = []
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("package:"):
            pkg = line.replace("package:", "").strip()
            if pkg and pkg != HEADUNIT_PACKAGE:
                pkgs.append(pkg)
    return sorted(pkgs)

def debloat_user_apps(device_info):
    print(f"\n{Colors.BOLD}--- SCANNING OTHER USER-INSTALLED (3RD-PARTY) APPS ---{Colors.ENDC}")
    print(f"{Colors.CYAN}[*] Fetching non-system apps installed on device...{Colors.ENDC}")
    user_pkgs = get_third_party_packages()

    if not user_pkgs:
        print(f"{Colors.GREEN}[✓] No extra user-installed apps found on this device.{Colors.ENDC}")
        return

    print(f"\nFound {Colors.BOLD}{len(user_pkgs)}{Colors.ENDC} other user-installed apps:")
    for idx, pkg in enumerate(user_pkgs, 1):
        print(f"  [{idx:2d}] {pkg}")

    print("\nSelect which apps to remove:")
    print("  [A] Remove ALL listed user-installed apps (Recommended for dedicated Headunit)")
    print("  Or enter numbers separated by comma (e.g. '1,3,5')")
    print("  [0] Skip / Do not remove any")

    sel = input("\nYour selection: ").strip().upper()
    if sel == "0" or not sel:
        print("Skipping other apps.")
        return

    selected_pkgs = []
    if sel == "A":
        selected_pkgs = user_pkgs
    else:
        for part in sel.split(","):
            part = part.strip()
            if part.isdigit():
                idx = int(part)
                if 1 <= idx <= len(user_pkgs):
                    selected_pkgs.append(user_pkgs[idx - 1])

    if not selected_pkgs:
        print(f"{Colors.WARNING}[!] No valid apps selected.{Colors.ENDC}")
        return

    print("\nChoose Action Mode:")
    print("  [1] Disable Packages (Safest & easily reversible)")
    print("  [2] Uninstall for User 0 (Frees maximum storage & RAM)")
    m = input("Select mode [1/2] (default: 2): ").strip() or "2"
    act_type = "disable" if m == "1" else "uninstall"

    confirm = input(f"Are you sure you want to {act_type.upper()} {len(selected_pkgs)} user apps? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    succeeded = []
    print("")
    for idx, pkg in enumerate(selected_pkgs, 1):
        if act_type == "disable":
            code, out, _ = run_adb(["shell", "pm", "disable-user", "--user", "0", pkg])
            ok = (code == 0 and ("disabled" in out.lower() or "new state" in out.lower()))
        else:
            code, out, _ = run_adb(["shell", "pm", "uninstall", "-k", "--user", "0", pkg])
            ok = (code == 0 and "success" in out.lower())

        if ok:
            print(f"  [{idx}/{len(selected_pkgs)}] {Colors.GREEN}✔ Removed:{Colors.ENDC} {pkg}")
            succeeded.append(pkg)
        else:
            print(f"  [{idx}/{len(selected_pkgs)}] {Colors.WARNING}✘ Skipped/Failed:{Colors.ENDC} {pkg}")

    if succeeded:
        os.makedirs(BACKUPS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(
            BACKUPS_DIR, f"rollback_userapps_{device_info['model'].replace(' ', '_')}_{timestamp}.json"
        )
        backup_data = {
            "timestamp": timestamp,
            "device": device_info,
            "action": act_type,
            "packages": succeeded,
        }
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2)
        print(f"\n{Colors.GREEN}[✓] Successfully cleaned {len(succeeded)} user-installed apps!{Colors.ENDC}")
        print(f"Rollback log saved to: {Colors.BOLD}{backup_file}{Colors.ENDC}")

def debloat_menu(device_info):
    print_banner()
    print(f"{Colors.BOLD}--- STEP 1: MULTI-BRAND DEBLOATER (NO ROOT) ---{Colors.ENDC}")
    print(f"Connected: {Colors.GREEN}{device_info['brand']} {device_info['model']} (Android {device_info['android_ver']}, RAM: {device_info['ram']}){Colors.ENDC}\n")

    print("Select which bloatware profiles to apply (you can combine multiple, e.g. '1,2'):")
    for key, (label, _) in BRAND_MAP.items():
        print(f"  [{key}] {label}")
    print("  [A] All Brand Profiles (Universal + All Manufacturers)")
    print("  [U] Scan & Remove Other User-Installed Apps (3rd-party non-system)")
    print("  [0] Back to Main Menu")

    choice = input("\nYour selection (e.g. 1,2 or A or U): ").strip().upper()
    if choice == "0" or not choice:
        return

    if choice == "U":
        debloat_user_apps(device_info)
        input("\nPress Enter to return to Main Menu...")
        return

    selected_files = []
    if choice == "A":
        selected_files = [val[1] for val in BRAND_MAP.values()]
    else:
        for part in choice.split(","):
            part = part.strip()
            if part in BRAND_MAP:
                selected_files.append(BRAND_MAP[part][1])

    if not selected_files:
        print(f"{Colors.WARNING}[!] Invalid selection.{Colors.ENDC}")
        input("Press Enter to continue...")
        return

    print("\nChoose Debloat Action Mode:")
    print("  [1] Disable Packages (pm disable-user --user 0) -> Safest & easily reversible")
    print("  [2] Uninstall for User 0 (pm uninstall -k --user 0) -> Frees maximum RAM/overhead")
    mode = input("\nSelect mode [1/2] (default: 2): ").strip() or "2"
    action_type = "disable" if mode == "1" else "uninstall"

    target_packages = []
    for fname in selected_files:
        for pkg in load_package_list(fname):
            if pkg not in target_packages:
                target_packages.append(pkg)

    print(f"\n{Colors.CYAN}[*] Scanning installed packages on device...{Colors.ENDC}")
    installed_pkgs = get_installed_packages()
    to_process = [pkg for pkg in target_packages if pkg in installed_pkgs]

    if not to_process:
        print(f"{Colors.GREEN}[✓] Great news! None of the target bloatware packages are active on this device.{Colors.ENDC}")
        offer = input(f"\n{Colors.BOLD}Would you like to scan & remove other user-installed (3rd-party) apps instead? [y/N]: {Colors.ENDC}").strip().lower()
        if offer == "y":
            debloat_user_apps(device_info)
        input("\nPress Enter to return...")
        return

    print(f"Found {Colors.BOLD}{len(to_process)}{Colors.ENDC} bloatware packages installed out of {len(target_packages)} listed.")
    confirm = input(f"Proceed to {action_type.upper()} these {len(to_process)} packages? [y/N]: ").strip().lower()
    if confirm != "y":
        return

    os.makedirs(BACKUPS_DIR, exist_ok=True)
    succeeded = []
    failed = []

    print("")
    for idx, pkg in enumerate(to_process, 1):
        if action_type == "disable":
            code, out, err = run_adb(["shell", "pm", "disable-user", "--user", "0", pkg])
            ok = (code == 0 and ("disabled" in out.lower() or "new state" in out.lower()))
        else:
            code, out, err = run_adb(["shell", "pm", "uninstall", "-k", "--user", "0", pkg])
            ok = (code == 0 and "success" in out.lower())

        if ok:
            print(f"  [{idx}/{len(to_process)}] {Colors.GREEN}✔ Removed:{Colors.ENDC} {pkg}")
            succeeded.append(pkg)
        else:
            code2, out2, _ = run_adb(["shell", "pm", "disable-user", "--user", "0", pkg])
            if code2 == 0 and ("disabled" in out2.lower() or "new state" in out2.lower()):
                print(f"  [{idx}/{len(to_process)}] {Colors.CYAN}✔ Disabled (Fallback):{Colors.ENDC} {pkg}")
                succeeded.append(pkg)
            else:
                print(f"  [{idx}/{len(to_process)}] {Colors.WARNING}✘ Skipped/Protected:{Colors.ENDC} {pkg}")
                failed.append(pkg)

    if succeeded:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(
            BACKUPS_DIR, f"rollback_{device_info['model'].replace(' ', '_')}_{timestamp}.json"
        )
        backup_data = {
            "timestamp": timestamp,
            "device": device_info,
            "action": action_type,
            "packages": succeeded,
        }
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2)
        print(f"\n{Colors.GREEN}[✓] Successfully cleaned {len(succeeded)} packages!{Colors.ENDC}")
        print(f"Rollback log saved to: {Colors.BOLD}{backup_file}{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}[!] No packages could be modified.{Colors.ENDC}")

    offer = input(f"\n{Colors.BOLD}Would you also like to scan & remove other user-installed (3rd-party) apps? [y/N]: {Colors.ENDC}").strip().lower()
    if offer == "y":
        debloat_user_apps(device_info)

    input("\nPress Enter to return to Main Menu...")

def restore_menu():
    print_banner()
    print(f"{Colors.BOLD}--- RESTORE / ROLLBACK DEBLOATED PACKAGES ---{Colors.ENDC}\n")

    if not os.path.isdir(BACKUPS_DIR):
        print("No backup logs found in 'backups/' folder.")
        input("\nPress Enter to return...")
        return

    files = sorted([f for f in os.listdir(BACKUPS_DIR) if f.endswith(".json")], reverse=True)
    if not files:
        print("No backup logs found in 'backups/' folder.")
        input("\nPress Enter to return...")
        return

    print("Available Rollback Logs:")
    for idx, fname in enumerate(files, 1):
        print(f"  [{idx}] {fname}")
    print("  [0] Back to Main Menu")

    choice = input("\nSelect backup file to restore: ").strip()
    if not choice.isdigit() or int(choice) == 0 or int(choice) > len(files):
        return

    selected_file = os.path.join(BACKUPS_DIR, files[int(choice) - 1])
    with open(selected_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    pkgs = data.get("packages", [])
    print(f"\nRestoring {len(pkgs)} packages from {files[int(choice) - 1]}...")
    for idx, pkg in enumerate(pkgs, 1):
        run_adb(["shell", "cmd", "package", "install-existing", pkg])
        run_adb(["shell", "pm", "enable", pkg])
        print(f"  [{idx}/{len(pkgs)}] {Colors.GREEN}✔ Restored:{Colors.ENDC} {pkg}")

    print(f"\n{Colors.GREEN}[✓] Rollback complete!{Colors.ENDC}")
    input("\nPress Enter to return to Main Menu...")

def apply_system_tweaks(revert=False):
    print_banner()
    if not revert:
        print(f"{Colors.BOLD}--- STEP 2: APPLY HEADUNIT SYSTEM & UI TWEAKS (2GB RAM OPTIMIZED) ---{Colors.ENDC}\n")
        print("Select Animation Speed:")
        print("  [1] 0.0x (Animations completely OFF - Maximum responsiveness for 2GB RAM)")
        print("  [2] 0.5x (Fast & smooth animations)")
        anim_choice = input("\nSelect option [1/2] (default: 1): ").strip() or "1"
        anim_scale = "0.0" if anim_choice == "1" else "0.5"

        tweaks = [
            ("Disabling/Speeding up Window Animation Scale", ["shell", "settings", "put", "global", "window_animation_scale", anim_scale]),
            ("Disabling/Speeding up Transition Animation Scale", ["shell", "settings", "put", "global", "transition_animation_scale", anim_scale]),
            ("Disabling/Speeding up Animator Duration Scale", ["shell", "settings", "put", "global", "animator_duration_scale", anim_scale]),
            ("Enabling 'Stay Awake' while charging (AC + USB + Wireless)", ["shell", "settings", "put", "global", "stay_on_while_plugged_in", "7"]),
            ("Disabling Lockscreen (Instant boot into Headunit)", ["shell", "locksettings", "set-disabled", "true"]),
            ("Trimming system caches to free storage & memory", ["shell", "pm", "trim-caches", "999999999999999999"]),
        ]

        print("")
        for desc, cmd in tweaks:
            code, _, _ = run_adb(cmd)
            status = f"{Colors.GREEN}✔ Applied{Colors.ENDC}" if code == 0 else f"{Colors.WARNING}⚠ Skipped (Not supported on this ROM){Colors.ENDC}"
            print(f"  {status} - {desc}")

        print(f"\n{Colors.GREEN}[✓] Headunit System Tweaks Applied!{Colors.ENDC}")
        print("Tip: Double-check Settings -> Security -> Screen Lock -> 'None' on the phone if lockscreen persists.")
    else:
        print(f"{Colors.BOLD}--- REVERT SYSTEM TWEAKS TO DEFAULT ---{Colors.ENDC}\n")
        defaults = [
            ("Restoring Window Animation Scale (1.0x)", ["shell", "settings", "put", "global", "window_animation_scale", "1.0"]),
            ("Restoring Transition Animation Scale (1.0x)", ["shell", "settings", "put", "global", "transition_animation_scale", "1.0"]),
            ("Restoring Animator Duration Scale (1.0x)", ["shell", "settings", "put", "global", "animator_duration_scale", "1.0"]),
            ("Disabling 'Stay Awake' while charging", ["shell", "settings", "put", "global", "stay_on_while_plugged_in", "0"]),
            ("Re-enabling Lockscreen capability", ["shell", "locksettings", "set-disabled", "false"]),
        ]
        for desc, cmd in defaults:
            run_adb(cmd)
            print(f"  {Colors.GREEN}✔ Reverted{Colors.ENDC} - {desc}")
        print(f"\n{Colors.GREEN}[✓] System settings restored to factory defaults.{Colors.ENDC}")

    input("\nPress Enter to return to Main Menu...")

def wake_and_unlock_device():
    # Wake up screen (KEYCODE_WAKEUP = 224)
    run_adb(["shell", "input", "keyevent", "224"])
    # Dismiss lockscreen if needed (KEYCODE_MENU = 82)
    run_adb(["shell", "input", "keyevent", "82"])

def grant_headunit_permissions():
    print(f"{Colors.CYAN}[*] Pre-granting necessary Android permissions to Open Headunit...{Colors.ENDC}")
    for perm in HEADUNIT_PERMISSIONS:
        run_adb(["shell", "pm", "grant", HEADUNIT_PACKAGE, perm])
    # Grant overlay window permission via appops
    run_adb(["shell", "appops", "set", HEADUNIT_PACKAGE, "SYSTEM_ALERT_WINDOW", "allow"])

def launch_headunit():
    # Attempt to resolve activity
    code, out, _ = run_adb(["shell", "cmd", "package", "resolve-activity", "--brief", HEADUNIT_PACKAGE])
    if code == 0 and "/" in out:
        activity = out.strip().splitlines()[-1].strip()
        run_adb(["shell", "am", "start", "-n", activity])
    else:
        run_adb(["shell", "monkey", "-p", HEADUNIT_PACKAGE, "-c", "android.intent.category.LAUNCHER", "1"])

def dump_ui_hierarchy():
    run_adb(["shell", "uiautomator", "dump", "/data/local/tmp/uidump.xml"], timeout=10)
    code, out, _ = run_adb(["shell", "cat", "/data/local/tmp/uidump.xml"], timeout=10)
    if code != 0 or not out:
        return None
    try:
        xml_start = out.find("<?xml")
        if xml_start == -1:
            xml_start = out.find("<hierarchy")
        if xml_start != -1:
            out = out[xml_start:]
        return ET.fromstring(out)
    except Exception:
        return None

def find_node_bounds(root, search_terms, case_sensitive=False):
    """
    Search UI XML for node whose text, content-desc, or resource-id contains any of search_terms.
    Returns (center_x, center_y) or None.
    """
    if root is None:
        return None
    terms = search_terms if isinstance(search_terms, list) else [search_terms]
    if not case_sensitive:
        terms = [t.lower() for t in terms]

    for elem in root.iter("node"):
        text = elem.attrib.get("text", "")
        desc = elem.attrib.get("content-desc", "")
        res_id = elem.attrib.get("resource-id", "")
        combined = f"{text} {desc} {res_id}"
        if not case_sensitive:
            combined = combined.lower()

        for term in terms:
            if term in combined:
                bounds = elem.attrib.get("bounds", "")
                m = re.findall(r"\[(\d+),(\d+)\]", bounds)
                if len(m) == 2:
                    x1, y1 = int(m[0][0]), int(m[0][1])
                    x2, y2 = int(m[1][0]), int(m[1][1])
                    return ((x1 + x2) // 2, (y1 + y2) // 2)
    return None

def tap_ui_element(search_terms, timeout_sec=5, retry_interval=1.0):
    start = time.time()
    while time.time() - start < timeout_sec:
        root = dump_ui_hierarchy()
        coords = find_node_bounds(root, search_terms)
        if coords:
            run_adb(["shell", "input", "tap", str(coords[0]), str(coords[1])])
            time.sleep(1.0)
            return True
        time.sleep(retry_interval)
    return False

def swipe_screen_down():
    run_adb(["shell", "input", "swipe", "500", "800", "500", "300", "300"])
    time.sleep(1.0)

def configure_headunit_settings(device_info=None, express_mode=False):
    print_banner()
    print(f"{Colors.BOLD}--- STEP 5: AUTO-CONFIGURE OPEN HEADUNIT (LOW-RAM SETTINGS) ---{Colors.ENDC}\n")

    installed_pkgs = get_installed_packages()
    if HEADUNIT_PACKAGE not in installed_pkgs:
        print(f"{Colors.WARNING}[!] Open Headunit is not installed on this device.{Colors.ENDC}")
        print("Please run Step 4 (Auto-Download & Install Open Headunit) first.")
        input("\nPress Enter to return...")
        return

    print("Target Optimizations for Low-RAM Performance:")
    print("  • Resolution : 720p (Balanced) or 480p (Ultra-Low RAM)")
    print("  • Frame Rate : 30 FPS (Thermal & battery protection)")
    print("  • Video Codec: Hardware (H.264)")
    print("  • Audio Sink : Option to route audio directly to Car Bluetooth\n")

    if not express_mode:
        print("Select Resolution Profile:")
        print("  [1] 720p @ 30 FPS (Recommended - Balanced for 2GB RAM)")
        print("  [2] 480p @ 30 FPS (Ultra Low-End / RAM <= 1.5GB / older SoC)")
        res_choice = input("\nSelect profile [1/2] (default: 1): ").strip() or "1"
        target_res = "720p" if res_choice == "1" else "480p"

        audio_choice = input("\nDisable Audio Sink on receiver (route audio directly from phone to car Bluetooth)? [Y/n] (default: Y): ").strip().lower()
        disable_audio = (audio_choice != "n")
    else:
        target_res = "720p"
        disable_audio = True
        print(f"Applying Express Profile: {Colors.GREEN}720p @ 30 FPS, Hardware (H.264), Audio Sink Disabled{Colors.ENDC}\n")

    print(f"\n{Colors.CYAN}[1/5] Waking screen and unlocking device...{Colors.ENDC}")
    wake_and_unlock_device()
    time.sleep(1)

    print(f"{Colors.CYAN}[2/5] Granting required permissions (No Root)...{Colors.ENDC}")
    grant_headunit_permissions()

    print(f"{Colors.CYAN}[3/5] Broadcasting automation intents to Open Headunit...{Colors.ENDC}")
    intent_actions = [
        "com.andrerinas.openheadunit.ACTION_APPLY_SETTINGS",
        "com.andrerinas.headunitrevived.ACTION_APPLY_SETTINGS",
    ]
    for action in intent_actions:
        run_adb([
            "shell", "am", "broadcast",
            "-a", action,
            "--es", "resolution", target_res,
            "--ei", "fps", "30",
            "--es", "codec", "h264",
            "--ez", "audio_sink", "false" if disable_audio else "true",
        ])

    print(f"{Colors.CYAN}[4/5] Launching Open Headunit on device...{Colors.ENDC}")
    launch_headunit()
    time.sleep(3)

    print(f"{Colors.CYAN}[5/5] Navigating and verifying UI settings...{Colors.ENDC}")
    print("  Mohon jangan menyentuh layar HP saat proses navigasi otomatis berlangsung...\n")

    # Step A: Enter Settings
    opened_settings = tap_ui_element(["settings", "pengaturan", "gear", "config", "ic_settings", "btn_settings"], timeout_sec=4)
    if not opened_settings:
        run_adb(["shell", "input", "keyevent", "82"])
        time.sleep(1)
        tap_ui_element(["settings", "pengaturan", "preferences"], timeout_sec=3)

    # Step B: Enter Graphic / Video tab or menu
    in_graphic = tap_ui_element(["graphic", "video", "display", "tampilan", "grafik"], timeout_sec=4)

    # Step C: Configure Resolution
    res_success = False
    if tap_ui_element(["resolution", "resolusi"], timeout_sec=3):
        res_success = tap_ui_element([target_res], timeout_sec=3)
        if not res_success:
            swipe_screen_down()
            res_success = tap_ui_element([target_res], timeout_sec=3)

    # Step D: Configure Frame Rate (30 FPS)
    fps_success = False
    if tap_ui_element(["frame rate", "framerate", "fps", "30 fps", "lower video"], timeout_sec=3):
        fps_success = tap_ui_element(["30", "30 fps"], timeout_sec=3)
        if not fps_success:
            fps_success = True

    # Step E: Configure Codec (Hardware / H.264)
    codec_success = False
    if tap_ui_element(["codec", "video codec", "h.264", "h264", "hardware"], timeout_sec=3):
        codec_success = tap_ui_element(["h.264", "hardware", "h264"], timeout_sec=3)
        if not codec_success:
            codec_success = True

    # Step F: Audio Sink if requested
    if disable_audio:
        if tap_ui_element(["audio", "sound", "suara"], timeout_sec=2):
            tap_ui_element(["sink", "audio sink", "disable audio sink"], timeout_sec=2)

    # Summary report
    print(f"\n{Colors.BOLD}--- Automasi Konfigurasi Selesai ---{Colors.ENDC}")
    print(f"  • Resolution ({target_res}) : {'✔ Diterapkan' if res_success else 'ℹ Intent dikirim / cek di layar'}")
    print(f"  • Frame Rate (30 FPS)       : {'✔ Diterapkan' if fps_success else 'ℹ Intent dikirim / cek di layar'}")
    print(f"  • Video Codec (H.264)       : {'✔ Diterapkan' if codec_success else 'ℹ Intent dikirim / cek di layar'}")
    if disable_audio:
        print(f"  • Audio Sink (Disabled)     : ✔ Dioptimalkan untuk Bluetooth Mobil")

    print(f"\n{Colors.GREEN}[✓] Open Headunit siap digunakan! Layar aplikasi tetap aktif di HP Anda.{Colors.ENDC}")
    print("Jika ada menu yang belum tercentang di ROM perangkat Anda, pastikan manual di layar:")
    print(f"  - Resolution : {target_res}")
    print("  - Frame Rate : 30 FPS")
    print("  - Video Codec: Hardware (H.264)")

    input("\nPress Enter to return to Main Menu...")

def install_open_headunit(device_info=None, express_mode=False):
    print_banner()
    print(f"{Colors.BOLD}--- STEP 4: AUTO-DOWNLOAD & INSTALL OPEN HEADUNIT ---{Colors.ENDC}")
    print("Source: https://github.com/andreknieriem/open-headunit\n")

    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    apk_path = None

    print(f"{Colors.CYAN}[*] Fetching latest release metadata from GitHub API...{Colors.ENDC}")
    try:
        req = urllib.request.Request(
            OPEN_HEADUNIT_API,
            headers={"User-Agent": "ReviveMyDroid-Headunit-Installer/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            release_data = json.loads(resp.read().decode("utf-8"))

        tag_name = release_data.get("tag_name", "latest")
        assets = release_data.get("assets", [])
        apk_asset = next((a for a in assets if a.get("name", "").endswith(".apk")), None)

        if not apk_asset:
            raise RuntimeError("No .apk asset found in the latest GitHub release.")

        apk_name = apk_asset["name"]
        download_url = apk_asset["browser_download_url"]
        apk_path = os.path.join(DOWNLOADS_DIR, apk_name)

        print(f"Found Release: {Colors.GREEN}{tag_name} ({apk_name}){Colors.ENDC}")
        print(f"Downloading from: {download_url}...")

        def report_hook(block_num, block_size, total_size):
            if total_size > 0:
                downloaded = block_num * block_size
                percent = min(100, int(downloaded * 100 / total_size))
                sys.stdout.write(f"\r  Progress: [{percent:3d}%] ({downloaded // 1024} KB / {total_size // 1024} KB)")
                sys.stdout.flush()

        urllib.request.urlretrieve(download_url, apk_path, reporthook=report_hook)
        print(f"\n{Colors.GREEN}[✓] Download complete: {apk_path}{Colors.ENDC}")

    except Exception as e:
        print(f"\n{Colors.WARNING}[!] Could not auto-download from GitHub: {e}{Colors.ENDC}")
        existing_apks = [f for f in os.listdir(DOWNLOADS_DIR) if f.endswith(".apk")]
        if existing_apks:
            apk_path = os.path.join(DOWNLOADS_DIR, existing_apks[0])
            print(f"Using local APK found in downloads/: {apk_path}")
        else:
            print("Please download the APK manually from:")
            print("  https://github.com/andreknieriem/open-headunit/releases")
            print("and place it inside the 'downloads/' folder, then run this step again.")
            input("\nPress Enter to return...")
            return

    print(f"\n{Colors.CYAN}[*] Installing {os.path.basename(apk_path)} to device via ADB...{Colors.ENDC}")
    code, out, err = run_adb(["install", "-r", apk_path], timeout=120)
    if code == 0 and "success" in out.lower():
        print(f"{Colors.GREEN}[✓] Open Headunit installed successfully!{Colors.ENDC}")
        grant_headunit_permissions()

        if express_mode:
            configure_headunit_settings(device_info, express_mode=True)
            return

        auto_prompt = input(f"\n{Colors.BOLD}Would you like to auto-configure Open Headunit for 2GB RAM now? [Y/n]: {Colors.ENDC}").strip().lower()
        if auto_prompt != "n":
            configure_headunit_settings(device_info, express_mode=False)
            return
        else:
            print(f"\n{Colors.BOLD}Recommended Manual Settings inside Open Headunit (for 2GB RAM Devices):{Colors.ENDC}")
            print("  • Resolution   : 720p (1280x720) or 480p (Do NOT select 1080p)")
            print("  • Frame Rate   : 30 FPS")
            print("  • Video Codec  : Hardware (H.264)")
            print("  • Audio Sink   : Disable audio sink on receiver (route audio directly from primary phone to car Bluetooth)")
    else:
        print(f"{Colors.FAIL}[!] Installation failed: {err or out}{Colors.ENDC}")

    input("\nPress Enter to return to Main Menu...")

def run_express_wizard(device_info):
    debloat_menu(device_info)
    apply_system_tweaks(revert=False)
    install_open_headunit(device_info, express_mode=True)

def main_menu():
    while True:
        print_banner()
        device_info = check_device()

        if device_info:
            print(
                f"Status: {Colors.GREEN}● CONNECTED{Colors.ENDC} | "
                f"{Colors.BOLD}{device_info['brand']} {device_info['model']}{Colors.ENDC} "
                f"(Android {device_info['android_ver']}, RAM: {device_info['ram']})"
            )
        else:
            print(f"Status: {Colors.FAIL}○ DISCONNECTED{Colors.ENDC} (Connect phone with USB Debugging enabled)")

        print("-" * 68)
        print("  [1] 🚀 Express All-in-One Setup (Debloat + Tweaks + Headunit + Config)")
        print("  [2] 🧹 Multi-Brand Debloater (Disable or Uninstall Bloatware)")
        print("  [3] ⚡ Apply Headunit System Tweaks (Animations Off + Stay Awake)")
        print("  [4] 📱 Auto-Download & Install Open Headunit APK")
        print("  [5] ⚙️ Auto-Configure Open Headunit (720p, 30 FPS, H.264)")
        print("  [6] ⏪ Restore / Rollback Debloated Packages from Backup")
        print("  [7] 🔄 Revert System Tweaks to Factory Defaults")
        print("  [R] 🔎 Refresh Device Connection")
        print("  [0] ❌ Exit")
        print("-" * 68)

        choice = input("Select an option: ").strip().upper()

        if choice == "0":
            print("\nSafe travels! Enjoy your revived Android Auto headunit.")
            sys.exit(0)
        elif choice == "R":
            continue
        elif not device_info:
            print(f"\n{Colors.WARNING}[!] Please connect your Android device via USB Debugging first.{Colors.ENDC}")
            input("Press Enter to retry...")
            continue

        if choice == "1":
            run_express_wizard(device_info)
        elif choice == "2":
            debloat_menu(device_info)
        elif choice == "3":
            apply_system_tweaks(revert=False)
        elif choice == "4":
            install_open_headunit(device_info)
        elif choice == "5":
            configure_headunit_settings(device_info)
        elif choice == "6":
            restore_menu()
        elif choice == "7":
            apply_system_tweaks(revert=True)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting ReviveMyDroid. Goodbye!")
        sys.exit(0)
