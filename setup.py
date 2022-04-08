import os

import setuptools

from setuptools import find_namespace_packages, setup
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements

import user_agreement_core_lib

dir_path = os.path.dirname(os.path.realpath(__file__))
install_reqs = parse_requirements(os.path.join(dir_path, 'requirements.txt'), session=PipSession)
requirements = []
try:
    requirements = [str(ir.req) for ir in install_reqs]
except:
    requirements = [str(ir.requirement) for ir in install_reqs]

packages1 = setuptools.find_packages()
packages2 = find_namespace_packages(include=['hydra_plugins.*'])
packages = list(set(packages1 + packages2))

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name='user_agreement_core_lib',
        version=user_agreement_core_lib.__version__,
        author='Shay Tessler',
        author_email='shay.te@gmail.com',
        description='A simple CoreLib for user agreement creation and recording',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/shay-te/user-agreement-core-lib',
        packages=packages,
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=requirements,
        include_package_data=True,
        python_requires='>=3.7',
    )
