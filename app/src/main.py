from litestar import Litestar, Request, get
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.orm import Session

from src.lifecycle_hooks import (
    read_environment,
    apply_db_metadata,
    get_db_connection,
    close_db_connection,
)
from src.database import Item
from src.exception_handlers import internal_server_error_handler


# If blocking I/O, should set sync_to_thread to delegate work to thread pool.
# Note: not enough for CPU heavy tasks, which then requires separate process
@get("/", sync_to_thread=True)
def hello_world(request: Request) -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    engine = request.app.state.engine
    assert engine, "Database engine is not configured!!"
    with Session(engine) as session:
        item = Item(name="test-item", status="todo")
        session.add(item)
        session.commit()

    return {"hello": "world"}


litestar_app = Litestar(
    route_handlers=[hello_world],
    on_startup=[read_environment, get_db_connection, apply_db_metadata],
    on_shutdown=[close_db_connection],
    exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler},
)
