from pydantic import BaseModel
from typing import Optional, List, Any, Union
from enum import Enum
from datetime import datetime

class TagDataType(str, Enum):
    """Enumeration of PLC tag data types"""
    BOOL = "BOOL"
    SINT = "SINT"
    INT = "INT"
    DINT = "DINT"
    LINT = "LINT"
    USINT = "USINT"
    UINT = "UINT"
    UDINT = "UDINT"
    ULINT = "ULINT"
    REAL = "REAL"
    LREAL = "LREAL"
    STRING = "STRING"
    ARRAY = "ARRAY"
    STRUCT = "STRUCT"
    UNKNOWN = "UNKNOWN"

class PLCTag(BaseModel):
    """Model for individual PLC tag information"""
    name: str
    tag_type: TagDataType
    description: Optional[str] = None
    value: Optional[Any] = None
    address: Optional[str] = None
    array_dimensions: Optional[List[int]] = None
    is_array: bool = False
    is_struct: bool = False

class PLCConnectionConfig(BaseModel):
    """Model for PLC connection configuration"""
    ip_address: str
    slot: int = 0
    timeout: int = 10
    micro800: bool = False

class TagScanResponse(BaseModel):
    """Model for tag scan response"""
    success: bool
    tags: List[PLCTag]
    total_count: int
    message: Optional[str] = None
    error: Optional[str] = None

class TagReadRequest(BaseModel):
    """Model for reading specific tags"""
    tags: List[str]
    ip_address: str
    slot: int = 0
    timeout: int = 10

class TagReadResponse(BaseModel):
    """Model for tag read response"""
    success: bool
    values: dict[str, Any]
    message: Optional[str] = None
    error: Optional[str] = None

class Tag(BaseModel):
    """Simple tag model for the simplified scan endpoint"""
    name: str
    type: str

class TagReadRequest(BaseModel):
    """Model for reading specific tags with live values"""
    ip: str
    slot: Optional[int] = 0
    tags: List[str]

class TagReadResult(BaseModel):
    """Model for individual tag read result"""
    name: str
    value: Union[str, int, float, bool, None]
    status: str
    timestamp: str 