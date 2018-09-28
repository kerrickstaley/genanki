.PHONY: install
install:
	python3 setup.py install --user

publish_test:
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish_real:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
