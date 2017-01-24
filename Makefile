.PHONY: help build serve deploy

help:
	@echo 'Makefile for pyconuk.org'
	@echo ''
	@echo 'Usage:'
	@echo '   make build    build the site into the output directory'
	@echo '   make serve    build the site and serve on port 8000, watching for changes'
	@echo '   make deploy   deploy site'
	@echo ''

build:
	python manage.py buildsite

serve:
	python manage.py serve

deploy:
	./deploy.sh
