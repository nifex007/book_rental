release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn books_rental.wsgi --log-file -