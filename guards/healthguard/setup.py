from setuptools import setup, find_packages

setup(
    name="poisonguard",
    version="0.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "poisonguard=poisonguard.api:main",
        ],
    },
)