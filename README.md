# DoctorGPT

Extensions needed for project to run:

- pip install Flask
- pip install bootstrap-flask
- pip install Flask-Login
- pip install psycopg2
- pip install python-dotenv
- pip install openai

Aanpassingen aan packages:

- In flaks_login/utils.py verwijder volgende imports:
  - from werkzeug.urls import url_encode
  - from werkzeug.urls import url_decode

Benodigd in de ENV-file:

- USER_DB=postgres
- PASSWORD_DB=password
- HOST_DB=localhost
- PORT_DB=5432

Gebruik NLP:

- Installeer nodige packages

  - cd in root van project
  - run pip install -r requirements.txt

- Aanmaken/ trainen van model:
  - cd in webapp/nlp en run main.py
  - symptom_model.joblib zou aangemaakt moeten zijn
  - cd webapp/ en run app.py zoals normaal
  - chat met bot
 
- Link naar LLM op HuggingFace:
  https://huggingface.co/Torando/doctor-gpt-gguf
