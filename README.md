# drf-api
A template to easily start coding simple REST APIs

## Quick start

Configure PostgreSQL:
```sql
create database backend;
create USER backend;
alter USER backend with ENCRYPTED PASSWORD 'backend';
alter database backend owner to backend ;
```

Create virtual environment:
```bash
cd backend/
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Migrate and create superuser:
```bash
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
```

Run server:
```bash
python manage.py runserver
```

And visit: http://localhost:8000/
