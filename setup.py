from setuptools import find_packages, setup
from typing import List

REQUIREMENTS_FILE_NAME = "requirements.txt"
HYPERLINK_EDITABLE = "-e ."

def get_requirements() -> List[str]:
    with open(REQUIREMENTS_FILE_NAME) as requirements_file:
        requirement_list = [line.strip() for line in requirements_file if line.strip()]

    if HYPERLINK_EDITABLE in requirement_list:
        requirement_list.remove(HYPERLINK_EDITABLE)

    return requirement_list

setup(
    name="Shipment Pricing",
    version="0.1.3",
    author="Hitesh Nimbalkar",
    author_email="nimbalkarhitesh@gmail.com",
    description="ML Regression",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11"
    ],
    keywords="Regression",
    
)