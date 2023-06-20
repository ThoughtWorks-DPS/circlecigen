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
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "pathvalidate",
        "jinja2"
    ],
    python_requires=">=3.7",
    entry_points='''
        [console_scripts]
        circlecigen=src.circlecigen:cli
    '''
)
