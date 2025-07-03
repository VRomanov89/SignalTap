from pylogix import PLC
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from app.models.tag import PLCTag, TagDataType, PLCConnectionConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PylogixService:
    """Service class for handling PLC operations using pylogix"""
    
    def __init__(self):
        self.plc = None
        self.connected = False
    
    def connect(self, config: PLCConnectionConfig) -> bool:
        """
        Connect to a PLC using the provided configuration
        
        Args:
            config: PLCConnectionConfig object with connection details
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.plc = PLC()
            self.plc.IPAddress = config.ip_address
            self.plc.ProcessorSlot = config.slot
            self.plc.Micro800 = config.micro800
            
            # Test connection
            response = self.plc.GetTagList()
            if response.Status == "Success":
                self.connected = True
                logger.info(f"Successfully connected to PLC at {config.ip_address}")
                return True
            else:
                logger.error(f"Failed to connect to PLC: {response.Status}")
                return False
                
        except Exception as e:
            logger.error(f"Error connecting to PLC: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from the PLC"""
        if self.plc:
            self.plc.Close()
            self.connected = False
            logger.info("Disconnected from PLC")
    
    def get_all_tags(self) -> List[PLCTag]:
        """
        Get all tags from the connected PLC
        
        Returns:
            List[PLCTag]: List of all PLC tags
        """
        if not self.connected or not self.plc:
            raise Exception("Not connected to PLC")
        
        try:
            response = self.plc.GetTagList()
            
            if response.Status != "Success":
                raise Exception(f"Failed to get tag list: {response.Status}")
            
            tags = []
            for tag_info in response.Value:
                # Convert pylogix tag info to our PLCTag model
                tag = PLCTag(
                    name=tag_info.TagName,
                    tag_type=self._map_tag_type(tag_info.DataType),
                    description=getattr(tag_info, 'Description', None),
                    address=getattr(tag_info, 'Address', None),
                    is_array=hasattr(tag_info, 'ArrayDimensions') and tag_info.ArrayDimensions is not None,
                    is_struct=tag_info.DataType == 'STRUCT'
                )
                
                # Handle array dimensions if present
                if hasattr(tag_info, 'ArrayDimensions') and tag_info.ArrayDimensions:
                    tag.array_dimensions = tag_info.ArrayDimensions
                
                tags.append(tag)
            
            logger.info(f"Retrieved {len(tags)} tags from PLC")
            return tags
            
        except Exception as e:
            logger.error(f"Error getting tags: {str(e)}")
            raise
    
    def read_tags(self, tag_names: List[str]) -> Dict[str, Any]:
        """
        Read specific tags from the PLC
        
        Args:
            tag_names: List of tag names to read
            
        Returns:
            Dict[str, Any]: Dictionary mapping tag names to their values
        """
        if not self.connected or not self.plc:
            raise Exception("Not connected to PLC")
        
        try:
            results = {}
            
            for tag_name in tag_names:
                response = self.plc.Read(tag_name)
                
                if response.Status == "Success":
                    results[tag_name] = response.Value
                else:
                    results[tag_name] = None
                    logger.warning(f"Failed to read tag {tag_name}: {response.Status}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error reading tags: {str(e)}")
            raise
    
    def write_tag(self, tag_name: str, value: Any) -> bool:
        """
        Write a value to a specific tag
        
        Args:
            tag_name: Name of the tag to write to
            value: Value to write
            
        Returns:
            bool: True if write successful, False otherwise
        """
        if not self.connected or not self.plc:
            raise Exception("Not connected to PLC")
        
        try:
            response = self.plc.Write(tag_name, value)
            
            if response.Status == "Success":
                logger.info(f"Successfully wrote {value} to tag {tag_name}")
                return True
            else:
                logger.error(f"Failed to write to tag {tag_name}: {response.Status}")
                return False
                
        except Exception as e:
            logger.error(f"Error writing to tag {tag_name}: {str(e)}")
            return False
    
    def _map_tag_type(self, pylogix_type: str) -> TagDataType:
        """
        Map pylogix data types to our TagDataType enum
        
        Args:
            pylogix_type: Data type string from pylogix
            
        Returns:
            TagDataType: Mapped tag data type
        """
        type_mapping = {
            'BOOL': TagDataType.BOOL,
            'SINT': TagDataType.SINT,
            'INT': TagDataType.INT,
            'DINT': TagDataType.DINT,
            'LINT': TagDataType.LINT,
            'USINT': TagDataType.USINT,
            'UINT': TagDataType.UINT,
            'UDINT': TagDataType.UDINT,
            'ULINT': TagDataType.ULINT,
            'REAL': TagDataType.REAL,
            'LREAL': TagDataType.LREAL,
            'STRING': TagDataType.STRING,
            'ARRAY': TagDataType.ARRAY,
            'STRUCT': TagDataType.STRUCT
        }
        
        return type_mapping.get(pylogix_type.upper(), TagDataType.UNKNOWN)
    
    def get_plc_info(self) -> Dict[str, Any]:
        """
        Get information about the connected PLC
        
        Returns:
            Dict[str, Any]: PLC information
        """
        if not self.connected or not self.plc:
            raise Exception("Not connected to PLC")
        
        try:
            # Get device properties
            response = self.plc.GetDeviceProperties()
            
            if response.Status == "Success":
                return {
                    "ip_address": self.plc.IPAddress,
                    "slot": self.plc.ProcessorSlot,
                    "device_name": getattr(response.Value, 'DeviceName', 'Unknown'),
                    "product_name": getattr(response.Value, 'ProductName', 'Unknown'),
                    "revision": getattr(response.Value, 'Revision', 'Unknown'),
                    "serial_number": getattr(response.Value, 'SerialNumber', 'Unknown')
                }
            else:
                return {
                    "ip_address": self.plc.IPAddress,
                    "slot": self.plc.ProcessorSlot,
                    "error": response.Status
                }
                
        except Exception as e:
            logger.error(f"Error getting PLC info: {str(e)}")
            return {
                "ip_address": self.plc.IPAddress if self.plc else None,
                "slot": self.plc.ProcessorSlot if self.plc else None,
                "error": str(e)
            }
    
    def get_all_tags_simple(self, ip: str, slot: int = 0) -> List[Dict[str, str]]:
        """
        Get all tags from a PLC and return them in a simple format
        
        Args:
            ip: PLC IP address
            slot: PLC processor slot (default: 0)
            
        Returns:
            List[Dict[str, str]]: List of tags with name and type
        """
        try:
            # Create connection config
            config = PLCConnectionConfig(
                ip_address=ip,
                slot=slot,
                timeout=10
            )
            
            # Connect to PLC
            if not self.connect(config):
                raise Exception(f"Failed to connect to PLC at {ip}")
            
            # Get all tags
            response = self.plc.GetTagList()
            
            if response.Status != "Success":
                raise Exception(f"Failed to get tag list: {response.Status}")
            
            tags = []
            for tag_info in response.Value:
                tag = {
                    "name": tag_info.TagName,
                    "type": tag_info.DataType
                }
                tags.append(tag)
            
            # Disconnect from PLC
            self.disconnect()
            
            logger.info(f"Retrieved {len(tags)} tags from PLC at {ip}")
            return tags
            
        except Exception as e:
            logger.error(f"Error getting tags from PLC at {ip}: {str(e)}")
            # Ensure we disconnect on error
            self.disconnect()
            raise
    
    def read_tags(self, ip: str, tags: List[str], slot: int = 0) -> List[Dict[str, Any]]:
        """
        Read live values for a list of tags from a PLC
        
        Args:
            ip: PLC IP address
            tags: List of tag names to read
            slot: PLC processor slot (default: 0)
            
        Returns:
            List[Dict[str, Any]]: List of tag read results with name, value, status, and timestamp
        """
        try:
            # Create connection config
            config = PLCConnectionConfig(
                ip_address=ip,
                slot=slot,
                timeout=10
            )
            
            # Connect to PLC
            if not self.connect(config):
                raise Exception(f"Failed to connect to PLC at {ip}")
            
            results = []
            timestamp = datetime.utcnow().isoformat()
            
            # Read each tag individually
            for tag_name in tags:
                try:
                    response = self.plc.Read(tag_name)
                    
                    if response.Status == "Success":
                        result = {
                            "name": tag_name,
                            "value": response.Value,
                            "status": "Success",
                            "timestamp": timestamp
                        }
                    else:
                        result = {
                            "name": tag_name,
                            "value": None,
                            "status": "Error",
                            "timestamp": timestamp
                        }
                        logger.warning(f"Failed to read tag {tag_name}: {response.Status}")
                    
                    results.append(result)
                    
                except Exception as e:
                    logger.error(f"Error reading tag {tag_name}: {str(e)}")
                    result = {
                        "name": tag_name,
                        "value": None,
                        "status": "Error",
                        "timestamp": timestamp
                    }
                    results.append(result)
            
            # Disconnect from PLC
            self.disconnect()
            
            logger.info(f"Read {len(results)} tags from PLC at {ip}")
            return results
            
        except Exception as e:
            logger.error(f"Error reading tags from PLC at {ip}: {str(e)}")
            # Ensure we disconnect on error
            self.disconnect()
            raise 