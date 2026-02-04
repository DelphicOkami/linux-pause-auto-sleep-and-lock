
# Manually block sleep and screen locking from commandline or a shortcut
<img src="doc/demo.png" alt="Battery and brightness showing sleep blocking enabled"></td>
# pause-auto-sleep

Manually block automatic suspend and screen locking from the command line or a keyboard shortcut.

![demo image](doc/demo.png)

**Quick summary:** the script uses the desktop/session power management D-Bus interface to request an idle inhibition so your screen and system won't auto-sleep while the inhibitor is active.

**Requirements**
- Python 3
- D-Bus Python bindings (package name varies by distro; e.g. `python3-dbus`)

## Installation

Clone or download this repository, then install the script into a directory on your PATH (example uses `~/.local/bin`):

```sh
mkdir -p ~/.local/bin
cp pause-auto-sleep ~/.local/bin/
chmod u+x ~/.local/bin/pause-auto-sleep
```

If you prefer, use `/usr/local/bin` or a system-wide location (requires sudo).

## Usage

1) With explicit application name and reason:

```sh
pause-auto-sleep "application_name_or_desktop.entry.name" "reason for inhibit"
```

Example (shows application icon/name in some desktop widgets):

```sh
pause-auto-sleep org.kde.konsole "SSH session"
```

To find desktop entry names try:

```sh
ls /usr/share/applications ~/.local/share/applications | grep -i YOUR_PROGRAM_NAME
```

2) Toggle mode (no arguments)

Run without arguments to toggle a manual inhibitor. Defaults:
- inhibitor: "User"
- reason: "Manually enabled"

Run it once to enable (it will run in foreground unless backgrounded). Run it again to release the inhibition.

Example (background):

```sh
pause-auto-sleep &
```

3) Release an existing inhibition

```sh
pause-auto-sleep --release
```

## Integrating with a shortcut or autostart

Use your desktop environment's custom shortcut settings and point the command to the installed path (for example `~/.local/bin/pause-auto-sleep`).

KDE Plasma: System Settings → Shortcuts → Add command...

GNOME: Settings → Keyboard → Custom Shortcuts → Add Shortcut

You can also create a `systemd --user` service to manage the inhibitor automatically. Example service (for reference only):

```ini
[Unit]
Description=Pause auto sleep when requested

[Service]
Type=simple
ExecStart=/home/YOUR_USERNAME/.local/bin/pause-auto-sleep org.kde.konsole "Service Enabled"
Restart=on-failure

[Install]
WantedBy=default.target
```

## Troubleshooting
- If you see D-Bus errors, ensure your session D-Bus is available and `python3-dbus` is installed.
- If icons do not appear in Plasma widgets, use the desktop entry name rather than a human-readable app name.

## Credits & Resources
- Idle Inhibition Service Draft: https://people.freedesktop.org/~hadess/idle-inhibition-spec/index.html
- Based on `gnome-inhibit` gist by @fxthomas: https://gist.github.com/fxthomas/9bdfadd972eaf7100b374042faac28c2

License: See the `LICENSE` file in this repository.

## Contributors

- **Luis Bocanegra** - original author and maintainer
- **Contributors & contributors list** - thank you to anyone who filed issues, suggested improvements, or contributed patches. If you'd like your name listed here, open a pull request or an issue and I'll add you.
  - **DelphicOkami** - Updated applet for use with KDE 6 
