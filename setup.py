import os

from dotenv import load_dotenv
load_dotenv()

def get_qb_databases_id():
	databases = {
		"COBRA": os.getenv("DB_ID_COBRA"),
		"LARI": os.getenv("DB_ID_LARI"),
		"DOMINION": os.getenv("DB_ID_DOMINION"),
		"ZENER": os.getenv("DB_ID_ZENER"),
		"INMOBILIARIO": os.getenv("DB_ID_INMOBILIARIO"),
		"HUAWEI": os.getenv("DB_ID_HUAWEI"),
		"EZENTIS": os.getenv("DB_ID_EZENTIS"),
		"CAMTELECOM": os.getenv("DB_ID_CAMTELECOM"),
	};
	return databases;

def get_qb_url():
	return os.getenv("QB_API_URL");


def get_base_file_url():
	return os.getenv("QB_FILE_URL")

def get_login_session_info():
	return {
		'action': 'login',
		'loginid': os.getenv("LOGIN_ID"),
		'password': os.getenv("LOGIN_PASSWORD")
	};

def get_login_url():
	return os.getenv("LOGIN_URL")