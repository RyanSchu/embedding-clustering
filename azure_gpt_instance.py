import os
import app_global as app_global
from openai import AzureOpenAI

class AzureGptClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AzureGptClient, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        azure_endpoint=app_global.SOCRATE_AZ_OPENAI_API_BASE_URL
        azure_api_version = "2024-04-01-preview"
        azure_api_key = app_global.SOCRATE_AZ_OPENAI_API_KEY
        self.azure_gpt_client = AzureOpenAI(
            api_key=azure_api_key,  
            api_version=azure_api_version,
            azure_endpoint=azure_endpoint
        )
        print('=======gpt_init==azure_endpoint:', self.azure_gpt_client)
    
    def get_azure_gpt_client(self):
        return self.azure_gpt_client

def getAzureGptClient():
    return AzureGptClient()

