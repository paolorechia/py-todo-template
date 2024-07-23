import logging
from litestar import Request, Response, MediaType

logger = logging.getLogger(__name__)


def internal_server_error_handler(request: Request, exc: Exception) -> Response:
    logger.exception(exc, exc_info=exc)
    return Response(
        media_type=MediaType.TEXT,
        content=f"server error: {exc}",
        status_code=500,
    )
