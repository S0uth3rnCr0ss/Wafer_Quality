from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e.'

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n") for req in requirements]
        
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
        
    print("==================================================================")
    print("requiremments======================================>", requirements)
    print("==================================================================")
    return requirements

setup(
    name = "Fault_Detection",
    version = "1.0.0",
    author = "Arma",
    install_requirements = ('requirements.txt'),
    packages = find_packages()
)