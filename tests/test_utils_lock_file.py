from __future__ import annotations

import types
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.utils import lock_file


class LockFileTests(unittest.TestCase):
    def test_failure_closes_handle(self):
        fake_msvcrt = types.SimpleNamespace(
            LK_NBLCK=1,
            locking=lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("locked")),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "lock.file"
            with patch("core.utils.sys.platform", "win32"), patch.dict(
                "sys.modules", {"msvcrt": fake_msvcrt}
            ):
                success, handle = lock_file(path)

        self.assertFalse(success)
        self.assertTrue(handle.closed)


if __name__ == "__main__":
    unittest.main()
