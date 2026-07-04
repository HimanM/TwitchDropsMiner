import unittest
import os
import io
from unittest.mock import patch

from tui import main as tui_main
from tui.cli import PortableCLIManager
from tui.manager import TUIManager


class TUIMainTests(unittest.TestCase):
    def test_frontend_factory_uses_portable_cli_on_windows_auto(self):
        with patch("tui.main.sys.platform", "win32"):
            self.assertIs(tui_main.frontend_factory("auto"), PortableCLIManager)

    def test_frontend_factory_uses_textual_on_linux_auto(self):
        with patch("tui.main.sys.platform", "linux"):
            self.assertIs(tui_main.frontend_factory("auto"), TUIManager)

    def test_frontend_factory_uses_portable_cli_on_wsl_auto(self):
        with patch("tui.main.sys.platform", "linux"), patch.dict(
            os.environ, {"WSL_INTEROP": "1"}, clear=False
        ):
            self.assertIs(tui_main.frontend_factory("auto"), PortableCLIManager)

    def test_frontend_factory_uses_portable_cli_on_termux_auto(self):
        with patch("tui.main.sys.platform", "linux"), patch.dict(
            os.environ, {"TERMUX_VERSION": "1"}, clear=False
        ):
            self.assertIs(tui_main.frontend_factory("auto"), PortableCLIManager)

    def test_frontend_factory_honors_explicit_frontend(self):
        self.assertIs(tui_main.frontend_factory("cli"), PortableCLIManager)
        self.assertIs(tui_main.frontend_factory("tui"), TUIManager)

    def test_main_reports_busy_lock(self):
        with patch("tui.main.lock_file", return_value=(False, None)), patch(
            "sys.stderr", new_callable=io.StringIO
        ) as stderr:
            self.assertEqual(tui_main.main(["cli"]), 3)

        self.assertIn("lock is busy", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
