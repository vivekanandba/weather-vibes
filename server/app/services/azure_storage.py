import os
import tempfile
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import logging

logger = logging.getLogger(__name__)

class AzureDataService:
    """Service for downloading climate data from Azure Blob Storage."""
    
    def __init__(self, account_name: str, container_name: str):
        self.account_name = account_name
        self.container_name = container_name
        
        # Use managed identity or connection string
        try:
            # Try managed identity first
            self.blob_service = BlobServiceClient(
                account_url=f"https://{account_name}.blob.core.windows.net",
                credential=DefaultAzureCredential()
            )
        except Exception:
            # Fallback to connection string
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if connection_string:
                self.blob_service = BlobServiceClient.from_connection_string(connection_string)
            else:
                raise Exception("No Azure storage credentials found")
    
    def download_data(self, local_path: str):
        """Download all data files from blob storage."""
        logger.info(f"Downloading data to {local_path}")
        
        # Create local directory
        Path(local_path).mkdir(parents=True, exist_ok=True)
        
        # List and download all blobs
        container_client = self.blob_service.get_container_client(self.container_name)
        
        for blob in container_client.list_blobs():
            # Create local file path
            local_file_path = Path(local_path) / blob.name
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download blob
            with open(local_file_path, "wb") as download_file:
                download_file.write(container_client.download_blob(blob.name).readall())
            
            logger.info(f"Downloaded {blob.name}")
        
        logger.info("Data download completed")
