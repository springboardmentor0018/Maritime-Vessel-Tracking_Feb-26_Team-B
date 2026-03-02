# Week 3 – Database Enhancements (Maritime Platform)

## Overview
This repository contains the **Week 3 database enhancements** for the **Maritime Vessel Tracking Platform**, focusing on **port congestion tracking** and a **scalable notification system** for operational alerts.

---

## Scope
- Port-level operational data tracking  
- Enhanced notification system with multiple alert categories  
- Improved database integrity and admin usability  

---

## Features & Work Completed

### 🚢 Port Management
Implemented a **Port** model to store and analyze port-level operational data:
- Port name  
- Location and country  
- Congestion score  
- Average wait time  
- Arrivals and departures  
- Last updated timestamp  

---

### 🔔 Notification System
Enhanced the **Notification** model to support multiple alert categories:
- Port congestion alerts  
- Weather alerts  
- Safety alerts  

Additional enhancements:
- Linked notifications to ports using foreign key relationships  
- Added notification lifecycle tracking (`is_read` flag)  
- Ensured backward compatibility with safe default values  

---

### 🧩 Database Integrity
- Maintained proper foreign key relationships across:
  - User  
  - Port  
  - Vessel  
  - Notification  
- Ran and applied migrations successfully without data loss  
- Validated schema and ORM behavior using the Django shell  

---

### 🛠️ Admin UI Optimization
Optimized Django Admin for improved usability:
- Faster search and filtering  
- Read-only timestamp fields  
- Custom admin actions (mark notifications as read)  
- Added sample port and notification data via Admin UI  

---

## Tech Stack
- Django  
- Django ORM  
- SQLite (development)

---

## Setup Instructions
```bash
pip install django djangorestframework
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver