# DoctorGPT

Extensions needed for project to run:
- pip install Flask
- pip install bootstrap-flask
- pip install Flask-Login
- pip install psycopg2


Aanpassingen aan packages:
- In flaks_login/utils.py verwijder volgende imports:
    - from werkzeug.urls import url_encode
    - from werkzeug.urls import url_decode