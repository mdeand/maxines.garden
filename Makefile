run: 
	python3.12 src/main.py

fmt: 
	black src

format: 
	black src

css-watch:
	tailwindcss -i ./styles/stylesheet.css -o ./dist/stylesheet.css --minify --watch

.PHONY: run