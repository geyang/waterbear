# shell option to use extended glob from from https://stackoverflow.com/a/6922447/1560241
SHELL:=/bin/bash -O extglob

author=$(Ge Yang)
author_email=$(yangge1987@gmail.com)

# notes on python packaging: http://python-packaging.readthedocs.io/en/latest/minimal.html
default: ;
wheel:
	rm -rf dist
	python setup.py bdist_wheel
dev:
	make wheel
	pip install --ignore-installed dist/waterbear*.whl
convert-rst:
	pandoc -s README.md -o README --to=rst
	sed -i '' 's/code/code-block/g' README
	sed -i '' 's/\.\//https\:\/\/github\.com\/episodeyang\/waterbear\/blob\/master\//g' README
#	sed -E -i '' 's/\.(jpg|png)/.\1?raw=true/g' README
	perl -p -i -e 's/\.(jpg|png)/_resized.$$1?raw=true\n   :width: 355px\n   :height: 266px\n   :scale: 50%/' README
	rst-lint README
release:
	git tag v`< VERSION` -m '$(msg)'
	git push origin --tags
resize:
	# from https://stackoverflow.com/a/28221795/1560241
	echo ./figures/!(*resized).jpg
	convert ./figures/!(*resized).jpg -resize 888x1000 -set filename:f '%t' ./figures/'%[filename:f]_resized.jpg'
update-doc: resize convert-rst
	python setup.py sdist upload
publish: resize convert-rst
	make test
	make wheel
	twine upload dist/*
test:
	pytest --capture=no
