# SignalTap - PLC Tag Management System

A FastAPI backend service for connecting to Rockwell Allen-Bradley CompactLogix PLCs using pylogix. SignalTap provides a modern REST API for scanning, reading, and writing PLC tags.

## 🚀 Features

- **PLC Tag Scanning**: Discover all available tags on a PLC
- **Tag Reading**: Read specific tag values in real-time
- **Tag Writing**: Write values to PLC tags
- **PLC Information**: Get device information and properties
- **Connection Testing**: Test PLC connectivity
- **Modern API**: RESTful API with automatic documentation
- **Type Safety**: Full Pydantic model validation
- **Error Handling**: Comprehensive error handling and logging

## 📋 Requirements

- Python 3.10+
- Network access to Rockwell Allen-Bradley CompactLogix PLCs
- pylogix library for PLC communication

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SignalTap
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Using the Run Script (Recommended)

```bash
# Make the script executable (Linux/macOS)
chmod +x run.sh

# Run the application
./run.sh
```

### Manual Start

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 API Endpoints

### 1. Scan PLC Tags
```
GET /api/v1/scan?ip_address={ip}&slot={slot}&timeout={timeout}&micro800={bool}
```

Scans and returns all available tags from the specified PLC.

**Parameters:**
- `ip_address` (required): PLC IP address
- `slot` (optional): PLC processor slot (default: 0)
- `timeout` (optional): Connection timeout in seconds (default: 10)
- `micro800` (optional): Whether this is a Micro800 PLC (default: false)

**Example Response:**
```json
{
  "success": true,
  "tags": [
    {
      "name": "Tag1",
      "tag_type": "DINT",
      "description": "Sample tag",
      "value": null,
      "address": "N7:0",
      "array_dimensions": null,
      "is_array": false,
      "is_struct": false
    }
  ],
  "total_count": 1,
  "message": "Successfully scanned 1 tags from PLC"
}
```

### 2. Read Specific Tags
```
POST /api/v1/read
```

Reads the values of specific tags from a PLC.

**Request Body:**
```json
{
  "tags": ["Tag1", "Tag2"],
  "ip_address": "192.168.1.100",
  "slot": 0,
  "timeout": 10
}
```

**Example Response:**
```json
{
  "success": true,
  "values": {
    "Tag1": 42,
    "Tag2": "Hello World"
  },
  "message": "Successfully read 2 tags from PLC"
}
```

### 3. Write to Tag
```
POST /api/v1/write/{tag_name}?ip_address={ip}&slot={slot}&timeout={timeout}
```

Writes a value to a specific tag.

**Parameters:**
- `tag_name` (path): Name of the tag to write to
- `value` (body): Value to write
- `ip_address` (query): PLC IP address
- `slot` (query): PLC processor slot
- `timeout` (query): Connection timeout

### 4. Get PLC Information
```
GET /api/v1/info?ip_address={ip}&slot={slot}&timeout={timeout}
```

Returns device information about the PLC.

### 5. Test Connection
```
GET /api/v1/test-connection?ip_address={ip}&slot={slot}&timeout={timeout}
```

Tests connectivity to a PLC without performing operations.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory for configuration:

```env
# PLC Default Settings
DEFAULT_PLC_TIMEOUT=10
DEFAULT_PLC_SLOT=0

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Logging
LOG_LEVEL=INFO
```

## 🏗️ Project Structure

```
SignalTap/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routes/
│   │   └── plc.py           # PLC-related API endpoints
│   ├── services/
│   │   └── pylogix_service.py # PLC communication service
│   └── models/
│       └── tag.py           # Pydantic models for data validation
├── requirements.txt         # Python dependencies
├── run.sh                  # Application runner script
├── README.md               # This file
└── .env                    # Environment variables (create this)
```

## 🧪 Testing

### Test PLC Connection

```bash
curl "http://localhost:8000/api/v1/test-connection?ip_address=192.168.1.100"
```

### Scan PLC Tags

```bash
curl "http://localhost:8000/api/v1/scan?ip_address=192.168.1.100"
```

### Read Specific Tags

```bash
curl -X POST "http://localhost:8000/api/v1/read" \
  -H "Content-Type: application/json" \
  -d '{
    "tags": ["Tag1", "Tag2"],
    "ip_address": "192.168.1.100"
  }'
```

## 🚀 Deployment

### Local Development

The application is configured for local development with auto-reload enabled.

### Production Deployment

For production deployment, consider:

1. **Docker**: Create a Dockerfile for containerized deployment
2. **Environment Variables**: Configure production settings via environment variables
3. **Reverse Proxy**: Use nginx or similar for production serving
4. **Process Manager**: Use systemd, supervisor, or PM2 for process management

### Example Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security Considerations

- Configure CORS properly for production
- Use environment variables for sensitive configuration
- Implement authentication if needed
- Validate all input parameters
- Use HTTPS in production

## 🐛 Troubleshooting

### Common Issues

1. **Connection Failed**: Check PLC IP address and network connectivity
2. **Permission Denied**: Ensure proper network access to PLC
3. **Import Errors**: Verify virtual environment is activated
4. **Port Already in Use**: Change port in uvicorn command

### Logs

The application logs to stdout. Check the console output for detailed error messages.

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support contact information here] 