import logging
from datetime import datetime
import os

LOG_DIR = "application_logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        filemode="w",
        level=logging.INFO,
        format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
    )

    # Add a rotating file handler (max log size of 1 MB, keep 3 backups)
    rotating_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE_PATH, maxBytes=1e6, backupCount=3
    )
    
    # Optionally set a formatter for the handler
    rotating_handler.setFormatter(logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s'))

    # Add the handler to the root logger
    logging.getLogger().addHandler(rotating_handler)


