clean:
	mkdir /tmp/peri
	mv .gitignore /tmp/peri/.gitignore
	git clean -f -d
	mv /tmp/peri.gitignore .gitignore
	rm -rf /tmp/peri -v
