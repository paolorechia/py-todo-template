from litestar import Litestar, get

from src.lifecycle_hooks import (
    read_environment,
    get_db_connection,
    close_db_connection,
)


# If blocking I/O, should set sync_to_thread to delegate work to thread pool.
# Note: not enough for CPU heavy tasks, which then requires separate process
@get("/", sync_to_thread=True)
def hello_world() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"hello": "world"}


litestar_app = Litestar(
    route_handlers=[hello_world],
    on_startup=[read_environment, get_db_connection],
    on_shutdown=[close_db_connection],
)