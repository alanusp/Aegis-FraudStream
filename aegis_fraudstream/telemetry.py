# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

from .config import settings
try:
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    import sentry_sdk
except Exception:
    trace=metrics=None
    sentry_sdk=None
def init_telemetry():
    if settings.sentry_dsn and sentry_sdk is not None:
        sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.0)
    if settings.telemetry.lower()!='on' or not settings.otlp_endpoint:
        return
    if trace is None:
        return
    resource=Resource.create({'service.name': settings.service_name})
    tp=TracerProvider(resource=resource)
    tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otlp_endpoint)))
    trace.set_tracer_provider(tp)
    mp=MeterProvider(resource=resource)
    reader=PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=settings.otlp_endpoint))
    mp._sdk_config.metric_readers=[reader]
    metrics.set_meter_provider(mp)
