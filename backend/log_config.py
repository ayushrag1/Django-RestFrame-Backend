"""
This utility is used to configure the logging for the application.
This contains different loggers for different modules and an email handler
to send emails when an error occurs.
"""

import datetime
# Logging Utilities
import logging
import logging.handlers
# General Utilities
import os
from logging.handlers import RotatingFileHandler

# from django_ses import SESBackend
from pytz import timezone

from backend.settings import BASE_DIR

# Log File:
LOG_FILE = os.path.join(
    BASE_DIR,
    'logs',
    'default-backend.log',
)


def log_file_exist(file_path):
    """
    Checks if the file exists if not
    creates the file.
    """
    try:
        logs_folder_path = f"{BASE_DIR}/logs"
        os.makedirs(logs_folder_path, exist_ok=True)
        if not os.path.exists(file_path):
            open(file_path, 'a', encoding='utf-8').close()
        return True

    except Exception as e:
        print(e)
        return False


def adjust_TZ(*args):
    """
    This function is used to convert the timestamp to 'Asia/Kolkata' timezone.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    timestamp = timestamp.astimezone(timezone('Asia/Kolkata'))
    return timestamp.timetuple()


def get_logger(name, file=LOG_FILE, level=logging.INFO):
    """
    This function is used to get the logger for the application.

    Usage:
    >>> LOGGER = get_logger('authentication', <filename - optional>)
    >>>>>>>>> LOGGER.exception(
            'Message (subject of mail)',
            extra={'emails': [list_of_emails], 'debug_info': <extra data>}
        )
    """
    # create the logger
    logger = logging.getLogger(name)

    # set the logger level
    logger.setLevel(level)

    file = os.path.join(BASE_DIR, 'logs', file)

    log_file = log_file_exist(file)

    if not log_file:
        print('Log file not created')

    # create the formatter with 'Asia/Kolkata' timezone
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )

    # Add time converter for 'Asia/Kolkata' timezone
    formatter.converter = adjust_TZ

    rotation_handler = RotatingFileHandler(
        file,
        maxBytes=100 * 1024 * 1024,  # 100 MB
        backupCount=1,
        mode='a',
    )

    rotation_handler.setFormatter(formatter)
    logger.addHandler(rotation_handler)

    return logger
