.PHONY: clean test docs-test test-all cov-html cov-report docs-build repl docs-show cov-show typecheck

all: clean test report html

BUILDDIR=$(DEV_HOME)/build/qtile

clean:
	env COVERAGE_FILE=$(BUILDDIR)/.coverage coverage erase
	@rm -rf $(BUILDDIR)/doctrees

cov-html:
	env COVERAGE_FILE=$(BUILDDIR)/.coverage coverage html -d $(BUILDDIR)/htmlcov/

cov-report:
	env COVERAGE_FILE=$(BUILDDIR)/.coverage coverage report

cov-show:
	/usr/bin/start $(BUILDDIR)/htmlcov/index.html

docs-build:
	sphinx-build -a -b html -d $(BUILDDIR)/doctrees ./src/docs ./docs

docs-test:
	tox -e doc

docs-show:
	/usr/bin/start ./doc/index.html

docs-publish:
	git subtree push --prefix docs origin gh-pages

install:
	cp -r ./src/config/* $HOME/.config/qtile/

repl:
	env PYTHONPATH=src python

test:
	tox

test-all:
	tox -e py38,doc

typecheck:
	@cd src
	mypy confi
	@cd ..
