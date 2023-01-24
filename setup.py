from setuptools import find_packages, setup
from typing import List

# assign the requirements.txt file to a variable
requirement_file_name = "requirements.txt"
REMOVE_PACKAGE = "-e ."

# function to open the requirement file
def get_requirements()->List[str]:
    with open(requirement_file_name) as requirement_file:
        requirement_list = requirement_file.readline()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]

    if REMOVE_PACKAGE in requirement_list:
        requirement_list.remove(REMOVE_PACKAGE)
    return requirement_list

setup(name='Insurance',
      version='1.0',
      description='Insurance premium prediction Industry level implimentation',
      author='AswanthAnu',
      author_email='aswanthanu777@gmail.com',
      packages=find_packages(),
      install_reqires=get_requirements()

     )

