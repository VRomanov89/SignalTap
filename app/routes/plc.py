from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Any
import logging
from app.services.pylogix_service import PylogixService
from app.models.tag import (
    PLCConnectionConfig, 
    TagScanResponse, 
    PLCTag, 
    TagReadRequest, 
    TagReadResponse,
    Tag,
    TagReadRequest as TagReadRequestNew,
    TagReadResult
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Global service instance (in production, consider dependency injection)
plc_service = PylogixService()

@router.get("/scan", response_model=TagScanResponse)
async def scan_plc_tags(
    ip_address: str = Query(..., description="PLC IP address"),
    slot: int = Query(0, description="PLC processor slot"),
    timeout: int = Query(10, description="Connection timeout in seconds"),
    micro800: bool = Query(False, description="Whether this is a Micro800 PLC")
):
    """
    Scan and retrieve all tags from a PLC
    
    This endpoint connects to the specified PLC and returns all available tags
    with their names, types, and other metadata.
    """
    try:
        # Create connection config
        config = PLCConnectionConfig(
            ip_address=ip_address,
            slot=slot,
            timeout=timeout,
            micro800=micro800
        )
        
        # Connect to PLC
        if not plc_service.connect(config):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to PLC at {ip_address}"
            )
        
        # Get all tags
        tags = plc_service.get_all_tags()
        
        # Disconnect from PLC
        plc_service.disconnect()
        
        return TagScanResponse(
            success=True,
            tags=tags,
            total_count=len(tags),
            message=f"Successfully scanned {len(tags)} tags from PLC"
        )
        
    except Exception as e:
        logger.error(f"Error scanning PLC tags: {str(e)}")
        # Ensure we disconnect on error
        plc_service.disconnect()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning PLC tags: {str(e)}"
        )

@router.get("/scan-simple", response_model=List[Tag])
async def scan_plc_tags_simple(
    ip: str = Query(..., description="PLC IP address"),
    slot: int = Query(0, description="PLC processor slot")
):
    """
    Scan and retrieve all tags from a PLC (simplified version)
    
    This endpoint connects to the specified PLC and returns all available tags
    with their names and data types in a simple format.
    """
    try:
        # Get all tags using the simplified service method
        tags_data = plc_service.get_all_tags_simple(ip, slot)
        
        # Convert to Tag models
        tags = [Tag(name=tag["name"], type=tag["type"]) for tag in tags_data]
        
        return tags
        
    except Exception as e:
        logger.error(f"Error scanning PLC tags: {str(e)}")
        
        # Return HTTP 400 for connection failures
        if "Failed to connect" in str(e) or "unreachable" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail=f"PLC connection failed: {str(e)}"
            )
        
        # Return HTTP 500 for other errors
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning PLC tags: {str(e)}"
        )

@router.post("/read", response_model=TagReadResponse)
async def read_plc_tags(request: TagReadRequest):
    """
    Read specific tags from a PLC
    
    This endpoint connects to the specified PLC and reads the values of the
    requested tags.
    """
    try:
        # Create connection config
        config = PLCConnectionConfig(
            ip_address=request.ip_address,
            slot=request.slot,
            timeout=request.timeout
        )
        
        # Connect to PLC
        if not plc_service.connect(config):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to PLC at {request.ip_address}"
            )
        
        # Read tags
        values = plc_service.read_tags(request.tags)
        
        # Disconnect from PLC
        plc_service.disconnect()
        
        return TagReadResponse(
            success=True,
            values=values,
            message=f"Successfully read {len(request.tags)} tags from PLC"
        )
        
    except Exception as e:
        logger.error(f"Error reading PLC tags: {str(e)}")
        # Ensure we disconnect on error
        plc_service.disconnect()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error reading PLC tags: {str(e)}"
        )

@router.post("/read-tags", response_model=List[TagReadResult])
async def read_tags_live(request: TagReadRequestNew):
    """
    Read live values for a list of selected PLC tags
    
    This endpoint connects to the specified PLC and reads the current values
    of the requested tags, returning them with timestamps and status information.
    """
    try:
        # Read tags using the service method
        results_data = plc_service.read_tags(request.ip, request.tags, request.slot)
        
        # Convert to TagReadResult models
        results = []
        for result_data in results_data:
            value = result_data["value"]
            # If value is not a valid type, mark as 'Unreadable'
            if not isinstance(value, (str, int, float, bool)):
                value = "Unreadable"
            result = TagReadResult(
                name=result_data["name"],
                value=value,
                status=result_data["status"],
                timestamp=result_data["timestamp"]
            )
            results.append(result)
        
        return results
        
    except Exception as e:
        logger.error(f"Error reading tags: {str(e)}")
        
        # Return HTTP 400 for connection failures
        if "Failed to connect" in str(e) or "unreachable" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail=f"PLC connection failed: {str(e)}"
            )
        
        # Return HTTP 500 for other errors
        raise HTTPException(
            status_code=500,
            detail=f"Error reading tags: {str(e)}"
        )

@router.post("/write/{tag_name}")
async def write_plc_tag(
    tag_name: str,
    value: Any,
    ip_address: str = Query(..., description="PLC IP address"),
    slot: int = Query(0, description="PLC processor slot"),
    timeout: int = Query(10, description="Connection timeout in seconds")
):
    """
    Write a value to a specific tag in the PLC
    
    This endpoint connects to the specified PLC and writes the provided value
    to the specified tag.
    """
    try:
        # Create connection config
        config = PLCConnectionConfig(
            ip_address=ip_address,
            slot=slot,
            timeout=timeout
        )
        
        # Connect to PLC
        if not plc_service.connect(config):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to PLC at {ip_address}"
            )
        
        # Write to tag
        success = plc_service.write_tag(tag_name, value)
        
        # Disconnect from PLC
        plc_service.disconnect()
        
        if success:
            return {
                "success": True,
                "message": f"Successfully wrote {value} to tag {tag_name}"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to write to tag {tag_name}"
            )
        
    except Exception as e:
        logger.error(f"Error writing to PLC tag: {str(e)}")
        # Ensure we disconnect on error
        plc_service.disconnect()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error writing to PLC tag: {str(e)}"
        )

@router.get("/info")
async def get_plc_info(
    ip_address: str = Query(..., description="PLC IP address"),
    slot: int = Query(0, description="PLC processor slot"),
    timeout: int = Query(10, description="Connection timeout in seconds")
):
    """
    Get information about the PLC
    
    This endpoint connects to the specified PLC and returns device information
    such as device name, product name, revision, and serial number.
    """
    try:
        # Create connection config
        config = PLCConnectionConfig(
            ip_address=ip_address,
            slot=slot,
            timeout=timeout
        )
        
        # Connect to PLC
        if not plc_service.connect(config):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to PLC at {ip_address}"
            )
        
        # Get PLC info
        info = plc_service.get_plc_info()
        
        # Disconnect from PLC
        plc_service.disconnect()
        
        return {
            "success": True,
            "plc_info": info
        }
        
    except Exception as e:
        logger.error(f"Error getting PLC info: {str(e)}")
        # Ensure we disconnect on error
        plc_service.disconnect()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error getting PLC info: {str(e)}"
        )

@router.get("/test-connection")
async def test_plc_connection(
    ip_address: str = Query(..., description="PLC IP address"),
    slot: int = Query(0, description="PLC processor slot"),
    timeout: int = Query(10, description="Connection timeout in seconds")
):
    """
    Test connection to a PLC
    
    This endpoint tests the connection to the specified PLC without performing
    any operations.
    """
    try:
        # Create connection config
        config = PLCConnectionConfig(
            ip_address=ip_address,
            slot=slot,
            timeout=timeout
        )
        
        # Test connection
        success = plc_service.connect(config)
        
        # Disconnect from PLC
        plc_service.disconnect()
        
        if success:
            return {
                "success": True,
                "message": f"Successfully connected to PLC at {ip_address}"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to PLC at {ip_address}"
            )
        
    except Exception as e:
        logger.error(f"Error testing PLC connection: {str(e)}")
        # Ensure we disconnect on error
        plc_service.disconnect()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error testing PLC connection: {str(e)}"
        ) 