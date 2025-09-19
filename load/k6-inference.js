// k6 run load/k6-inference.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = { vus: 10, duration: '30s' };

export default function () {
  const url = 'http://127.0.0.1:8080/v1/inference';
  const payload = JSON.stringify({ user_id:'u1', amount:10, tx_count_1h:1, country_risk:0.1 });
  const params = { headers: { 'Content-Type': 'application/json' } };
  const res = http.post(url, payload, params);
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(0.1);
}
