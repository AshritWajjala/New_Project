from setuptools import find_packages, setup # find_packages scans for all the __init__.py files and make parent folder as packages
from typing import List

def get_requirements()->List[str]:
    """
    This function will return the list of requirements

    """
    requirement_list:List[str] = []
    try:
        with open('requirements.txt') as f:
            # Read lines from the file
            lines = f.readlines()
            for line in lines:
                requirement = line.strip() # Remove spaces
                if requirement and requirement != '-e .': # Ignore empty lines and '-e .'
                    requirement_list.append(requirement)
        
        return requirement_list
    except:
        pass

    return requirement_list

setup(
    name='Network Security',
    version='0.0.1',
    author='Ashrit Wajjala',
    author_email='ashritw2000@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)