while ! nc -z db 5432;
    do sleep .5;
    echo 'wait database';
done;
    echo 'connected to the database';

python manage.py migrate recipes;
python manage.py migrate users;
python manage.py migrate;
python manage.py import_ingredients_data;
python manage.py import_tags_data;
python manage.py collectstatic --noinput;
gunicorn -b 0:8000 foodgram_backend.wsgi;
