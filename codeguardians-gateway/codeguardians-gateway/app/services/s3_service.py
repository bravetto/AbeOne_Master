"""
S3 File Storage Service

This module provides S3 file storage operations for the CodeGuardians Gateway.
It handles file uploads, downloads, presigned URLs, and file management using AWS S3.
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, BinaryIO
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException

from app.core.config import get_settings
from app.core.exceptions import FileUploadError
from app.utils.logging import get_logger

logger = get_logger(__name__)


class S3Service:
    """
    S3 file storage service for handling file operations.
    
    Provides methods for uploading, downloading, generating presigned URLs,
    and managing files in S3 with proper error handling and validation.
    """
    
    def __init__(self):
        """Initialize S3 service with configuration."""
        self.settings = get_settings()
        self._client: Optional[boto3.client] = None
        self._bucket_name: Optional[str] = None
        self._use_local_fallback = False

        if self.settings.is_s3_enabled:
            try:
                self._initialize_client()
                logger.info("S3 service initialized successfully")
            except Exception as e:
                logger.warning(f"S3 initialization failed: {e}. Using local file system fallback.")
                self._use_local_fallback = True
                self._initialize_local_fallback()
        else:
            logger.warning("S3 is not enabled. Using local file system fallback.")
            self._use_local_fallback = True
            self._initialize_local_fallback()

    def _initialize_local_fallback(self) -> None:
        """Initialize local file system fallback."""
        import os
        # Create uploads directory if it doesn't exist
        self._local_upload_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(self._local_upload_dir, exist_ok=True)
        self._bucket_name = "local-uploads"  # Mock bucket name
        logger.info(f"Local file system fallback initialized: {self._local_upload_dir}")

    def _initialize_client(self) -> None:
        """Initialize S3 client with proper configuration."""
        try:
            # Create S3 client with configuration
            client_kwargs = {
                'region_name': self.settings.S3_REGION,
            }
            
            # Add credentials if provided
            if self.settings.S3_ACCESS_KEY_ID and self.settings.S3_SECRET_ACCESS_KEY:
                client_kwargs.update({
                    'aws_access_key_id': self.settings.S3_ACCESS_KEY_ID,
                    'aws_secret_access_key': self.settings.S3_SECRET_ACCESS_KEY,
                })
                
                if self.settings.S3_SESSION_TOKEN:
                    client_kwargs['aws_session_token'] = self.settings.S3_SESSION_TOKEN
            
            # Add custom endpoint for local testing (e.g., MinIO)
            if self.settings.S3_ENDPOINT_URL:
                client_kwargs['endpoint_url'] = self.settings.S3_ENDPOINT_URL
            
            self._client = boto3.client('s3', **client_kwargs)
            self._bucket_name = self.settings.S3_BUCKET_NAME
            
            # Test connection
            self._test_connection()
            
            logger.info(f"S3 service initialized successfully for bucket: {self._bucket_name}")
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise FileUploadError("S3 credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise FileUploadError(f"S3 initialization failed: {str(e)}")
    
    def _test_connection(self) -> None:
        """Test S3 connection and bucket access."""
        try:
            self._client.head_bucket(Bucket=self._bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                raise FileUploadError(f"S3 bucket '{self._bucket_name}' not found")
            elif error_code == '403':
                raise FileUploadError(f"Access denied to S3 bucket '{self._bucket_name}'")
            else:
                raise FileUploadError(f"S3 connection test failed: {e}")
        except Exception as e:
            raise FileUploadError(f"S3 connection test failed: {e}")
    
    def _generate_file_key(self, filename: str, prefix: str = "uploads") -> str:
        """
        Generate a unique S3 key for the file.
        
        Args:
            filename: Original filename
            prefix: S3 key prefix (default: "uploads")
            
        Returns:
            Unique S3 key for the file
        """
        # Extract file extension
        file_ext = os.path.splitext(filename)[1]
        
        # Generate unique identifier
        unique_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().strftime("%Y/%m/%d")
        
        # Create key: prefix/YYYY/MM/DD/unique_id.ext
        return f"{prefix}/{timestamp}/{unique_id}{file_ext}"
    
    def _validate_file(self, file_content: bytes, filename: str) -> None:
        """
        Validate file before upload.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Raises:
            FileUploadError: If file validation fails
        """
        # Check file size
        if len(file_content) > self.settings.MAX_FILE_SIZE:
            raise FileUploadError(
                f"File too large. Maximum size: {self.settings.MAX_FILE_SIZE} bytes"
            )
        
        # Check file type
        if self.settings.ALLOWED_FILE_TYPES:
            # Get MIME type from filename extension
            file_ext = os.path.splitext(filename)[1].lower()
            mime_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.pdf': 'application/pdf',
            }
            
            file_mime_type = mime_type_map.get(file_ext)
            if file_mime_type not in self.settings.ALLOWED_FILE_TYPES:
                raise FileUploadError(
                    f"File type not allowed. Allowed types: {self.settings.ALLOWED_FILE_TYPES}"
                )
    
    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        user_id: Optional[int] = None,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload file to S3 or local filesystem.

        Args:
            file_content: File content as bytes
            filename: Original filename
            content_type: MIME type of the file
            metadata: Additional metadata for the file

        Returns:
            Dictionary containing file information and storage details

        Raises:
            FileUploadError: If upload fails
        """
        if self._use_local_fallback:
            return await self._upload_file_local(file_content, filename, content_type, metadata, user_id, organization_id)
        elif not self._client:
            raise FileUploadError("S3 service not initialized")
        
        try:
            # Validate file
            self._validate_file(file_content, filename)
            
            # Generate S3 key
            s3_key = self._generate_file_key(filename)
            
            # Prepare metadata
            file_metadata = {
                'original_filename': filename,
                'upload_timestamp': datetime.utcnow().isoformat(),
                'file_size': str(len(file_content)),
            }
            # Add ownership metadata for authorization checks
            if user_id is not None:
                file_metadata['user_id'] = str(user_id)
            if organization_id is not None:
                file_metadata['organization_id'] = str(organization_id)
            if metadata:
                file_metadata.update(metadata)
            
            # Upload to S3
            upload_kwargs = {
                'Bucket': self._bucket_name,
                'Key': s3_key,
                'Body': file_content,
                'Metadata': file_metadata,
            }
            
            if content_type:
                upload_kwargs['ContentType'] = content_type
            
            response = self._client.put_object(**upload_kwargs)
            
            # Generate public URL
            file_url = self._generate_file_url(s3_key)
            
            result = {
                'file_id': s3_key,
                'filename': filename,
                'file_url': file_url,
                'file_size': len(file_content),
                'content_type': content_type,
                'upload_timestamp': file_metadata['upload_timestamp'],
                'etag': response.get('ETag', '').strip('"'),
                's3_key': s3_key,
            }
            
            logger.info(f"File uploaded successfully: {filename} -> {s3_key}")
            return result
            
        except FileUploadError:
            raise
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            raise FileUploadError(f"Upload failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during upload: {e}")
            raise FileUploadError(f"Upload failed: {str(e)}")

    async def _upload_file_local(
        self,
        file_content: bytes,
        filename: str,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        user_id: Optional[int] = None,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload file to local filesystem (fallback when S3 is not available).
        """
        import uuid
        import os
        import hashlib

        try:
            # Validate file
            self._validate_file(file_content, filename)

            # Generate unique file ID and path
            file_id = str(uuid.uuid4())
            file_hash = hashlib.md5(file_content).hexdigest()[:8]
            file_extension = os.path.splitext(filename)[1]
            local_filename = f"{file_id}_{file_hash}{file_extension}"
            file_path = os.path.join(self._local_upload_dir, local_filename)

            # Write file to local filesystem
            with open(file_path, 'wb') as f:
                f.write(file_content)

            # Generate file URL (relative path for local access)
            file_url = f"/uploads/{local_filename}"

            # Prepare result
            result = {
                'file_id': file_id,
                'filename': filename,
                'file_url': file_url,
                'file_size': len(file_content),
                'content_type': content_type or 'application/octet-stream',
                'upload_timestamp': datetime.utcnow().isoformat(),
                'etag': f'"{file_hash}"',
                'storage_type': 'local',
                'local_path': file_path
            }
            
            # Store ownership metadata for local files (in a metadata file)
            local_metadata = {}
            if user_id is not None:
                local_metadata['user_id'] = str(user_id)
            if organization_id is not None:
                local_metadata['organization_id'] = str(organization_id)
            if metadata:
                local_metadata.update(metadata)
            
            # Save metadata to a separate file for local storage
            metadata_path = file_path + '.meta'
            import json
            with open(metadata_path, 'w') as f:
                json.dump(local_metadata, f)

            if metadata:
                result.update(metadata)

            logger.info(f"File uploaded to local storage: {filename} -> {file_path}")
            return result

        except Exception as e:
            logger.error(f"Local file upload failed: {e}")
            raise FileUploadError(f"Upload failed: {str(e)}")

    async def download_file(self, file_id: str) -> bytes:
        """
        Download file from S3.
        
        Args:
            file_id: S3 key or file ID
            
        Returns:
            File content as bytes
            
        Raises:
            FileUploadError: If download fails
        """
        if not self._client:
            raise FileUploadError("S3 service not initialized")
        
        try:
            response = self._client.get_object(
                Bucket=self._bucket_name,
                Key=file_id
            )
            
            return response['Body'].read()
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise FileUploadError("File not found")
            else:
                logger.error(f"S3 download failed: {e}")
                raise FileUploadError(f"Download failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during download: {e}")
            raise FileUploadError(f"Download failed: {str(e)}")
    
    def generate_presigned_upload_url(
        self, 
        filename: str, 
        content_type: Optional[str] = None,
        expires_in: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate presigned URL for direct client upload.
        
        Args:
            filename: Original filename
            content_type: MIME type of the file
            expires_in: URL expiry time in seconds (default: from settings)
            
        Returns:
            Dictionary containing presigned URL and upload details
        """
        if not self._client:
            raise FileUploadError("S3 service not initialized")
        
        try:
            # Generate S3 key
            s3_key = self._generate_file_key(filename)
            
            # Set expiry time
            if expires_in is None:
                expires_in = self.settings.UPLOAD_EXPIRY_MINUTES * 60
            
            # Generate presigned URL
            presigned_url = self._client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self._bucket_name,
                    'Key': s3_key,
                    'ContentType': content_type,
                },
                ExpiresIn=expires_in
            )
            
            # Generate file URL for after upload
            file_url = self._generate_file_url(s3_key)
            
            return {
                'upload_url': presigned_url,
                'file_url': file_url,
                'file_id': s3_key,
                'filename': filename,
                'expires_in': expires_in,
                'expires_at': (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat(),
            }
            
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise FileUploadError(f"Failed to generate upload URL: {e}")
        except Exception as e:
            logger.error(f"Unexpected error generating presigned URL: {e}")
            raise FileUploadError(f"Failed to generate upload URL: {str(e)}")
    
    def generate_presigned_download_url(
        self, 
        file_id: str, 
        expires_in: int = 3600
    ) -> str:
        """
        Generate presigned URL for file download.
        
        Args:
            file_id: S3 key or file ID
            expires_in: URL expiry time in seconds (default: 1 hour)
            
        Returns:
            Presigned download URL
        """
        if not self._client:
            raise FileUploadError("S3 service not initialized")
        
        try:
            presigned_url = self._client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self._bucket_name,
                    'Key': file_id,
                },
                ExpiresIn=expires_in
            )
            
            return presigned_url
            
        except ClientError as e:
            logger.error(f"Failed to generate download URL: {e}")
            raise FileUploadError(f"Failed to generate download URL: {e}")
        except Exception as e:
            logger.error(f"Unexpected error generating download URL: {e}")
            raise FileUploadError(f"Failed to generate download URL: {str(e)}")
    
    def _generate_file_url(self, s3_key: str) -> str:
        """
        Generate public URL for the file.
        
        Args:
            s3_key: S3 key for the file
            
        Returns:
            Public URL for the file
        """
        if self.settings.S3_ENDPOINT_URL:
            # Custom endpoint (e.g., MinIO)
            return f"{self.settings.S3_ENDPOINT_URL}/{self._bucket_name}/{s3_key}"
        else:
            # Standard AWS S3 URL
            return f"https://{self._bucket_name}.s3.{self.settings.S3_REGION}.amazonaws.com/{s3_key}"
    
    async def delete_file(self, file_id: str) -> bool:
        """
        Delete file from S3.
        
        Args:
            file_id: S3 key or file ID
            
        Returns:
            True if deletion was successful
            
        Raises:
            FileUploadError: If deletion fails
        """
        if not self._client:
            raise FileUploadError("S3 service not initialized")
        
        try:
            self._client.delete_object(
                Bucket=self._bucket_name,
                Key=file_id
            )
            
            logger.info(f"File deleted successfully: {file_id}")
            return True
            
        except ClientError as e:
            logger.error(f"S3 deletion failed: {e}")
            raise FileUploadError(f"Deletion failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during deletion: {e}")
            raise FileUploadError(f"Deletion failed: {str(e)}")
    
    async def list_files(self, prefix: str = "uploads", limit: int = 100) -> List[Dict[str, Any]]:
        """
        List files in S3 bucket.
        
        Args:
            prefix: S3 key prefix to filter files
            limit: Maximum number of files to return
            
        Returns:
            List of file information dictionaries
        """
        if not self._client:
            raise FileUploadError("S3 service not initialized")
        
        try:
            response = self._client.list_objects_v2(
                Bucket=self._bucket_name,
                Prefix=prefix,
                MaxKeys=limit
            )
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'file_id': obj['Key'],
                    'file_url': self._generate_file_url(obj['Key']),
                    'file_size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'etag': obj['ETag'].strip('"'),
                })
            
            return files
            
        except ClientError as e:
            logger.error(f"S3 list files failed: {e}")
            raise FileUploadError(f"Failed to list files: {e}")
        except Exception as e:
            logger.error(f"Unexpected error listing files: {e}")
            raise FileUploadError(f"Failed to list files: {str(e)}")
    
    async def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Get file metadata from S3.
        
        Args:
            file_id: S3 key or file ID
            
        Returns:
            File metadata dictionary
        """
        if not self._client:
            raise FileUploadError("S3 service not initialized")
        
        try:
            response = self._client.head_object(
                Bucket=self._bucket_name,
                Key=file_id
            )
            
            return {
                'file_id': file_id,
                'file_url': self._generate_file_url(file_id),
                'file_size': response['ContentLength'],
                'content_type': response.get('ContentType', ''),
                'last_modified': response['LastModified'].isoformat(),
                'etag': response['ETag'].strip('"'),
                'metadata': response.get('Metadata', {}),
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise FileUploadError("File not found")
            else:
                logger.error(f"S3 metadata fetch failed: {e}")
                raise FileUploadError(f"Failed to get file metadata: {e}")
        except Exception as e:
            logger.error(f"Unexpected error getting file metadata: {e}")
            raise FileUploadError(f"Failed to get file metadata: {str(e)}")


# Global S3 service instance
_s3_service: Optional[S3Service] = None


def get_s3_service() -> S3Service:
    """Get S3 service instance."""
    global _s3_service
    if _s3_service is None:
        _s3_service = S3Service()
    return _s3_service
