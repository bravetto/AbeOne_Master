# S3 File Storage Integration

This document describes the S3 file storage integration for the CodeGuardians Gateway, which enables horizontal scaling by replacing local disk storage with cloud-based S3 storage.

## Overview

The application now uses AWS S3 for file storage instead of local disk storage. This change enables:

- **Horizontal Scaling**: Multiple replicas can access the same files
- **High Availability**: Files are stored in a highly available cloud service
- **Cost Efficiency**: No local disk storage costs
- **Security**: S3 provides better security than local files
- **Scalability**: Unlimited storage capacity

## Architecture

```
        
   Client App           FastAPI App          AWS S3        
                                                           
 1. Upload File   2. Generate      3. Store File   
                         Presigned                         
                         URL                               
 4. Upload to S3  3. Return URL                        
                                                           
 5. Get File      6. Generate      7. Return File  
                         Download URL                      
        
```

## Configuration

### Environment Variables

Add these environment variables to your `.env` file:

```bash
# S3 File Storage
S3_ENABLED=true
S3_BUCKET_NAME=your-bucket-name
S3_REGION=us-east-1
S3_ACCESS_KEY_ID=your-access-key
S3_SECRET_ACCESS_KEY=your-secret-key
S3_SESSION_TOKEN=your-session-token  # Optional
S3_ENDPOINT_URL=  # Optional, for local testing with MinIO

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES=image/jpeg,image/png,image/gif,application/pdf
UPLOAD_EXPIRY_MINUTES=60
FILE_CLEANUP_DAYS=30
```

### AWS Credentials

The application supports multiple ways to provide AWS credentials:

1. **Environment Variables** (for development):
   ```bash
   S3_ACCESS_KEY_ID=your-access-key
   S3_SECRET_ACCESS_KEY=your-secret-key
   ```

2. **IAM Roles** (recommended for production):
   - Attach an IAM role to your ECS task or EC2 instance
   - No need to provide credentials in environment variables

3. **AWS Secrets Manager** (for production):
   - Store credentials in AWS Secrets Manager
   - The application will automatically retrieve them

## API Endpoints

### File Upload

#### Direct Upload
```http
POST /api/v1/upload/direct
Content-Type: multipart/form-data

file: [binary file data]
```

**Response:**
```json
{
  "file_id": "uploads/2024/01/15/uuid-filename.ext",
  "filename": "example.jpg",
  "file_url": "https://bucket.s3.region.amazonaws.com/uploads/2024/01/15/uuid-filename.ext",
  "file_size": 1024,
  "content_type": "image/jpeg",
  "upload_timestamp": "2024-01-15T10:30:00Z",
  "etag": "abc123def456"
}
```

#### Presigned Upload URL
```http
POST /api/v1/upload/presigned
Content-Type: application/json

{
  "filename": "example.jpg",
  "content_type": "image/jpeg",
  "expires_in": 3600
}
```

**Response:**
```json
{
  "upload_url": "https://bucket.s3.region.amazonaws.com/uploads/2024/01/15/uuid-filename.ext?X-Amz-Algorithm=...",
  "file_url": "https://bucket.s3.region.amazonaws.com/uploads/2024/01/15/uuid-filename.ext",
  "file_id": "uploads/2024/01/15/uuid-filename.ext",
  "filename": "example.jpg",
  "expires_in": 3600,
  "expires_at": "2024-01-15T11:30:00Z"
}
```

### File Download

#### Direct Download
```http
GET /api/v1/upload/download/{file_id}
```

#### Presigned Download URL
```http
GET /api/v1/upload/download/{file_id}/url?expires_in=3600
```

**Response:**
```json
{
  "download_url": "https://bucket.s3.region.amazonaws.com/uploads/2024/01/15/uuid-filename.ext?X-Amz-Algorithm=...",
  "file_id": "uploads/2024/01/15/uuid-filename.ext",
  "expires_in": 3600
}
```

### File Management

#### Get File Metadata
```http
GET /api/v1/upload/metadata/{file_id}
```

#### Delete File
```http
DELETE /api/v1/upload/{file_id}
```

#### List Files
```http
GET /api/v1/upload/list?prefix=uploads&limit=100
```

### Health Check
```http
GET /api/v1/upload/health
```

## Usage Examples

### Python Client

```python
import requests
import json

# Upload file directly
with open('example.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/upload/direct', files=files)
    result = response.json()
    print(f"File uploaded: {result['file_url']}")

# Generate presigned upload URL
upload_data = {
    "filename": "example.jpg",
    "content_type": "image/jpeg"
}
response = requests.post('http://localhost:8000/api/v1/upload/presigned', json=upload_data)
result = response.json()

# Upload directly to S3 using presigned URL
with open('example.jpg', 'rb') as f:
    response = requests.put(result['upload_url'], data=f, headers={'Content-Type': 'image/jpeg'})
    print(f"File uploaded to S3: {result['file_url']}")
```

### JavaScript Client

```javascript
// Upload file directly
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/v1/upload/direct', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('File uploaded:', result.file_url);

// Generate presigned upload URL
const uploadData = {
  filename: 'example.jpg',
  content_type: 'image/jpeg'
};

const response = await fetch('/api/v1/upload/presigned', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(uploadData)
});

const result = await response.json();

// Upload directly to S3
const file = fileInput.files[0];
await fetch(result.upload_url, {
  method: 'PUT',
  body: file,
  headers: { 'Content-Type': 'image/jpeg' }
});

console.log('File uploaded to S3:', result.file_url);
```

## Testing

### Run Integration Tests

```bash
# Set up environment variables
export S3_ENABLED=true
export S3_BUCKET_NAME=your-test-bucket
export S3_REGION=us-east-1
export S3_ACCESS_KEY_ID=your-access-key
export S3_SECRET_ACCESS_KEY=your-secret-key

# Run the test script
python test_s3_integration.py
```

### Manual Testing

1. **Test Configuration:**
   ```bash
   curl http://localhost:8000/api/v1/upload/health
   ```

2. **Test Direct Upload:**
   ```bash
   curl -X POST -F "file=@test.jpg" http://localhost:8000/api/v1/upload/direct
   ```

3. **Test Presigned Upload:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"filename":"test.jpg","content_type":"image/jpeg"}' \
        http://localhost:8000/api/v1/upload/presigned
   ```

## Migration from Local Storage

If you're migrating from local file storage:

1. **Update Environment Variables:**
   - Add S3 configuration variables
   - Remove or comment out `UPLOAD_DIR` if it was used

2. **Update Client Code:**
   - Change upload endpoints from local paths to S3 URLs
   - Update file handling to work with S3 URLs

3. **Migrate Existing Files:**
   - Upload existing files to S3
   - Update database records with new S3 URLs

## Troubleshooting

### Common Issues

1. **S3 Not Enabled:**
   ```
   Error: S3 file storage is not enabled or not properly configured
   ```
   - Check that `S3_ENABLED=true`
   - Verify `S3_BUCKET_NAME` is set
   - Ensure `S3_REGION` is configured

2. **Access Denied:**
   ```
   Error: Access denied to S3 bucket
   ```
   - Check AWS credentials
   - Verify IAM permissions
   - Ensure bucket exists and is accessible

3. **File Too Large:**
   ```
   Error: File too large. Maximum size: 10485760 bytes
   ```
   - Increase `MAX_FILE_SIZE` in environment variables
   - Consider using presigned URLs for large files

4. **File Type Not Allowed:**
   ```
   Error: File type not allowed
   ```
   - Add the file type to `ALLOWED_FILE_TYPES`
   - Check file extension mapping

### Debug Mode

Enable debug logging to see detailed S3 operations:

```bash
export LOG_LEVEL=DEBUG
```

## Security Considerations

1. **IAM Permissions:**
   - Use least privilege principle
   - Only grant necessary S3 permissions
   - Consider using IAM roles instead of access keys

2. **Presigned URLs:**
   - Set appropriate expiration times
   - Validate file types and sizes
   - Monitor usage patterns

3. **Bucket Security:**
   - Enable bucket versioning
   - Configure lifecycle policies
   - Use bucket encryption

4. **CORS Configuration:**
   - Configure S3 bucket CORS for web uploads
   - Restrict allowed origins
   - Set appropriate headers

## Performance Optimization

1. **Use Presigned URLs:**
   - Reduces server load
   - Better for large files
   - Faster uploads

2. **CDN Integration:**
   - Use CloudFront for file delivery
   - Reduce latency
   - Lower costs

3. **Lifecycle Policies:**
   - Move old files to cheaper storage
   - Automatically delete temporary files
   - Optimize costs

## Monitoring

Monitor S3 usage with:

1. **CloudWatch Metrics:**
   - Request count and latency
   - Error rates
   - Storage usage

2. **Application Logs:**
   - Upload/download success rates
   - Error patterns
   - Performance metrics

3. **Cost Monitoring:**
   - Track storage costs
   - Monitor request costs
   - Set up billing alerts

## Support

For issues or questions:

1. Check the application logs
2. Run the integration test script
3. Verify S3 configuration
4. Check AWS CloudTrail for S3 API calls
