# Distributed Rate Limiter

A production-inspired distributed rate limiting service built using Flask, Redis, Docker, and Nginx.

This project implements multiple industry-standard rate limiting algorithms including:

- Fixed Window Counter
- Token Bucket
- Sliding Window Counter
- Sliding Window Log (Lua-based atomic implementation)

The system supports:
- distributed rate limiting across multiple backend instances
- JWT-aware user throttling
- runtime algorithm switching
- Redis-backed shared state
- middleware-based request interception
- Nginx load balancing
- Dockerized deployment

---

# Architecture

```text
                ┌─────────────────┐
                │     Client      │
                └────────┬────────┘
                         │
                    HTTP Request
                         │
                ┌────────-────────┐
                │      Nginx      │
                │  Load Balancer  │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
      ┌───────-───────┐     ┌──────-──────┐
      │ Flask App 1   │     │ Flask App 2 │
      └───────┬───────┘     └──────┬──────┘
              │                    │
              └────────┬───────────┘
                       │
                ┌──────-──────┐
                │    Redis    │
                └─────────────┘
```

---

# Features

## Distributed Rate Limiting

All backend instances share rate limiting state through Redis.

This ensures:
- global consistency
- horizontal scalability
- centralized coordination

---

## Multiple Rate Limiting Algorithms

### Fixed Window Counter
Simple and fast counter-based limiting.

### Token Bucket
Allows traffic bursts while controlling average request rate.

### Sliding Window Counter
Weighted rolling window implementation with smoother limiting.

### Sliding Window Log
Precise rolling-window limiting using Redis sorted sets and Lua scripting.

---

## Atomic Redis Lua Scripts

The sliding log algorithm uses Redis Lua scripting to ensure atomic execution.

This prevents race conditions during concurrent requests.

Without Lua:
- multiple requests may bypass limits simultaneously

With Lua:
- all operations execute atomically inside Redis

---

## JWT-aware User Throttling

Supports:
- per-IP limiting
- authenticated user limiting

Authenticated requests are rate-limited based on JWT user identity instead of IP address.

---

## Runtime Configuration Updates

Rate limiting strategy and thresholds can be updated dynamically without restarting services.

Example:

```json
{
  "algorithm": "token_bucket",
  "limit": 20,
  "window": 60
}
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Backend Framework | Flask |
| Shared State Store | Redis |
| Reverse Proxy | Nginx |
| Containerization | Docker |
| WSGI Server | Gunicorn |
| Authentication | JWT |
| Distributed Coordination | Redis |
| Atomic Operations | Redis Lua Scripts |

---

# Project Structure

```text
distributed-rate-limiter/
│
├── app/
│   ├── algorithms/
│   ├── middleware/
│   ├── routes/
│   ├── storage/
│   ├── utils/
│   ├── config/
│   └── main.py
│
├── nginx/
│   └── default.conf
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/shlok-git340/distributed-rate-limiter.git

cd distributed-rate-limiter
```

---

## Start Services

```bash
docker compose up --build
```

---

# API Endpoints

## Unlimited Endpoint

```http
GET /unlimited
```

Response:

```json
{
  "message": "Unlimited access"
}
```

---

## Rate Limited Endpoint

```http
GET /limited
```

Response:

```json
{
  "message": "Protected endpoint"
}
```

When rate limit is exceeded:

```json
{
  "error": "Too Many Requests"
}
```

HTTP Status:

```http
429 TOO MANY REQUESTS
```

---

## Runtime Configuration Endpoint

```http
POST /admin/config
```

Example Request:

```bash
curl -X POST http://localhost:8080/admin/config \
-H "Content-Type: application/json" \
-d '{
  "algorithm":"token_bucket",
  "limit":20,
  "window":60
}'
```

---

# Supported Algorithms

| Algorithm | Description |
|---|---|
| fixed_window | Fixed time-window request counting |
| token_bucket | Burst-tolerant token refill strategy |
| sliding_window | Weighted rolling-window implementation |
| sliding_log | Precise rolling-window logging using Lua |

---

# JWT Authentication Example

Generate JWT token:

```python
import jwt

token = jwt.encode(
    {"user_id": "shlok"},
    "super-secret",
    algorithm="HS256"
)

print(token)
```

Use token:

```bash
curl http://localhost:8080/limited \
-H "Authorization: Bearer YOUR_TOKEN"
```

---

# Stress Testing

Example concurrent load test:

```bash
seq 1 50 | xargs -n1 -P20 curl -s \
http://localhost:8080/limited
```

This validates:
- concurrent request handling
- distributed coordination
- atomic Redis operations

---

# Key Engineering Concepts Demonstrated

- Distributed Systems
- Middleware Architecture
- Redis Coordination
- Atomic Operations
- Concurrency Control
- API Gateway Patterns
- Request Throttling
- Horizontal Scaling
- Load Balancing
- JWT Authentication
- Docker Orchestration

---

# Future Improvements

- Redis Cluster support
- API key management
- Admin dashboard
- Rate limit analytics
- Request priority queues
- Geo-based throttling
- Adaptive rate limiting
- Kubernetes deployment

---
