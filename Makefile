init:
	cd frontend && cnpm install
	source env/bin/activate && pip install -r backend/requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
	source env/bin/activate && python backend/manage.py makemigrations && python backend/manage.py migrate
	source env/bin/activate && python backend/manage.py init_users
	source env/bin/activate && python backend/manage.py init_cmdb
	source env/bin/activate && python backend/manage.py collectstatic --noinput

migrate:
	source env/bin/activate && python backend/manage.py makemigrations && python backend/manage.py migrate

dev:
	npm run --prefix frontend dev & (source env/bin/activate && python backend/manage.py runserver)

start:
	test ! -f backend/logs/uwsgi.pid && source env/bin/activate && uwsgi --ini backend/uwsgi.ini || echo 'uwsgi running'

stop:
	test -f backend/logs/uwsgi.pid && source env/bin/activate && uwsgi --stop backend/logs/uwsgi.pid || echo 'uwsgi closed'

build-prod:
	npm run --prefix frontend  build:prod
	source env/bin/activate && python backend/manage.py collectstatic --noinput
	test ! -f backend/logs/uwsgi.pid && source env/bin/activate && uwsgi --ini backend/uwsgi.ini || echo 'uwsgi running'

build-test:
	npm run --prefix frontend  build:test
	source env/bin/activate && python backend/manage.py collectstatic --noinput
	source env/bin/activate && uwsgi --reload backend/logs/uwsgi.pid
