from fastapi import APIRouter, Depends, UploadFile, File

from app.dependencies.auth import current_user
from app.models.user import User
from app.services.image_upload import upload_image_to_cloudinary

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


@router.post(
    "/upload",
    summary="Upload an image",
    description="""
Uploads an image to Cloudinary and returns its URL.

This is a general-purpose upload endpoint — it is not tied to any specific post.
Useful when creating a post before it has been saved (e.g. selecting a cover image
or inserting an image into the editor before publishing).
"""
)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(current_user),
):
    image_url = await upload_image_to_cloudinary(file)
    return {"url": image_url}