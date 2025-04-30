from setuptools import setup
import cmd_router

with open("README.md", "r",encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cmd_router",  # Library name                                  
    version= cmd_router.__version__,  # Version
    
    description="A simple command router for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    author="sioxty",
    author_email="maksymslushayev@gmail.com",
    
    packages=[
        "cmd_router",
    ],
    url="https://github.com/sioxty/cmd_router", 
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
)