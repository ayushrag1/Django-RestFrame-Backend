from backend.settings import BASE_DIR

TEAMS_MAIL_IDS = ["ayadav102301@gmail.com"]
MODULE_EXCEPTION_TO_EMAIL_MAPPING = {
    "backend": TEAMS_MAIL_IDS,
}

DATA_FOLDER_PATH = f"{BASE_DIR}/data"
