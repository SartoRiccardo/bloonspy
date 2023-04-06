import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

metadata = {}
with open("bloonspy/__init__.py", "r") as fh:
    metadata_str = fh.read()
metadata_fields = [
    (r"__version__ = \"(\d+\.\d+\.\d+)\"\n", "version"),
    (r"__author__ = \"([\w\s]+)\"\n", "author")
]
for regex, field_name in metadata_fields:
    metadata[field_name] = re.search(regex, metadata_str).group(1)


setuptools.setup(
    **metadata,
    name="bloonspy",
    description="A Python wrapper for the Ninja Kiwi Open Data API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SartoRiccardo/bloonspy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)