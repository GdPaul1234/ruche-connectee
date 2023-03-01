# Super Hive release notes

## v0.4.0 [Pusher] Initial support for sensor pushers

- Fix: Simplify pusher architecture
- Fix: Migrate from python built-in configparser to Pydantic BaseSettings
  - Validated environment variable on runtime!
- Add: Fallback when main endpoint cannot be reached
- Add: Sample pusher: DummyWeightSensorPusher

The launch of puher is managed externally via cron for example

---

## v0.3.2 [Frontend] Fix mobile navigation for sensors

- Fix: Hide sensors lists when showing sensor data on mobile

---

## v0.3.1 [Backend] Unit tests

- Add: Pytest fixtures (database connection, entities setup and teardown)
- Add: Behive router tests
- Add: Sensor router tests
- Bug: Disable token signature verification

---

## v0.3.0 [Backend] Indoor and outdoor temperature and humidity sensors

- Fix: Rename temperature sensor to temperature_indoor
- Fix: Rename humidity sensor to humidity_indoor
- Add: Add temperature_outdoor sensor
- Add: Add humidity_outdoor sensor
- Fix: Aggregated last behive metrics
- Fix: Migrate UI

---

## v0.2.2 [Backend] [Frontend] Fix routers + generate OpenApi client

- Fix: Pydantic models for persisting in the database
- Add: Transactions in insert / delete routes for better realiability and consistency (need replica set)
- Add: Generate Typescript OpenApi 3.0 compliant client
- Fix: Migrate the frontend for mock API call to generated OpenApi call

---

## v0.2.1 [Backend] Sensor and Event routes

- Add: Sensor routers (get values by date range, add record)
- Add: Event routers (get values by date range, add record)

---

## v0.2.0 [Backend] Bootstrap backend

- Add: FastAPI and mongodb client
  - Easy to use python web-framework
  - Declarative path request parameters and body
  - Auto generation of OpenAPI spec
  - Swagger UI included
- Add: OAuth2PasswordBeare based authentication with JWT token
- Add: CRUD APIs for behives

---

## v0.1.2 [Frontend] Various fixes and events page

- Fix: branding color for charts
- Add: Events page (grouped by day)
- Add: Login page

---

## v0.1.1 [Frontend] Mobile UI

- Add: Fully responsive pages
- Add: Mobile navigation (menu hierarchy)
- Add: Date range picker for selecting period in sensor page
- Fix: Branding (favicon, page title...)

---

## v0.1.0 [Frontend] Beekeeper account space

- Add: React router for client-side routing
- Add: React-Chart for charts
- Add: Desktop main menu
- Add: Hive page
- Add: Hive metrics page
- Add: Mock APIs

---

## v0.0.1 Initial version

- Add: Template for sensor pushers
- Add: Initialize frontend and install React and Taillwind CSS libraries
- Add: Librairies for getting data for sensors
