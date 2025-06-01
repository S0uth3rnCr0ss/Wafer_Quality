# # Basically used to log messages on the console
# # Eg: user A connected, app has started successfully

# import logging 
# import os
# from datetime import datetime

# LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)

# os.makedirs(logs_path, exist_ok = True)

# LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)
 
# logging.basicConfig(
#     filename=logs_path,
#     format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
#     level = logging.INFO
# )



import logging 
import os
from datetime import datetime

# Create a logs directory
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Define the log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging to both file and console (optional)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
