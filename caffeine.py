#!/usr/bin/env python3
"""Caffeine tray controller for pause-auto-sleep

This small system-tray utility toggles `pause-auto-sleep` and shows a
different icon when the pause (idle inhibition) is active. The name
"Caffeine" is inspired by similar utilities that keep the system awake.

Dependencies: PySide6 or PyQt6 (Qt6), python3

Usage: run this file (optionally autostart it via KDE autostart/.desktop)
"""
import os
import sys
import stat
import shutil
import subprocess
import tempfile
import time

try:
    from PySide6 import QtWidgets, QtGui, QtCore
except Exception:
    try:
        from PyQt6 import QtWidgets, QtGui, QtCore
    except Exception:
        print("This tool requires PySide6 or PyQt6. Install one of them and try again.", file=sys.stderr)
        sys.exit(1)


def find_script() -> str | None:
    """Locate the `pause-auto-sleep` script in PATH or repository.

    Returns the absolute path to the script if found and executable,
    otherwise `None`.
    """
    name = 'pause-auto-sleep'
    path = shutil.which(name)
    if path:
        return path
    here = os.path.dirname(__file__)
    candidate = os.path.join(here, name)
    if os.path.exists(candidate) and os.access(candidate, os.X_OK):
        return candidate
    return None


def socket_path_for_script() -> str:
    """Return the UNIX socket path used by `pause-auto-sleep`.

    The path mirrors the script's own temporary socket naming scheme
    (`/tmp/<basename>-<uid>.socket`).
    """
    name = os.path.basename(find_script() or 'pause-auto-sleep')
    return os.path.join(tempfile.gettempdir(), f"{name}-{os.getuid()}.socket")


def is_paused() -> bool:
    """Detect whether the inhibitor is currently active.

    This checks for the presence of a UNIX socket file created by
    `pause-auto-sleep`. It is a best-effort check suitable for the
    tray app's UI state.
    """
    path = socket_path_for_script()
    try:
        st = os.stat(path)
        return stat.S_ISSOCK(st.st_mode)
    except FileNotFoundError:
        return False
    except Exception:
        return False


class CaffeineApp(QtWidgets.QApplication):
    """Qt application providing a system tray icon and menu.

    The app toggles the `pause-auto-sleep` script and updates the tray
    icon every second to reflect the current state.
    """
    def __init__(self, argv):
        super().__init__(argv)
        self.script = find_script()
        if not self.script:
            QtWidgets.QMessageBox.critical(None, 'Caffeine', 'Cannot find pause-auto-sleep script in PATH or repository.')
            sys.exit(1)

        self.tray = QtWidgets.QSystemTrayIcon()
        icon_dir = os.path.join(os.path.dirname(__file__), 'icons')
        icon_on_path = os.path.join(icon_dir, 'caffeine-on.svg')
        icon_off_path = os.path.join(icon_dir, 'caffeine-off.svg')
        if os.path.exists(icon_on_path):
            self.icon_on = QtGui.QIcon(icon_on_path)
        else:
            self.icon_on = QtGui.QIcon.fromTheme('media-playback-pause')
        if os.path.exists(icon_off_path):
            self.icon_off = QtGui.QIcon(icon_off_path)
        else:
            self.icon_off = QtGui.QIcon.fromTheme('media-playback-start')

        self.menu = QtWidgets.QMenu()
        self.action_toggle = self.menu.addAction('Toggle Caffeine')
        self.action_toggle.triggered.connect(self.toggle_pause)
        self.menu.addSeparator()
        quit_action = self.menu.addAction('Quit')
        quit_action.triggered.connect(self.quit)

        # Environment variables to override the default inhibitor/reason
        # (useful for desktop entries or wrapper scripts).
        self.default_inhibitor = os.environ.get('PAUSE_INHIBITOR', 'User')
        self.default_reason = os.environ.get('PAUSE_REASON', 'Manually enabled')

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.on_activated)
        self.tray.show()

        # Update icon periodically
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_icon)
        self.timer.start()
        self.update_icon()

        # Ensure the inhibitor is released on app quit
        self.aboutToQuit.connect(self.release_pause)

    def update_icon(self) -> None:
        """Set the tray icon and tooltip according to the pause state."""
        if is_paused():
            if not self.icon_on.isNull():
                self.tray.setIcon(self.icon_on)
            else:
                self.tray.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogYesButton))
            self.tray.setToolTip('Caffeine: Paused (auto-sleep inhibited)')
        else:
            if not self.icon_off.isNull():
                self.tray.setIcon(self.icon_off)
            else:
                self.tray.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogNoButton))
            self.tray.setToolTip('Caffeine: Active (auto-sleep enabled)')

    def on_activated(self, reason) -> None:
        """React to tray icon activation (left click toggles)."""
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_pause()

    def toggle_pause(self) -> None:
        """Toggle the pause state by launching or releasing `pause-auto-sleep`."""
        if is_paused():
            subprocess.run([self.script, '--release'])
            time.sleep(0.2)
        else:
            subprocess.Popen([self.script, self.default_inhibitor, self.default_reason], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)

    def release_pause(self) -> None:
        """Best-effort release of any active inhibitor when quitting."""
        try:
            if is_paused():
                subprocess.run([self.script, '--release'])
        except Exception:
            pass


def main() -> None:
    app = CaffeineApp(sys.argv)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
