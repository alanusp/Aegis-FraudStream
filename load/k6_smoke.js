import http from 'k6/http';
import { check, sleep } from 'k6';
export let options = { vus: 5, duration: '30s' };
export default function () {
  const url = __ENV.BASE || 'http://127.0.0.1:8080/v1/inference';
  const payload = JSON.stringify({user_id:'u1', amount:10, tx_count_1h:1, country_risk:0.1});
  const params = { headers: { 'content-type': 'application/json' } };
  const res = http.post(url, payload, params);
  check(res, { '200': (r) => r.status === 200 });
  sleep(1);
}
