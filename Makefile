HUGO ?= hugo

.PHONY: dev build clean

dev:
	$(HUGO) server --disableFastRender --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/

build:
	$(HUGO) --gc --minify

clean:
	rm -rf public resources/_gen .hugo_build.lock
