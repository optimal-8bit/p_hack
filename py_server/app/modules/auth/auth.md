# Auth Module

## Purpose
User registration, login, JWT session handling, and Google token login.

## Key Files
- routes.py
- controller.py
- service.py
- schemas.py

## Main Endpoints
- POST /auth/register
- POST /auth/login
- POST /auth/google
- GET /auth/me

## Notes
Auth service stores users in MongoDB and uses shared security helpers.
