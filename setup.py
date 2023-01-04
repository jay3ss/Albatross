import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="albatross",
    version="0.0.1",
    author="jay3ss",
    description="A CMS for the Pelican static site generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jay3ss/albatross",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "FastAPI",
        "Jinja2",
        "Markdown",
        "Pelican",
        "pydantic",
        "python-dateutil",
        "python-dotenv",
        "python-slugify",
        "SQLAlchemy",
        "uvicorn",
    ],
    python_requires=">=3.10",
)
