from litestar import Litestar, get


# If blocking I/O, should set sync_to_thread to delegate work to thread pool.
# Note: not enough for CPU heavy tasks, which then requires separate process
@get("/", sync_to_thread=True)
def hello_world() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"hello": "world"}


app = Litestar(route_handlers=[hello_world])

