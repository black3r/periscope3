all: build

build:
	python3 setup.py build

dist: build
	python3 setup.py install --root=${PWD}/package/

install:
	python3 setup.py install

prepclean:
	rm -rf /tmp/peri

clean: prepclean
	mkdir /tmp/peri
	mv .gitignore /tmp/peri/.gitignore
	git clean -f -d
	mv /tmp/peri/.gitignore .gitignore
	rm -rf /tmp/peri -v
