# Microshop

A production-grade e-commerce platform built as a hands-on DevOps portfolio project — designed to demonstrate end-to-end microservices architecture, containerization, orchestration, CI/CD, and observability.

## Overview

Microshop simulates a real e-commerce backend made of independent microservices. Each service owns its own database, runs in its own container, and communicates with others over REST and event-driven messaging. The entire stack is deployable locally via Docker Compose and to Kubernetes via Helm.

## Tech Stack

| Layer | Technology |
|---|---|
| API Services | FastAPI (Python 3.12) |
| Databases | PostgreSQL |
| Cache / Messaging | Redis |
| Containers | Docker, Docker Compose |
| Orchestration | Kubernetes (Minikube) |
| Package Management | Helm |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus, Grafana |
| Logging | ELK Stack (Elasticsearch, Logstash, Kibana) |
| Payments | Stripe (test mode) |

## Services

| Service | Responsibility | Port |
|---|---|---|
| product-service | Manage product catalog, inventory | 8001 |
| order-service | Handle order creation and state | 8002 |
| payment-service | Process payments via Stripe | 8003 |
| analytics-service | Aggregate events for reporting | 8004 |

## Project Status

🚧 In active development — built incrementally over 30 days as a learning project.

## Getting Started

Setup instructions will be added as each service comes online. See `docs/daily-logs/` for day-by-day build progress.

## Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [Daily Logs](docs/daily-logs/)
- [Runbooks](docs/runbooks/)

## License

MIT