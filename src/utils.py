import pickle 
import os
import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "main.log"


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )

    return logging.getLogger(__name__)

def handle_model_states(model=None, name=None, state="save"):
    save_dir = "model_states"
    os.makedirs(save_dir, exist_ok=True) 
    if name == "logistic_model":
        model_path = os.path.join(save_dir, "logistic_model.pkl")
    elif name == "svc_model":
        model_path = os.path.join(save_dir, "svc_model.pkl")
    else:
        model_path = os.path.join(save_dir, "rf_model.pkl")

    if state == "save":
        try:
            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            print(f"Model saved successfully at: {model_path}")
        except (OSError, pickle.PickleError) as e:
            print(f"Error saving model: {e}")
    elif state == "load":
        try:
            with open(model_path, "rb") as f:
                loaded_model = pickle.load(f)
            print("Model loaded successfully.")
        except (OSError, pickle.PickleError) as e:
            print(f"Error loading model: {e}")
        return loaded_model
