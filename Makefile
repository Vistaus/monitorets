SOURCE_DIR=src
REQUIREMENTS_TXT=requirements.txt

install-dev-requirements:
	pipenv sync --dev --verbose

generate-python-gtk-symbols: install-dev-requirements
	pipenv run gengir --gtk 4

setup-dev-environment: install-dev-requirements generate-python-gtk-symbols

dev-shell:
	pipenv shell

update-po-files:
	find . -name *.po -exec xgettext --no-location --omit-header -j -f po/POTFILES -o {} \;
	find . -name *.po -exec xgettext --omit-header -j -f po/POTFILES -o {} \;

test:
	pipenv run pytest

check-linting:
	pipenv run black --check $(SOURCE_DIR)

linting:
	pipenv run black $(SOURCE_DIR)

_generate-requirements-txt:
	pipenv requirements > $(REQUIREMENTS_TXT)

_delete-requirements-txt:
	rm $(REQUIREMENTS_TXT)

_generate-dependencies-json-file:
	python ./build_helper/flatpak-pip-generator.py --requirements-file=$(REQUIREMENTS_TXT) --output pypi-dependencies

update-dependencies-manifest: _generate-requirements-txt _generate-dependencies-json-file _delete-requirements-txt

validate-app-data:
	flatpak run --env=G_DEBUG=fatal-criticals --command=appstream-util org.flatpak.Builder validate data/io.github.jorchube.monitorets.appdata.xml.in
