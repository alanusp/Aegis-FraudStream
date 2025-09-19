import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = { vus: 5, duration: '30s', thresholds: { http_req_duration: ['p(95)<200'], http_req_failed: ['rate<0.01'] } };
export default function () {
  const payload = JSON.stringify({ user_id: 'u', amount: 10.5 });
  const res = http.post('http://localhost:8080/v1/score', payload, { headers: { 'Content-Type': 'application/json' } });
  check(res, { 'status 200': (r) => r.status === 200, 'has score': (r) => JSON.parse(r.body).score !== undefined });
  sleep(0.5);
}
