## Generate setup.py by poetry command for shared package

PACKAGE = asdf-auto-install

.PHONY: build-package
build-package:
	$(eval VERSION := $(shell poetry version -s))
	poetry build
	@tar zxf dist/$(PACKAGE)-$(VERSION).tar.gz -C ./dist
	@cp dist/$(PACKAGE)-$(VERSION)/setup.py setup.py
	@rm -rf dist
