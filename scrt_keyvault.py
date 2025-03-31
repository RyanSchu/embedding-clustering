import os, urllib, ast
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class AzureKeyVaultSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AzureKeyVaultSingleton, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        keyVaultName = os.environ.get("AZ_KEY_VAULT_NAME")
        KVUri = f"https://{keyVaultName}.vault.azure.net"
        print("=======scrt_keyvault:keyVaultName", keyVaultName)
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        USERPASS_KEYVAULT_KEY = os.environ.get('SQL_USERPASS_KEYVAULT_KEY')
        retrieved_secret = client.get_secret(USERPASS_KEYVAULT_KEY)
        db_encryption_secret = client.get_secret('SOCRATE-SQL-DB-ENCRYPTION-KEY')
        self.DB_PASSWORD_ORI = retrieved_secret.value
        self.DB_PASSWORD = urllib.parse.quote_plus(self.DB_PASSWORD_ORI)
        self.DB_ENCRYPTION_KEY = ast.literal_eval(db_encryption_secret.value)
        #print("======scrt_keyvault: retrieved_secret:", retrieved_secret, self.DB_ENCRYPTION_KEY, self.DB_PASSWORD)
        self.SOCRATE_AZ_OPENAI_API_BASE_URL = client.get_secret('SOCRATE-AZ-OPENAI-API-BASE').value
        self.SOCRATE_AZ_OPENAI_API_KEY = client.get_secret('SOCRATE-AZ-OPENAI-API-KEY').value
        self.SOCRATE_OPENAI_API_ORG = client.get_secret('SOCRATE-OPENAI-ORG').value
        self.SOCRATE_OPENAI_API_KEY = client.get_secret('SOCRATE-OPENAI-ORG').value
        self.BLOB_ACCESS_KEY = client.get_secret('roadhomenonprodsa').value

    def get_db_password_ori(self):
        return self.DB_PASSWORD_ORI
    def get_db_password_url(self):
        return self.DB_PASSWORD
    def get_db_encryption_key(self):
        return self.DB_ENCRYPTION_KEY
    def get_az_gpt_url(self):
        return self.SOCRATE_AZ_OPENAI_API_BASE_URL
    def get_az_gpt_key(self):
        return self.SOCRATE_AZ_OPENAI_API_KEY
    def get_openai_gpt_url(self):
        return self.SOCRATE_OPENAI_API_ORG
    def get_openai_gpt_key(self):
        return self.SOCRATE_OPENAI_API_KEY
    def get_blob_access_key(self):
        return self.BLOB_ACCESS_KEY
    
def getAzureKeyVaultInstance():
    return AzureKeyVaultSingleton()