.PHONY: install
install:
	python3 setup.py install --user

publish_test:
	rm -rf dist/*
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish_real:
	rm -rf dist/*
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
