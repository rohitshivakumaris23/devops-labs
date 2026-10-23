# Exercise 06 — Prometheus and Grafana

## Objective
Create a Flask application that exposes Prometheus metrics, configure Prometheus to scrape it, show the metrics on a Grafana dashboard, and define example alert rules.

## Technologies Used
- Flask with `prometheus-client`
- Prometheus (`prom/prometheus`)
- Grafana (`grafana/grafana`)
- Docker Compose

## Prerequisites
- Docker Desktop running
- Ports 5006, 9090 and 3000 free
- Minikube and Jenkins stopped, to free memory

## Project Structure
```
exercise-06-monitoring/
├── app.py                  # Flask app exposing /metrics
├── Dockerfile
├── docker-compose.yml      # flask-app, prometheus, grafana
├── prometheus.yml          # scrape configuration
├── alert_rules.yml         # 3 example alert rules
├── grafana-dashboard.json  # dashboard definition
├── grafana-*.yml           # Grafana provisioning
├── evidence.txt
└── README.md
```

## Step-by-Step Commands
```powershell
cd E:\devops-labs\exercise-06-monitoring
docker compose up -d --build
docker compose ps
1..50 | ForEach-Object { Invoke-RestMethod http://localhost:5006/ | Out-Null }
```
Then open:
- http://localhost:5006/metrics
- http://localhost:9090/targets
- http://localhost:9090/alerts
- http://localhost:3000 (demo login from the compose file)

Stop the stack when finished:
```powershell
docker compose down
```

## Configuration Explanation
- **`/metrics`:** the Flask app exposes request counters, request duration and active requests.
- **`prometheus.yml`:** Prometheus scrapes `flask-app:5000/metrics` using the service name on the Docker network.
- **`alert_rules.yml`:** group `flask_alerts` with three rules:
  - `HighRequestRate`: `rate(flask_requests_total[1m]) > 10` for 1m (warning)
  - `SlowResponseTime`: p95 request duration above 0.5 s for 2m (warning)
  - `FlaskAppDown`: `up{job="flask-app"} == 0` for 30s (critical)
- **Grafana:** its datasource URL must be `http://prometheus:9090`, because Grafana runs in its own container.

## Actual Observed Results

- **Containers:** `ex06-flask` (healthy), `ex06-prometheus` and `ex06-grafana` were all Up.
- **Prometheus targets** (http://localhost:9090/targets): `flask-app` showed **1/1 up** and `prometheus` showed **1/1 up**.
- **Grafana dashboard** "Flask App - Exercise 06 Dashboard":
  - Request Rate panel showed lines for `/ [200]` and `/health [200]`.
  - Active Requests showed 1.
  - Total Requests (Last Hour) showed a value of about 32.6, which is a Prometheus estimate.
  - The p95 Response Time panel stayed empty, because there was not enough latency data in the window.
- **Alerts** (http://localhost:9090/alerts): group `flask_alerts` showed **INACTIVE (3)**. All three rules were loaded and none fired. **No alert was triggered** during this run.

## Troubleshooting

| Problem | Fix |
|---|---|
| Grafana panels show "No data" with a warning icon | The datasource was missing or pointed at an old ID. Add a Prometheus datasource with URL `http://prometheus:9090`, click Save & test, then select it in the dashboard's datasource dropdown. This was done manually in this run |
| Target shows DOWN | Check `docker compose ps` and that the scrape address is `flask-app:5000` |
| Dashboard empty | Generate traffic with the `Invoke-RestMethod` loop and set the time range to the last 5 minutes |
| `failed to connect to the docker API` | Docker Desktop is not running yet |

## Key Concepts
- **Counter, Gauge, Histogram:** the three Prometheus metric types used for requests, active requests and latency.
- **Scraping:** Prometheus pulls metrics from `/metrics` on a schedule.
- **PromQL:** the query language, for example `rate(flask_requests_total[1m])`.
- **Alert rule `for:`:** the condition must stay true for that long before the alert fires.

## Viva Questions

**Q1: How does Prometheus collect metrics?**
It scrapes the `/metrics` endpoint of each target at a set interval.

**Q2: What is the difference between a Counter and a Gauge?**
A counter only goes up, such as total requests. A gauge can go up and down, such as active requests.

**Q3: What does `rate()` do?**
It calculates the per-second average increase of a counter over a time window.

**Q4: Why must the Grafana datasource URL be `http://prometheus:9090`?**
Grafana runs in its own container, so `localhost` would point to itself. The service name resolves on the Docker network.

**Q5: What does `for: 1m` mean in an alert rule?**
The condition must be true continuously for one minute before the alert moves from Pending to Firing.

**Q6: Was any alert triggered?**
No. All three rules were loaded and Inactive. To trigger `FlaskAppDown`, stop the Flask container and wait about 30 seconds.

## Conclusion
Prometheus scraped the Flask metrics endpoint (target UP), Grafana displayed the request metrics on a dashboard, and three alert rules were loaded. The rules stayed Inactive, so none was triggered.