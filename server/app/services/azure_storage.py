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
        
        # Try connection string first (more reliable in containers)
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if connection_string:
            logger.info("Using Azure Storage connection string")
            self.blob_service = BlobServiceClient.from_connection_string(connection_string)
        else:
            # Fallback to managed identity
            try:
                logger.info("Trying Azure managed identity")
                self.blob_service = BlobServiceClient(
                    account_url=f"https://{account_name}.blob.core.windows.net",
                    credential=DefaultAzureCredential()
                )
            except Exception as e:
                logger.error(f"Azure managed identity failed: {e}")
                raise Exception("No Azure storage credentials found")
    
    def download_data(self, local_path: str):
        """Download all data files from blob storage."""
        logger.info(f"Downloading data to {local_path}")
        
        # Handle symlink case - create the target directory
        try:
            if Path(local_path).is_symlink():
                logger.info(f"Path {local_path} is a symlink, creating target directory...")
                # Get the symlink target
                target_path = Path(local_path).resolve()
                target_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created target directory: {target_path}")
            else:
                Path(local_path).mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            logger.info(f"Directory {local_path} already exists, continuing...")
        except Exception as e:
            logger.warning(f"Could not create directory {local_path}: {e}, continuing...")
        
        # List and download all blobs
        container_client = self.blob_service.get_container_client(self.container_name)
        
        blob_count = 0
        for blob in container_client.list_blobs():
            blob_count += 1
            # Create local file path
            local_file_path = Path(local_path) / blob.name
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download blob
            with open(local_file_path, "wb") as download_file:
                download_file.write(container_client.download_blob(blob.name).readall())
            
            logger.info(f"Downloaded {blob.name}")
        
        logger.info(f"Data download completed - {blob_count} files downloaded")
