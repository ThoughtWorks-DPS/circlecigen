import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="circlecigen",
    author="Nic Cheneweth",
    author_email="nchenewe@thoughtworks.com",
    description="Opinionated generation of continuation pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThoughtWorks-DPS/circlecigen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    entry_points='''
        [console_scripts]
        circlecigen=circlecigen:cli
    '''
)
