# Edvely

Edvely is a Django-based course marketplace app with user auth, course listings, and Razorpay payments.




<img width="1902" height="857" alt="image" src="https://github.com/user-attachments/assets/84f0dbfc-002e-4ce7-af74-65913ddc0182" />



<img width="1853" height="847" alt="image" src="https://github.com/user-attachments/assets/50204f14-6969-4b10-881c-6be63784a226" />



<img width="1859" height="824" alt="image" src="https://github.com/user-attachments/assets/4935fe48-3d58-4a55-85eb-fa108a299cbe" />


<img width="1323" height="869" alt="image" src="https://github.com/user-attachments/assets/1d258d28-e720-4993-ae55-ec4fc4cd718c" />


<img width="1919" height="864" alt="image" src="https://github.com/user-attachments/assets/88cdaa14-28a6-477f-a984-218ca78691f7" />

- If not, course buy then only some videos are free for preview


<img width="1869" height="859" alt="image" src="https://github.com/user-attachments/assets/a2f2b5c6-9b17-45b4-948b-f1f8eae8954e" />



## Tech stack

- Backend: Django 5.2, Python 3
- Database: SQLite (default), PostgreSQL via `DATABASE_URL`
- Payments: Razorpay
- Static files: WhiteNoise
- Media: Pillow
- Deploy: Gunicorn, Docker (Dockerfile + docker-compose)

## Working (how it runs)

- Django project: `course`
- Main app: `sell`
- Templates: `sell/templates/`
- Static assets: `sell/static/`
- Media uploads: `media/`
- Auth flow: login/registration in `sell/templates/registration/`

## Local setup

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000/

## Environment variables

Create a `.env` in the project root if needed:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (1/0)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DATABASE_URL` (optional, e.g. Postgres)
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`

## Useful commands

```bash
python manage.py createsuperuser
python manage.py collectstatic
```
