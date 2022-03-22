init:
	@pip install -r requirements.txt

build: test clean
    @pip install -U setuptools wheel
	python setup.py bdist_wheel

test:
	pytest --mypy --mypy-ignore-missing-imports -v --capture=no
	flake8

clean:
	rm -rf ffbuild build dist $(package).egg-info
