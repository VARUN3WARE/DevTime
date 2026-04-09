from setuptools import setup, find_packages

setup(
    name="devos",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "watchdog",
        "psutil",
        "python-daemon",
    ],
    entry_points={
        "console_scripts": [
            "devos=devos.cli.main:app",
        ],
    },
)
