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

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Manual instrumentation on top of automatic
# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "todo-app"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="jaeger-service:4317"))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="jaeger-service:4317")
)

meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

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

    with Session(engine) as session:
        items = session.query(Item).all()

    response = []
    for item in items:
        response.append(item.as_dict())
    return response


litestar_app = Litestar(
    route_handlers=[hello_world],
    on_startup=[read_environment, get_db_connection, apply_db_metadata],
    on_shutdown=[close_db_connection],
    exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler},
)
