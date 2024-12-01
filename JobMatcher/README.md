by lance cedrick espina pogi

CLUTCH 4HRS AND 20MINS

Web Application built using Django.

User Functionality:
    Upload a resume in PDF format.
    The system uses NLP techniques (TF-IDF, cosine similarity) to match the resume with relevant job listings.

Admin Functionality:
    Create and manage job listings through the Django admin interface.

Technologies Used:
    Django (backend framework).
    scikit-learn for text analysis (TF-IDF, cosine similarity).
    PyPDF2 to extract text from resumes.
    SQLite as the database.

Goal: Suggest job opportunities based on the user’s qualifications extracted from their resume.

HOW TO RUN:

MIGRATE THE DATABASE:

    python manage.py migrate

CREATE A SUPERUSER (for admin access):

    python manage.py createsuperuser

START THE PROJECT:

    python manage.py runserver


ACCESS ADMIN PANEL:

    http://127.0.0.1:8000/admin/

ACCESS UPLOAD:

    http://127.0.0.1:8000/jobs/upload/

ACCESSING THE ADMIN PANEL:

USERNAME: Admin@access
PASSWORD: Admin12345



DJANGO ADMINTRATION

admin

ADMINACCESS