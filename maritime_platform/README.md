# Week 4 – Database Enhancements (Maritime Platform)

## Overview
This repository contains the **Week 4 database enhancements** for the **Maritime Vessel Tracking Platform**, focusing on **voyage history tracking**, **analytics data structures**, and **export-ready voyage records** for operational reporting and analysis.

---

## Scope
- Voyage movement history tracking  
- Analytics tables for operational insights  
- Export-ready voyage records  
- Improved database structure for scalable analytics  

---

## Features & Work Completed

### 🧭 Voyage History Tracking
Implemented a **VoyageHistory** model to track vessel movement during voyages.

Stored information includes:
- Linked voyage reference  
- Latitude and longitude coordinates  
- Timestamp of vessel location updates  
- Event descriptions for voyage replay  

This enables **reconstruction and replay of vessel routes**, allowing the platform to analyze vessel movement over time.

---

### 📊 Analytics Tables
Created dedicated analytics tables to support operational reporting and insights.

#### Company Analytics
Tracks statistics related to shipping companies:
- Total vessels operated  
- Total voyages completed  
- Number of incidents reported  

#### Port Analytics
Captures port-level operational performance:
- Total arrivals  
- Total departures  
- Congestion index  
- Average vessel wait time  

#### Insurer Analytics
Provides insurance-related operational statistics:
- Total vessels insured  
- Incidents reported  
- Claims processed  
- Risk score metrics  

These tables support **analytics dashboards and operational monitoring systems**.

---

### 📤 Voyage Export Support
Enhanced the **Voyage** model with export-related fields:

- `export_ready` – indicates whether a voyage record is ready for export  
- `exported_at` – timestamp indicating when the export occurred  

This enables integration with **data pipelines and reporting workflows**.

---

### 🧩 Database Integrity
- Maintained proper foreign key relationships across:
  - Vessel  
  - Voyage  
  - VoyageHistory  
  - Port  
  - Analytics tables  
- Generated and applied migrations successfully  
- Validated database schema using the Django Admin interface and Django shell  

---

### 🛠️ Migration Execution
Applied database migrations to update the schema.

```bash
pip install django djangorestframework
python manage.py makemigrations
python manage.py migrate
python manage.py runserver