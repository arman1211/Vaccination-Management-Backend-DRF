# VacciSure Backend

This repository contains the backend of the VacciSure vaccination management system built with Django and Django Rest Framework. The project includes patient and doctor management, vaccine campaigns, appointment booking, and reporting. 

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)

## Features

- User authentication with login and logout
- Patient registration, profile update, and password change
- Doctor registration and profile update
- Vaccine campaign listing, creation, editing, and deletion
- Vaccine dose booking, review, and report generation

## Requirements

- Python 3.x
- Django
- Django Rest Framework

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/arman1211/Vaccination-Management-Backend-DRF.git
    cd Vaccination-Management-Backend-DRF
    ```

2. **Create and Activate a Virtual Environment**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Database**
    - Ensure you have a PostgreSQL database or any other supported database and update the `DATABASES` setting in your Django `settings.py` file.

5. **Run Migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```

## Running the Server

Start the development server:

```bash
python manage.py runserver
```
### Api Endpoint

## API Endpoints

### User Authentication
- **Login**  
  `POST /api/user/login/`  
  Authenticate a user and retrieve access tokens.

- **Logout**  
  `POST /api/user/logout/`  
  Invalidate the user session and log out.

### Patient Management
- **Register Patient**  
  `POST /api/patient/register/`  
  Register a new patient account.

- **List Patients**  
  `GET /api/patient/list/`  
  Retrieve a list of all patients (authentication required).

- **Activate Patient Account**  
  `GET /api/patient/active/<uid64>/<token>/`  
  Activate a newly registered patient account via token.

- **Update Patient Profile**  
  `PATCH /api/patient/update-patient/<int:id>/`  
  Update the patient profile information.

- **Change Patient Password**  
  `PATCH /api/patient/update-password/<int:id>/`  
  Change the patient's password.

### Doctor Management
- **Register Doctor**  
  `POST /api/doctor/register/`  
  Register a new doctor account.

- **List Doctors**  
  `GET /api/doctor/list/`  
  Retrieve a list of all doctors (authentication required).

- **Activate Doctor Account**  
  `GET /api/doctor/active/<uid64>/<token>/`  
  Activate a newly registered doctor account via token.

- **Update Doctor Profile**  
  `PATCH /api/doctor/update-doctor/<int:id>/`  
  Update the doctor's profile information.

### Vaccine Campaign
- **List Vaccine Campaigns**  
  `GET /api/vaccine-campaign/list/`  
  Retrieve a list of all available vaccine campaigns.

- **Vaccine Campaign Details**  
  `GET /api/vaccine-campaign/lists/<int:pk>/`  
  Get details of a specific vaccine campaign by ID.

- **Book Vaccine Dose**  
  `POST /api/vaccine-campaign/post/`  
  Book a vaccine dose for a patient.

- **List Patient Bookings**  
  `GET /api/vaccine-campaign/bookings/<int:patient_id>/`  
  Retrieve all vaccine dose bookings for a specific patient.

- **Mark Vaccine Dose as Complete**  
  `PATCH /api/vaccine-campaign/complete/<int:id>/`  
  Update a booking to mark a vaccine dose as completed.

- **Post Vaccine Review**  
  `POST /api/vaccine-campaign/review/post/`  
  Submit a review for a specific vaccine campaign.

- **Edit Vaccine Campaign**  
  `PATCH /api/vaccine-campaign/edit/<int:id>/`  
  Modify details of an existing vaccine campaign.

- **Delete Vaccine Campaign**  
  `DELETE /api/vaccine-campaign/delete/<int:id>/`  
  Remove a specific vaccine campaign by ID.

- **Delete Vaccine Booking**  
  `DELETE /api/vaccine-campaign/booking/delete/<int:id>/`  
  Remove a specific vaccine dose booking by ID.

- **Generate PDF Report**  
  `GET /api/vaccine-campaign/vaccine-dose-report/<int:id>/`  
  Generate and download a PDF report for a completed vaccine dose.

