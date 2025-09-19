// Simple performance smoke with budgets
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = { vus: 20, duration: '15s', thresholds: { http_req_duration: ['p(95)<200'] } };
export default function () {
  const url = `${__ENV.BASE || 'http://localhost:8080'}/v1/inference`;
  const res = http.post(url, JSON.stringify({user_id:'u1',amount:12,tx_count_1h:1,country_risk:0.1}), { headers: { 'content-type': 'application/json' } });
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(0.1);
}
