import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status

from app.core import cloudinary_config  # noqa: F401 -- cloudinary.config() çalışsın diye import ediliyor


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE_MB = 5


async def upload_image_to_cloudinary(file: UploadFile, folder: str = "mediumvari/posts") -> str:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, WEBP, and GIF images are allowed."
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image must be smaller than {MAX_FILE_SIZE_MB}MB."
        )

    try:
        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="image",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Image upload failed: {str(e)}"
        )

    return result["secure_url"]