run:
	./manage.py runserver 0.0.0.0:8000

migrate:
	./manage.py migrate ${app}

superuser: migrate
	./manage.py createsuperuser

makemigrate:
	./manage.py makemigrations ${app}

app:
	./manage.py startapp ${name}

test:
	pytest ${app}
