# Week 2 – Database Enhancements (Maritime Platform)

## Scope
This repository contains the Week-2 database enhancements for the Maritime Vessel Tracking platform.

## Work Completed
- Extended the Vessel model to support real-time tracking data:
  - Speed
  - Heading
  - Last update timestamp (existing)
  - Latitude and longitude (existing)
- Created a Subscription model to link users with vessels and store alert preferences.
- Established proper foreign key relationships between User, Vessel, and Subscription.
- Ran and applied database migrations successfully without impacting existing data.
- Added sample vessel and subscription records using Django Admin.
- Verified data integrity and relationships using Django shell.

## Tech Stack
- Django
- Django ORM
- SQLite (development)

## Setup Instructions
```bash
pip install django djangorestframework
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
