import cloudinary
import cloudinary.uploader

from app.core.config import settings


_is_configured = False


def _configure_cloudinary() -> None:
    global _is_configured
    if _is_configured:
        return

    if (
        not settings.cloudinary_cloud_name
        or not settings.cloudinary_api_key
        or not settings.cloudinary_api_secret
    ):
        raise RuntimeError(
            "Cloudinary is not configured. Set CLOUDINARY_CLOUD_NAME, "
            "CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET."
        )

    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=settings.cloudinary_secure,
    )
    _is_configured = True


def upload_file_bytes(
    file_bytes: bytes,
    filename: str,
    folder: str | None = None,
    resource_type: str = "auto",
    public_id: str | None = None,
) -> dict:
    _configure_cloudinary()
    return cloudinary.uploader.upload(
        file=file_bytes,
        filename=filename,
        folder=folder,
        resource_type=resource_type,
        public_id=public_id,
    )


def upload_file_path(
    file_path: str,
    folder: str | None = None,
    resource_type: str = "auto",
    public_id: str | None = None,
) -> dict:
    _configure_cloudinary()
    return cloudinary.uploader.upload(
        file=file_path,
        folder=folder,
        resource_type=resource_type,
        public_id=public_id,
    )


def delete_asset(public_id: str, resource_type: str = "image") -> dict:
    _configure_cloudinary()
    return cloudinary.uploader.destroy(public_id, resource_type=resource_type)
