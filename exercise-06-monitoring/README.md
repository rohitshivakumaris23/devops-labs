# Exercise 06 — Prometheus and Grafana Monitoring

## Objective
Create a monitored Flask application that exposes Prometheus metrics, configure Prometheus scraping, set up a Grafana dashboard with meaningful metrics panels, and create alert rules.

## Technologies Used
- Flask 3.0.3 + prometheus-client 0.20.0
- Prometheus (prom/prometheus:latest)
- Grafana (grafana/grafana:latest)
- Docker Compose

## Project Structure
```
exercise-06-monitoring/
├── app.py                       # Flask app exposing /metrics endpoint
├── requirements.txt             # flask + prometheus-client
├── Dockerfile                   # Python:3.11-slim
├── docker-compose.yml           # Flask + Prometheus + Grafana stack
├── prometheus.yml               # Prometheus scrape configuration
├── alert_rules.yml              # Alert rules (3 rules defined)
├── grafana-datasource.yml       # Auto-configures Prometheus datasource
├── grafana-dashboard-config.yml # Dashboard provisioning config
├── grafana-dashboard.json       # Pre-built Flask metrics dashboard
└── README.md
```

## Step-by-Step Commands

### 1. Start the Full Monitoring Stack
```powershell
docker compose up -d --build
```

### 2. Verify Services
```powershell
docker compose ps
```

### 3. Access Endpoints
| Service | URL | Credentials |
|---|---|---|
| Flask App | http://localhost:5006 | — |
| Flask Metrics | http://localhost:5006/metrics | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin123 |

### 4. Generate Metrics
```powershell
# Hit the app endpoints to generate traffic
for ($i=0; $i -lt 20; $i++) {
    Invoke-RestMethod http://localhost:5006/
    Invoke-RestMethod http://localhost:5006/health
    Invoke-RestMethod http://localhost:5006/data
    Start-Sleep -Milliseconds 200
}
```

### 5. Verify Prometheus Scraping
- Go to http://localhost:9090/targets
- `flask-app` should show **UP**

### 6. Import Grafana Dashboard
- Go to http://localhost:3000 → Dashboards → "Flask App - Exercise 06 Dashboard"
- (Auto-provisioned via `grafana-dashboard.json`)

## Prometheus Metrics Exposed

| Metric | Type | Description |
|---|---|---|
| `flask_requests_total` | Counter | Total HTTP requests by method, endpoint, status |
| `flask_request_duration_seconds` | Histogram | Request duration with buckets |
| `flask_active_requests` | Gauge | Currently in-flight requests |
| `flask_app_info` | Gauge | App version and environment info |

## Alert Rules Defined

| Alert | Condition | Severity |
|---|---|---|
| `HighRequestRate` | `rate > 10 req/s for 1m` | Warning |
| `SlowResponseTime` | `p95 latency > 500ms for 2m` | Warning |
| `FlaskAppDown` | `up == 0 for 30s` | Critical |

> **Alert Status**: Alerts are **defined** in `alert_rules.yml` but were **not triggered** during this lab session as load was insufficient to breach thresholds.

## Grafana Dashboard Panels
1. **Request Rate (req/s)** — Time series of `rate(flask_requests_total[1m])`
2. **p95 Response Time** — `histogram_quantile(0.95, ...)`
3. **Active Requests** — Current gauge value
4. **Total Requests (1h)** — `increase(flask_requests_total[1h])`

## Viva Questions

**Q1: What is Prometheus?**  
Prometheus is an open-source monitoring system with a time-series database. It scrapes metrics from target HTTP endpoints at configured intervals.

**Q2: What is the difference between Counter, Gauge, and Histogram?**  
- **Counter**: Only increases (e.g., total requests)
- **Gauge**: Can increase or decrease (e.g., active connections)
- **Histogram**: Measures distribution of values across buckets (e.g., response times)

**Q3: What is `rate()` in PromQL?**  
`rate(metric[5m])` calculates the per-second average rate of increase over the last 5 minutes — used for counters.

**Q4: How does Grafana connect to Prometheus?**  
Via a datasource configuration pointing to the Prometheus HTTP API (`http://prometheus:9090`). Grafana queries PromQL and renders the results.

**Q5: What is `histogram_quantile(0.95, ...)`?**  
It calculates the 95th percentile (p95) from a histogram metric — meaning 95% of requests are faster than this value.

## Conclusion
Flask application built with 4 Prometheus metrics (Counter, Histogram, Gauge). Prometheus scrape config targets `/metrics` every 5s. Grafana dashboard pre-provisioned with 4 meaningful panels. Three alert rules configured for production-ready monitoring.
