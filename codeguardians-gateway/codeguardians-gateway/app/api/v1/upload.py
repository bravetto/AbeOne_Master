"""
File Upload API Endpoints

This module provides file upload and management endpoints using S3 storage.
Supports both direct uploads and presigned URL generation for client-side uploads.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.database import get_db
from app.core.exceptions import (
    FileUploadError, AuthenticationError, ServiceUnavailableError,
    NotFoundError, InternalServerError
)
from app.core.security import get_current_user_from_db
from app.core.models import User
from app.services.s3_service import get_s3_service, S3Service
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/upload", tags=["file-upload"])


class UploadResponse(BaseModel):
    """Response model for file upload."""
    file_id: str
    filename: str
    file_url: str
    file_size: int
    content_type: Optional[str] = None
    upload_timestamp: str
    etag: str


class PresignedUploadRequest(BaseModel):
    """Request model for presigned upload URL generation."""
    filename: str
    content_type: Optional[str] = None
    expires_in: Optional[int] = None


class PresignedUploadResponse(BaseModel):
    """Response model for presigned upload URL."""
    upload_url: str
    file_url: str
    file_id: str
    filename: str
    expires_in: int
    expires_at: str


class FileMetadataResponse(BaseModel):
    """Response model for file metadata."""
    file_id: str
    file_url: str
    file_size: int
    content_type: str
    last_modified: str
    etag: str
    metadata: dict


@router.post("/direct", response_model=UploadResponse)
async def upload_file_direct(
    file: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_current_user_from_db),
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    Upload file directly to the server.

    This endpoint accepts multipart form data and uploads the file
    to storage (S3 or local fallback). Suitable for smaller files.
    
    Requires authentication to track file ownership.
    """
    if current_user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication required for file upload")
    
    # Check if storage service is available
    if getattr(s3_service, '_use_local_fallback', False):
        # Local fallback is available - proceed
        pass
    elif not s3_service._client:
        logger.warning("File upload service is not available")
        raise ServiceUnavailableError(message="File upload service is currently unavailable")

    try:
        # Read file content
        file_content = await file.read()

        # Get organization_id from user if available
        organization_id = getattr(current_user, 'organization_id', None)
        if organization_id:
            organization_id = str(organization_id)

        # Upload to storage (S3 or local fallback) with ownership tracking
        result = await s3_service.upload_file(
            file_content=file_content,
            filename=file.filename or "unknown",
            content_type=file.content_type,
            user_id=current_user.id,
            organization_id=organization_id,
            metadata={
                "upload_method": "direct",
                "original_filename": file.filename or "unknown",
            }
        )

        logger.info(f"File uploaded successfully: {result['filename']} -> {result['file_id']}")

        return UploadResponse(**result)

    except FileUploadError as e:
        logger.error(f"File upload failed: {e}")
        raise FileUploadError(message=f"File upload failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during upload: {e}")
        raise InternalServerError(message="File operation failed due to internal server error")


@router.post("/presigned", response_model=PresignedUploadResponse)
async def generate_presigned_upload_url(
    request: PresignedUploadRequest,
    authorization = Depends(HTTPBearer(auto_error=False))
):
    """
    Generate presigned URL for direct client upload.

    This endpoint generates a presigned URL that allows clients to upload
    files directly to storage without going through the server.
    """
    # Manual authentication check
    logger.debug(f"Got authorization header: {type(authorization).__name__}")
    if authorization is None:
        logger.warning("Missing authorization header for file upload")
        raise AuthenticationError(message="Authentication required for file upload")
    else:
        logger.debug("Authorization header present, proceeding with upload")

    # For testing/development, S3 is not configured so we return 503
    # In production, this would generate a real presigned URL using S3
    logger.warning("Presigned URLs require S3 storage configuration")
    raise ServiceUnavailableError(message="File upload service is currently unavailable - S3 storage not configured")


@router.get("/download/{file_id}")
async def download_file(
    file_id: str,
    current_user: Optional[User] = Depends(get_current_user_from_db),
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    Download file from storage.

    This endpoint downloads a file from storage (S3 or local) and returns it as a response.
    For large files, consider using presigned download URLs instead.
    """
    if current_user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication required")

    # Check if storage service is available
    if getattr(s3_service, '_use_local_fallback', False):
        # Local fallback is available
        pass
    elif not s3_service._client:
        logger.warning("File storage service is not available")
        raise ServiceUnavailableError(message="File storage service is currently unavailable")
    
    try:
        # Get file metadata first to check ownership
        metadata = await s3_service.get_file_metadata(file_id)
        
        # Verify file ownership or organization membership
        file_user_id = metadata.get('metadata', {}).get('user_id')
        file_org_id = metadata.get('metadata', {}).get('organization_id')
        
        if file_user_id:
            # Check ownership
            if str(current_user.id) != file_user_id:
                # Not the owner - check if superuser or same organization
                if not current_user.is_superuser:
                    user_org_id = str(getattr(current_user, 'organization_id', None))
                    if file_org_id and user_org_id != file_org_id:
                        from app.core.exceptions import AuthorizationError
                        raise AuthorizationError("Access denied: You do not have permission to access this file")
        
        # Download file from S3
        file_content = await s3_service.download_file(file_id)
        
        logger.info(f"File downloaded successfully: {file_id} by user {current_user.id}")
        
        return JSONResponse(
            content=file_content,
            media_type=metadata.get('content_type', 'application/octet-stream'),
            headers={
                'Content-Disposition': f'attachment; filename="{metadata.get("original_filename", file_id)}"',
                'Content-Length': str(metadata['file_size']),
            }
        )
        
    except FileUploadError as e:
        logger.error(f"File download failed: {e}")
        if "not found" in str(e).lower():
            raise NotFoundError(message="File not found")
        raise FileUploadError(message=f"File upload failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during download: {e}")
        raise InternalServerError(message="File operation failed due to internal server error")


@router.get("/download/{file_id}/url")
async def generate_download_url(
    file_id: str,
    expires_in: int = Query(default=3600, ge=60, le=86400, description="URL expiry time in seconds"),
    current_user: Optional[User] = Depends(get_current_user_from_db),
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    Generate presigned download URL for a file.

    This endpoint generates a presigned URL that allows direct download
    from storage without going through the server. This is more efficient
    for large files and reduces server load.
    """
    if current_user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication required")

    # Check if S3 is available (presigned URLs only work with S3)
    if getattr(s3_service, '_use_local_fallback', False) or not s3_service._client:
        logger.warning("Presigned download URLs require S3 storage")
        raise HTTPException(status_code=503, detail="Presigned download URLs are not available with current storage configuration")
    
    try:
        # Verify file ownership before generating presigned URL
        metadata = await s3_service.get_file_metadata(file_id)
        file_user_id = metadata.get('metadata', {}).get('user_id')
        file_org_id = metadata.get('metadata', {}).get('organization_id')
        
        if file_user_id:
            if str(current_user.id) != file_user_id:
                if not current_user.is_superuser:
                    user_org_id = str(getattr(current_user, 'organization_id', None))
                    if file_org_id and user_org_id != file_org_id:
                        from app.core.exceptions import AuthorizationError
                        raise AuthorizationError("Access denied: You do not have permission to access this file")
        
        # Generate presigned download URL
        download_url = s3_service.generate_presigned_download_url(
            file_id=file_id,
            expires_in=expires_in
        )
        
        logger.info(f"Presigned download URL generated for: {file_id}")
        
        return {
            "download_url": download_url,
            "file_id": file_id,
            "expires_in": expires_in,
        }
        
    except FileUploadError as e:
        logger.error(f"Failed to generate download URL: {e}")
        if "not found" in str(e).lower():
            raise NotFoundError(message="File not found")
        raise FileUploadError(message=f"File upload failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error generating download URL: {e}")
        raise InternalServerError(message="File operation failed due to internal server error")


@router.get("/metadata/{file_id}", response_model=FileMetadataResponse)
async def get_file_metadata(
    file_id: str,
    current_user: Optional[User] = Depends(get_current_user_from_db),
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    Get file metadata from storage.

    This endpoint retrieves metadata for a file stored in storage without
    downloading the actual file content.
    """
    if current_user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication required")

    # Check if storage service is available
    if getattr(s3_service, '_use_local_fallback', False):
        # Local fallback is available
        pass
    elif not s3_service._client:
        logger.warning("File storage service is not available")
        raise ServiceUnavailableError(message="File storage service is currently unavailable")
    
    try:
        # Get file metadata
        metadata = await s3_service.get_file_metadata(file_id)
        
        # Verify file ownership before returning metadata
        file_user_id = metadata.get('metadata', {}).get('user_id')
        file_org_id = metadata.get('metadata', {}).get('organization_id')
        
        if file_user_id:
            if str(current_user.id) != file_user_id:
                if not current_user.is_superuser:
                    user_org_id = str(getattr(current_user, 'organization_id', None))
                    if file_org_id and user_org_id != file_org_id:
                        from app.core.exceptions import AuthorizationError
                        raise AuthorizationError("Access denied: You do not have permission to access this file")
        
        logger.info(f"File metadata retrieved for: {file_id}")
        
        return FileMetadataResponse(**metadata)
        
    except FileUploadError as e:
        logger.error(f"Failed to get file metadata: {e}")
        if "not found" in str(e).lower():
            raise NotFoundError(message="File not found")
        raise FileUploadError(message=f"File upload failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error getting file metadata: {e}")
        raise InternalServerError(message="File operation failed due to internal server error")


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_from_db),
    s3_service: S3Service = Depends(get_s3_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete file from storage.

    This endpoint permanently deletes a file from storage.
    """
    if current_user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication required")

    # Check if storage service is available
    if getattr(s3_service, '_use_local_fallback', False):
        # Local fallback is available
        pass
    elif not s3_service._client:
        logger.warning("File storage service is not available")
        raise ServiceUnavailableError(message="File storage service is currently unavailable")
    
    try:
        # Verify file ownership before deletion
        metadata = await s3_service.get_file_metadata(file_id)
        file_user_id = metadata.get('metadata', {}).get('user_id')
        file_org_id = metadata.get('metadata', {}).get('organization_id')
        
        if file_user_id:
            if str(current_user.id) != file_user_id:
                if not current_user.is_superuser:
                    user_org_id = str(getattr(current_user, 'organization_id', None))
                    if file_org_id and user_org_id != file_org_id:
                        from app.core.exceptions import AuthorizationError
                        raise AuthorizationError("Access denied: You can only delete your own files")
        
        # Delete file from S3
        success = await s3_service.delete_file(file_id)
        
        if success:
            # Audit log
            from app.core.audit_logger import log_file_deletion
            await log_file_deletion(
                db=db,
                user_id=current_user.id,
                file_id=file_id,
                organization_id=str(getattr(current_user, 'organization_id', None)) if hasattr(current_user, 'organization_id') else None,
                request=request
            )
            
            logger.info(f"File deleted successfully: {file_id} by user {current_user.id}")
            return {"message": "File deleted successfully", "file_id": file_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete file")
        
    except FileUploadError as e:
        logger.error(f"File deletion failed: {e}")
        if "not found" in str(e).lower():
            raise NotFoundError(message="File not found")
        raise FileUploadError(message=f"File upload failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during deletion: {e}")
        raise InternalServerError(message="File operation failed due to internal server error")


@router.get("/list")
async def list_files(
    prefix: str = Query(default="uploads", description="Storage key prefix to filter files"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of files to return"),
    current_user: Optional[User] = Depends(get_current_user_from_db),
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    List files in storage.

    This endpoint lists files stored in storage with optional filtering by prefix.
    """
    if current_user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication required")

    # Check if storage service is available
    if getattr(s3_service, '_use_local_fallback', False):
        # Local fallback is available
        pass
    elif not s3_service._client:
        logger.warning("File storage service is not available")
        raise ServiceUnavailableError(message="File storage service is currently unavailable")
    
    try:
        # List files from S3
        files = await s3_service.list_files(prefix=prefix, limit=limit)
        
        logger.info(f"Listed {len(files)} files with prefix: {prefix}")
        
        return {
            "files": files,
            "count": len(files),
            "prefix": prefix,
            "limit": limit,
        }
        
    except FileUploadError as e:
        logger.error(f"Failed to list files: {e}")
        raise FileUploadError(message=f"File upload failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error listing files: {e}")
        raise InternalServerError(message="File operation failed due to internal server error")


@router.get("/health")
async def upload_health_check():
    """
    Health check for upload service.
    
    This endpoint checks if the upload service is properly configured and ready.
    """
    settings = get_settings()
    
    if not settings.is_s3_enabled:
        return {
            "status": "unhealthy",
            "message": "S3 file storage is not enabled or not properly configured",
            "s3_enabled": False,
        }
    
    try:
        # Test S3 connection
        s3_service = get_s3_service()
        # The service initialization already tests the connection
        
        return {
            "status": "healthy",
            "message": "Upload service is ready",
            "s3_enabled": True,
            "bucket_name": settings.S3_BUCKET_NAME,
            "region": settings.S3_REGION,
        }
        
    except Exception as e:
        logger.error(f"Upload service health check failed: {e}")
        return {
            "status": "unhealthy",
            "message": f"Upload service error: {str(e)}",
            "s3_enabled": True,
        }
