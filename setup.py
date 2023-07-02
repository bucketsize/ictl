import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "ictl",
    version = "0.0.1",
    author = "Jaya Balan Aaron",
    author_email = "bucket.size@gmail.com",
    description = "control stuff from a terminal",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "package URL",
    project_urls = {
        "Bug Tracker": "package issues URL",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
    ],
    packages = ['ictl'],
    scripts = ['bin/ictl'],
    include_package_data=True,
    python_requires = ">=3.6"
)
