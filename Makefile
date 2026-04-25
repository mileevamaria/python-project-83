install:
    uv sync
lint:
	uv run ruff check page_analyzer
test:
    pytest
build:
    ./build.sh

PORT ?= 8000
start:
    uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
dev:
    uv run flask --debug --app page_analyzer:app run
render-start:
    gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
    
shell-rec:
	asciinema rec demo.cast
shell-upload:
	asciinema upload demo.cast