import os
from dotenv import load_dotenv
load_dotenv(override=True)

from scrt_keyvault import getAzureKeyVaultInstance


JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
USERNAME = os.environ.get('SQL_USERNAME')
USERPASS_KEYVAULT_KEY = os.environ.get('SQL_USERPASS_KEYVAULT_KEY')
DATABASE_HOST = os.environ.get('SQL_DATABASE_HOST')
DBNAME = os.environ.get('SQL_DBNAME')
CONN_NAME = os.environ.get('SQL_CONN_NAME')
DB_PASSWORD = getAzureKeyVaultInstance().get_db_password_url()
DB_ENCRYPTION_KEY = getAzureKeyVaultInstance().get_db_encryption_key()
SOCRATE_AZ_OPENAI_API_BASE_URL = getAzureKeyVaultInstance().get_az_gpt_url()
SOCRATE_AZ_OPENAI_API_KEY = getAzureKeyVaultInstance().get_az_gpt_key()
SYSTEM_PROMPT = os.environ.get('System_Prompt_day4')
WEB_REQUEST_UUID_SPLIT = '---'
GPT_MODEL='text-embedding-3-small-2025-03-18'
AZ_BLOB_STORAGE_KEY = getAzureKeyVaultInstance().get_blob_access_key()
STORAGE_ACCOUNT_URL = os.environ.get('storage_account_url')
CONTAINER_NAME = os.environ.get('blob_container')
