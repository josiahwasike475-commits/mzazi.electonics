FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=3000
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 3000
CMD sh -c 'python manage.py migrate --noinput && gunicorn mzazi_config.wsgi:application --bind 0.0.0.0:${PORT:-3000}'
