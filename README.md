# Mzazi Electronics

A Django-based storefront and shop-management foundation for Mzazi Electronics, owned by Josiah Wasike.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:3000
```

Open `/` for the customer storefront and `/django-admin/` for the Django management area. The first storefront request creates clearly marked demo catalogue records with no invented prices or stock; replace those values from the admin before selling.

## M-Pesa

Set `MPESA_CONSUMER_KEY`, `MPESA_CONSUMER_SECRET`, `MPESA_SHORTCODE`, `MPESA_PASSKEY`, `MPESA_CALLBACK_URL`, and `MPESA_ENVIRONMENT` in the runtime environment. STK Push remains explicitly unavailable until those values exist. Only a verified successful callback marks an order paid; no M-Pesa PIN is stored.

## Production notes

Use PostgreSQL, HTTPS, a production WSGI server, configured email delivery for password reset, durable media storage, and a public Safaricom callback URL before launch. The included Dockerfile runs migrations and Gunicorn on `$PORT`.
