# Kafka Worker

- Install extras: `pip install .[kafka]`
- Run: `AEGIS_KAFKA_BROKERS=host:9092 python scripts/kafka_worker.py`
- Consumes JSON events from `AEGIS_KAFKA_INPUT` and produces scored events to `AEGIS_KAFKA_OUTPUT`.
