import logging as lg
import os
from datetime import datetime


def get_current_time_stamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


# log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# log file name
LOG_FILE_NAME = f"log_{get_current_time_stamp()}.log"

# full path
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)


lg.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level=lg.INFO
)