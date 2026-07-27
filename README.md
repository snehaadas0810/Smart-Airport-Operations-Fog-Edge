# Smart Airport Operations — Fog & Edge Computing

Smart Airport Operations is an IoT monitoring system for airport terminal operations, built on a three-tier **Edge → Fog → Cloud** architecture. Five virtual sensors (passenger flow, security queue, gate occupancy, temperature and emergency alerts) publish data over MQTT; an Edge layer validates and timestamps every reading; a Fog layer classifies it and raises threshold-based alerts; and a Django REST backend on AWS EC2 persists the result (via a Celery/Redis task queue) and drives a live, auto-refreshing operations dashboard.

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the System](#running-the-system)
- [Dashboard & API](#dashboard--api)
- [Testing](#testing)
- [Known Limitations / Roadmap](#known-limitations--roadmap)
- [Contributors](#contributors)

## Architecture

```
SENSOR TIER   Passenger Counter · Queue Sensor · Gate Sensor · Temperature Sensor · Emergency Sensor
                                   │  MQTT: airport/raw/<type>
                                   ▼
EDGE TIER     Edge MQTT Subscriber → Edge Processor (validate → timestamp → republish)
                                   │  MQTT: airport/edge/<type>
                                   ▼
FOG TIER      Fog MQTT Receiver → Fog Processor (analytics + alert rules)
                                   │  MQTT: airport/fog/#
                                   ▼
CLOUD TIER    MQTT Consumer (Django thread) → Redis → Celery Worker → Django ORM (SQLite)
   (AWS EC2)                                                              │
                                                                REST API /api/dashboard/
                                                                            │
                                                        Web Dashboard (Bootstrap + Chart.js, 2s poll)
```

Each tier communicates asynchronously over MQTT, so the Sensor, Edge, Fog and Cloud components can be started, stopped or scaled independently. On the Cloud tier, message receipt (MQTT consumer) is decoupled from database persistence using a Celery task queue backed by Redis, so a slow database write never blocks the MQTT client.

## Features

- **5 virtual sensor types** — Passenger Counter, Queue Sensor, Gate Sensor, Temperature Sensor, Emergency Sensor — each publishing on its own configurable interval.
- **Edge validation** — malformed payloads are dropped close to the source instead of reaching the Fog or Cloud tiers.
- **Fog analytics & alerting** — passenger-flow classification (LOW / MEDIUM / HIGH) and threshold-based alerts (e.g. high passenger traffic).
- **Asynchronous Cloud ingestion** — MQTT → Redis → Celery worker → Django ORM, so ingestion and persistence scale independently.
- **REST API** (`/api/dashboard/`) aggregating the latest reading per sensor type plus passenger-count history.
- **Live dashboard** — Bootstrap + Chart.js, KPI cards, trend charts and a recent-activity table, refreshing every 2 seconds.
- **Cloud deployment** on AWS EC2.

## Tech Stack

| Layer | Technology |
|---|---|
| Sensors / Edge / Fog | Python 3, paho-mqtt |
| Message broker | Eclipse Mosquitto (MQTT) |
| Task queue | Celery, Redis |
| Backend | Django 6.0, Django REST Framework |
| Database | SQLite (PostgreSQL-ready via psycopg2-binary) |
| Static files | WhiteNoise |
| Frontend | Bootstrap 5, Chart.js |
| Deployment | AWS EC2 (Ubuntu) |

## Project Structure

```
Smart-Airport-Operations-Fog-Edge/
├── sensors/            # Virtual sensors + sensor manager
│   ├── base_sensor.py
│   ├── passenger_sensor.py
│   ├── queue_sensor.py
│   ├── gate_sensor.py
│   ├── temperature_sensor.py
│   ├── emergency_sensor.py
│   ├── mqtt_client.py
│   └── sensor_manager.py
├── edge/                # Edge tier: validate, timestamp, republish
│   ├── mqtt_subscriber.py
│   ├── edge_processor.py
│   ├── validator.py
│   ├── publisher.py
│   └── logger.py
├── fog/                 # Fog tier: analytics + alerting
│   ├── mqtt_receiver.py
│   ├── fog_processor.py
│   ├── analytics.py
│   ├── alert_manager.py
│   └── publisher.py
├── backend/             # Django Cloud tier
│   ├── airport/         # Models: PassengerData, QueueStatus, GateStatus, TemperatureLog, EmergencyAlert
│   ├── api/              # REST endpoint (/api/dashboard/)
│   ├── dashboard/        # Dashboard template, static assets, Celery task
│   ├── mqtt_consumer/    # Background MQTT client → enqueues Celery task
│   └── airport_backend/  # Django project settings, Celery app config
└── requirements.txt
```

## Prerequisites

- Python 3.11+
- An MQTT broker (e.g. [Eclipse Mosquitto](https://mosquitto.org/download/))
- Redis (for the Celery task queue)
- pip / virtualenv

## Setup

```bash
# Clone the repository
git clone https://github.com/snehaadas0810/Smart-Airport-Operations-Fog-Edge.git
cd Smart-Airport-Operations-Fog-Edge

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install celery redis         # not yet pinned in requirements.txt — see Known Limitations

# Apply Django migrations
cd backend
python manage.py migrate
```

Update `ALLOWED_HOSTS`, `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` in `backend/airport_backend/settings.py` if your MQTT broker or Redis instance are not on `localhost`.

## Running the System

Each tier runs as its own process. Open a separate terminal for each:

```bash
# 1. Start the MQTT broker (if not already running as a service)
mosquitto

# 2. Start Redis (if not already running as a service)
redis-server

# 3. Start the Django backend (also starts the MQTT consumer thread)
cd backend
python manage.py runserver 0.0.0.0:8000

# 4. Start the Celery worker
cd backend
celery -A airport_backend worker --loglevel=info

# 5. Start the Fog tier
cd fog
python mqtt_receiver.py

# 6. Start the Edge tier
cd edge
python mqtt_subscriber.py

# 7. Start the sensors
cd sensors
python sensor_manager.py
```

Once all processes are running, open the dashboard at:

```
http://localhost:8000/
```

## Dashboard & API

- **Dashboard:** `GET /` — live KPI cards, passenger-flow/queue/gate charts and a recent-activity table, polling `/api/dashboard/` every 2 seconds.
- **REST API:** `GET /api/dashboard/` — returns the latest reading for each sensor type plus recent passenger-count history as JSON.

## Testing

The pipeline was validated end to end by running every tier concurrently and confirming:
- Edge validation drops malformed payloads before they reach the Fog tier.
- Fog classification and alert thresholds behave correctly at boundary values.
- MQTT messages are correctly enqueued as Celery tasks and persisted via the Django ORM.
- The dashboard and REST API reflect the latest sensor state within the polling interval.

## Known Limitations / Roadmap

- `celery` and a Redis client are used in code but not yet pinned in `requirements.txt`.
- The Fog tier currently republishes all sensor types onto a single MQTT topic rather than per-type topics.
- Queue/Gate status classification currently happens in the Celery task rather than in the Fog Processor.
- `ALLOWED_HOSTS` currently includes a wildcard (`*`) — should be narrowed before production use.
- Planned: WebSocket-based dashboard updates (Django Channels), automated CI/CD, real unit/integration tests, and PostgreSQL migration.

## Contributors

- [Sneha Das](https://github.com/snehaadas0810)
