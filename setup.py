from setuptools import find_packages, setup  # type: ignore

setup(
    name="symeo-python",
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    install_requires=["pyyaml", "typer[all]", "requests"],
    extra_require={},
    url="https://github.com/symeo-io/symeo-python",
    author="Symeo.io",
    author_email="support@symeo.io",
    description="Symeo python SDK with embedded CLI for conf as code",
    entry_points={
        "console_scripts": [
            "symeo-python = symeo_python.cli.main:cli",
        ],
    },
)
