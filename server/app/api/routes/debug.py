from fastapi import APIRouter, HTTPException
from app.services.data_service import get_data_service
from app.core.vibe_engine import get_vibe_engine
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/debug/data-status")
async def check_data_status():
    """
    Debug endpoint to check if climate data is properly downloaded and accessible.
    """
    try:
        # Check if data directory exists
        data_path = os.getenv("DATA_PATH", "/app/data")
        data_dir = Path(data_path)
        
        debug_info = {
            "data_path": data_path,
            "data_directory_exists": data_dir.exists(),
            "data_directory_is_dir": data_dir.is_dir() if data_dir.exists() else False,
            "data_directory_contents": [],
            "azure_storage_connected": False,
            "data_service_status": "unknown",
            "vibe_engine_status": "unknown",
            "sample_data_available": False
        }
        
        # List contents of data directory
        if data_dir.exists():
            try:
                contents = list(data_dir.iterdir())
                debug_info["data_directory_contents"] = [str(item.name) for item in contents]
            except Exception as e:
                debug_info["data_directory_contents"] = [f"Error listing contents: {str(e)}"]
        
        # Check if outputs directory exists (where the actual data should be)
        outputs_dir = data_dir / "outputs"
        debug_info["outputs_directory_exists"] = outputs_dir.exists()
        if outputs_dir.exists():
            try:
                outputs_contents = list(outputs_dir.iterdir())
                debug_info["outputs_directory_contents"] = [str(item.name) for item in outputs_contents]
            except Exception as e:
                debug_info["outputs_directory_contents"] = [f"Error listing outputs: {str(e)}"]
        
        # Check Azure storage connection
        try:
            from app.services.azure_storage import AzureDataService
            azure_service = AzureDataService(
                account_name=os.getenv("AZURE_STORAGE_ACCOUNT", "weathervibesdata"),
                container_name=os.getenv("AZURE_STORAGE_CONTAINER", "climate-data")
            )
            debug_info["azure_storage_connected"] = True
        except Exception as e:
            debug_info["azure_storage_error"] = str(e)
        
        # Check data service
        try:
            data_service = get_data_service()
            debug_info["data_service_status"] = "initialized"
            debug_info["data_service_locations_count"] = len(data_service.locations_cache) if hasattr(data_service, 'locations_cache') else 0
        except Exception as e:
            debug_info["data_service_error"] = str(e)
        
        # Check vibe engine
        try:
            vibe_engine = get_vibe_engine()
            debug_info["vibe_engine_status"] = "initialized"
            debug_info["vibes_count"] = len(vibe_engine.vibes) if hasattr(vibe_engine, 'vibes') else 0
        except Exception as e:
            debug_info["vibe_engine_error"] = str(e)
        
        # Try to get sample data
        try:
            data_service = get_data_service()
            if hasattr(data_service, 'locations_cache') and data_service.locations_cache:
                # Get first available location
                first_location = list(data_service.locations_cache.keys())[0]
                debug_info["sample_location"] = first_location
                debug_info["sample_data_available"] = True
            else:
                debug_info["sample_data_available"] = False
        except Exception as e:
            debug_info["sample_data_error"] = str(e)
        
        return debug_info
        
    except Exception as e:
        logger.error(f"Debug endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Debug check failed: {str(e)}")


@router.get("/debug/test-data-download")
async def test_data_download():
    """
    Test endpoint to manually trigger data download from Azure Blob Storage.
    """
    try:
        from app.services.azure_storage import AzureDataService
        
        azure_service = AzureDataService(
            account_name=os.getenv("AZURE_STORAGE_ACCOUNT", "weathervibesdata"),
            container_name=os.getenv("AZURE_STORAGE_CONTAINER", "climate-data")
        )
        
        data_path = os.getenv("DATA_PATH", "/app/data")
        azure_service.download_data(data_path)
        
        return {
            "status": "success",
            "message": "Data download completed",
            "data_path": data_path
        }
        
    except Exception as e:
        logger.error(f"Data download test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data download failed: {str(e)}")


@router.get("/version")
async def get_version():
    """
    Simple version endpoint to check if the latest code is deployed.
    """
    return {
        "version": "2.0.0-debug",
        "message": "Debug version with data status endpoints",
        "timestamp": "2025-10-05T14:00:00Z"
    }


@router.get("/debug/create-data-dir")
async def create_data_directory():
    """
    Test endpoint to manually create the data directory.
    """
    try:
        import os
        from pathlib import Path
        
        data_path = os.getenv("DATA_PATH", "/app/data")
        
        # Try to create the directory
        Path(data_path).mkdir(parents=True, exist_ok=True)
        
        # Check if it exists now
        exists = Path(data_path).exists()
        is_dir = Path(data_path).is_dir()
        
        return {
            "status": "success",
            "data_path": data_path,
            "exists": exists,
            "is_dir": is_dir,
            "message": "Data directory creation attempted"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "data_path": data_path
        }
