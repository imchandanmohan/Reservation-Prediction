from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirement = f.read().splitlines()

setup(
    name="MLOps-Reservation-Prediction",
    version='0.0.1',
    author="Chandan Mohan",
    author_email="chandan.mohan@gwu.edu",
    packages=find_packages(),
    install_requires=requirement, 
)
