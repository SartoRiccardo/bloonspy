import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bloonspy",
    version="0.1",
    author="TheSartorsss",
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
    python_requires='>=3.6',
)