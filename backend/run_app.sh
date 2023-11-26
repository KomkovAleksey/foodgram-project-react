while ! nc -z db 5432;
    do sleep .5;
    echo "wait database";
done;
    echo "connected to the database";

python manage.py collectstatic --noinput;
gunicorn -b 0:80 foodgram_backend.wsgi;
