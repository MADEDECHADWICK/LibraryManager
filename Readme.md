# Kenyan Library Management System

## Overview
A complete library management solution tailored for Kenyan libraries, featuring:
- MySQL database with Kenyan-context fields
- FastAPI backend with CRUD operations
- Data validation for Kenyan IDs, phone numbers, and counties

## Features

- Kenyan phone number validation (254XXXXXXXXX)
- County-based member locations
- Support for both English and Kiswahili materials
- KICD-approved book tracking

## Python CRUD API
### Technologies:

- FastAPI framework
- MySQL connector
- Validation models

## Endpoints:

- Member management (create, read, update, delete)
- Book inventory management
- Loan processing
- Fine collection with M-Pesa support

### Prerequisites
- MySQL 8.0+
- Python 3.9+

## ERD
- Provided n the code in the ERdiagram.draw.io file

### Installation
1. **Set up database**:
   ```bash
   mysql -u root -p < library_db.sql