# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import asyncio, json, os
from typing import Any
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer  # type: ignore

async def main():
    brokers = os.getenv("AEGIS_KAFKA_BROKERS","127.0.0.1:9092")
    topic_in = os.getenv("AEGIS_KAFKA_INPUT","aegis-input")
    topic_out = os.getenv("AEGIS_KAFKA_OUTPUT","aegis-output")
    from aegis_fraudstream.features import FeatureResolver
    from aegis_fraudstream.model import Model
    resolver, model = FeatureResolver(), Model()
    consumer = AIOKafkaConsumer(topic_in, bootstrap_servers=brokers, enable_auto_commit=True, auto_offset_reset="latest")
    producer = AIOKafkaProducer(bootstrap_servers=brokers)
    await consumer.start(); await producer.start()
    try:
        async for msg in consumer:
            try:
                ev = json.loads(msg.value.decode())
                feats = resolver.resolve(ev)
                score = float(model.score(feats["amount"], feats["velocity"], feats["country_risk"]))
                out = {"user_id": ev.get("user_id"), "score": score}
                await producer.send_and_wait(topic_out, json.dumps(out).encode())
            except Exception:
                pass
    finally:
        await consumer.stop(); await producer.stop()

if __name__ == "__main__":
    asyncio.run(main())
