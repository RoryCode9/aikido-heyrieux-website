HUGO ?= hugo

.PHONY: dev build check clean

dev:
	$(HUGO) server --disableFastRender --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/

build:
	$(HUGO) --gc --minify

check: build
	python3 scripts/check_site.py public

clean:
	rm -rf public resources/_gen .hugo_build.lock
