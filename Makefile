.PHONY: help serve build check update compare test

help:
	@echo "Comandos disponibles:"
	@echo "  make serve    - Arranca el servidor local de desarrollo con borradores (verifica versiones)"
	@echo "  make build    - Compila el sitio estático para producción en ./public (verifica versiones)"
	@echo "  make check    - Comprueba alineación de versiones de Hugo y Go"
	@echo "  make compare  - Compila y compara el resultado con la web en producción para evitar regresiones"
	@echo "  make update   - Trae cambios del remoto, actualiza módulos de Hugo y valida versiones"
	@echo "  make test     - Ejecuta las pruebas unitarias de los scripts"

check:
	@./scripts/check-versions.sh

serve: check
	hugo server -D

build: check
	hugo --gc --minify

compare: build
	python3 scripts/compare-site.py --new public --prod https://www.agustinventura.dev

update:
	git pull
	hugo mod get -u
	hugo mod tidy
	@./scripts/check-versions.sh

test:
	python3 -m unittest scripts/test_compare_site.py
