import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Generate dynamic filename based on date
log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%m-%d-%Y, %H-%M-%S')}.log")

# Configure logger
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)
