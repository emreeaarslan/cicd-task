import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import (
    ALWAYS_ON,
    ParentBased,
    Sampler,
    TraceIdRatioBased,
)


class DemoEndpointSampler(Sampler):
    """
    Use 50% head sampling only for /sampling/head.

    All other root traces are sampled so they can reach the Collector,
    where tail sampling can make its decision later.
    """

    def __init__(self):
        self._head_sampler = TraceIdRatioBased(0.5)
        self._default_sampler = ALWAYS_ON

    def should_sample(
        self,
        parent_context,
        trace_id,
        name,
        kind=None,
        attributes=None,
        links=None,
        trace_state=None,
    ):
        attributes = attributes or {}
        route = attributes.get("http.route")

        if route == "/sampling/head" or name.endswith(" /sampling/head"):
            sampler = self._head_sampler
        else:
            sampler = self._default_sampler

        return sampler.should_sample(
            parent_context,
            trace_id,
            name,
            kind,
            attributes,
            links,
            trace_state,
        )

    def get_description(self):
        return "DemoEndpointSampler{head=/sampling/head:0.5,default=1.0}"


def configure_tracing(app):
    if os.getenv("OTEL_TRACING_ENABLED", "false").lower() != "true":
        return

    resource = Resource.create(
        {
            SERVICE_NAME: "backend",
        }
    )

    provider = TracerProvider(
        resource=resource,
        sampler=ParentBased(DemoEndpointSampler()),
    )

    exporter = OTLPSpanExporter(
        endpoint=os.getenv(
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
            "http://otel-collector:4318/v1/traces",
        )
    )

    provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )

    trace.set_tracer_provider(provider)

    FlaskInstrumentor().instrument_app(
        app,
        excluded_urls="health,metrics",
    )

    PsycopgInstrumentor().instrument()
