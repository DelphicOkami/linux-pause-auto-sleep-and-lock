
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
### pause-auto-sleep only
Clone or download this repository, then install the script into a directory on your PATH (example uses `~/.local/bin`):

```sh
mkdir -p ~/.local/bin
cp pause-auto-sleep ~/.local/bin/
chmod u+x ~/.local/bin/pause-auto-sleep
```

If you prefer, use `/usr/local/bin` or a system-wide location (requires sudo).

### Caffeine (tray) — KDE 6 GUI controller

This repository includes a small system tray application, "Caffeine", that
controls `pause-auto-sleep` from the KDE/Qt system tray. It ships as
`caffeine.py` and provides a wrapper `run-caffeine.sh` and a
desktop autostart entry in `desktop/caffeine-tray.desktop`.

```sh
# install the app files to a central user location (recommended)
mkdir -p ~/.local/share/caffeine
cp run-caffeine.sh ~/.local/share/caffeine/run-caffeine.sh
cp caffeine.py ~/.local/share/caffeine/caffeine.py
cp -r icons ~/.local/share/caffeine/icons
cp desktop/caffeine-tray.desktop ~/.local/share/caffeine/
chmod u+x ~/.local/share/caffeine/run-caffeine.sh

# Also install the `pause-auto-sleep` script so the tray app can control it.
# You can either place it alongside the other app files, or install it to
# a directory on your PATH such as `~/.local/bin`.
cp pause-auto-sleep ~/.local/share/caffeine/pause-auto-sleep
chmod u+x ~/.local/share/caffeine/pause-auto-sleep

# To make the icons available to the whole desktop (so `QIcon.fromTheme` finds them) install them into the hicolor icon theme:
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
ln -sf ~/.local/share/caffeine/icons/caffeine-on.svg ~/.local/share/icons/hicolor/scalable/apps/caffeine-on.svg
ln -sf ~/.local/share/caffeine/icons/caffeine-off.svg ~/.local/share/icons/hicolor/scalable/apps/caffeine-off.svg

# install the desktop file into the per-user applications directory, then enable autostart via a symlink
mkdir -p ~/.local/share/applications
cp ~/.local/share/caffeine/caffeine-tray.desktop ~/.local/share/applications/caffeine-tray.desktop


# create a symlink for autostart (desktop files in ~/.config/autostart that point into applications are preferred)
mkdir -p ~/.config/autostart
ln -sf ~/.local/share/applications/caffeine-tray.desktop ~/.config/autostart/caffeine-tray.desktop

# run the tray app via the installed wrapper
~/.local/share/caffeine/run-caffeine.sh
```

Customization:
- To set a custom application identifier and reason (displayed by the
  session UI), export `PAUSE_INHIBITOR` and `PAUSE_REASON` before
  launching the tray app. Example:

```sh
export PAUSE_INHIBITOR="org.kde.konsole"
export PAUSE_REASON="Watching a long task"
./run-caffeine.sh
```

Icons:
- Example SVG icons are provided in `icons/caffeine-on.svg` and
  `icons/caffeine-off.svg`. The tray app prefers these bundled SVGs but
  will fall back to the desktop theme icons if they are missing.
  

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
  - **DelphicOkami** - Updated applet for use with KDE 6 & added caffination
