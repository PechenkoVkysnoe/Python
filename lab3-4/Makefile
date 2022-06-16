run:
	python3 manage.py runserver 0.0.0.0:8000

makemigrations:
	python3 manage.py makemigrations mainapp

migrate:
	python3 manage.py migrate
	
db:
	python3 manage.py makemigrations mainapp
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser

coverage: 
	rm -rf htmlcov/
	coverage run --source="." manage.py test
	coverage html

test:
	python3 manage.py test