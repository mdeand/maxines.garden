run: 
	@python3.12 -m server.main

fmt: 
	@black src

format: 
	@black server tools shared

css-watch:
	@tailwindcss -i ./styles/stylesheet.css -o ./dist/stylesheet.css --minify --watch

compile: 
	@python3.12 tools/compile.py

reset-db: 
	@rm -f .db.sqlite3
	@python3.12 tools/compile.py

.PHONY: run fmt format css-watch