import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from utils import handle_model_states


class UtilsTests(unittest.TestCase):
    def test_handle_model_states_saves_and_loads_named_model(self):
        model = {
            "name": "support-vector-classifier",
            "classes": [0, 1],
            "metadata": {"trained": True},
        }

        current_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)

                with redirect_stdout(io.StringIO()):
                    handle_model_states(model=model, name="svc_model", state="save")
                    loaded_model = handle_model_states(name="svc_model", state="load")
            finally:
                os.chdir(current_dir)

            self.assertEqual(loaded_model, model)
            self.assertTrue(Path(temp_dir, "model_states", "svc_model.pkl").exists())


if __name__ == "__main__":
    unittest.main()
