import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boardwatch-api",
    version="0.1.0",
    author="Nathan Alexander Page",
    author_email="nathanalexanderpage@gmail.com",
    description="An API used to find and track video game products across multiple web-based listing services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nathanalexanderpage/boardwatch_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Games/Entertainment",
    ],
    python_requires='>=3.8',
)