import io
import logging
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

MPLCONFIGDIR = Path("/tmp") / "matplotlib"
MPLCONFIGDIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import utils


class MainLoggingTests(unittest.TestCase):
    def test_setup_logging_creates_log_file_and_writes_messages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_dir = Path(temp_dir) / "logs"
            log_file = log_dir / "main.log"

            with patch.object(utils, "LOG_DIR", log_dir):
                with patch.object(utils, "LOG_FILE", log_file):
                    with redirect_stdout(io.StringIO()):
                        logger = utils.setup_logging()
                        logger.info("unit test logging message")

                        for handler in logging.getLogger().handlers:
                            handler.flush()

            self.assertTrue(log_file.exists())
            self.assertIn(
                "unit test logging message",
                log_file.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
