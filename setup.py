import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("requirements-dev.txt") as f:
    extras_require = {"dev": f.read().splitlines()}

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
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.10",
)
