#!/bin/bash
version=$(echo "$CIRCLE_TAG" | cut -d '-' -f2)
twine upload dist/symeo-python-"$version".tar.gz dist/symeo_python-"$version"-py3-none-any.whl -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD"