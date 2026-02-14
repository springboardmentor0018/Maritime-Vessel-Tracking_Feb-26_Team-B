# Week 1 – Backend Setup (Maritime Platform)

## Scope
This repository contains the **Week-1 database and backend setup** for the Maritime Vessel Tracking platform.

## Work Completed
- Designed database schema for users, vessels, ports, voyages, events, and notifications
- Implemented Django models with proper relationships
- Used Django’s built-in User model for authentication
- Created a UserProfile table to store application-specific roles:
  - Operator
  - Analyst
  - Admin
- Generated and applied migrations to create all tables
- Added sample data using Django Admin
- Verified tables and data using Django shell
- Implemented basic authentication APIs (register, login, profile)

## Tech Stack
- Django
- Django REST Framework
- Django ORM
- SQLite (development)

## Setup Instructions
```bash
pip install django djangorestframework
python manage.py migrate
python manage.py runserver

