# Candidate Management API

A FastAPI backend for handling candidate registrations, job applications, and background task processing.

## Features
- Candidate CRUD
- Application submission + status
- Skill filtering & pagination
- JWT authentication
- Redis queue for async background tasks
- Dockerized with PostgreSQL and Redis

## Running the App

```bash
docker-compose up --build