from setuptools import setup

setup(
    name="conf",
    version="0.0.1",
    description="Open file in an instant",
    author="Ritik Ranjan",
    author_email="ranjan5ritik@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    install_requires=[
        "toml", "click"
    ],
    entry_points={"console_scripts": ["conf=main.__main__:main"]},
)
