import os
import sys
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]

os.environ.setdefault("MPLCONFIGDIR", str(Path("/tmp") / "matplotlib"))

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
